import os
import sys
import shutil
import logging
import zipfile

from datetime import datetime
from xml.dom import minidom

class XPSReader:
    '''
    Data reader for XPS files

    Arguments:
        - file_path (string): Path to the XPS file
        - header_size (list of shape [rows, cols]): Size of header in XPS file (number of row, number of columns)
        - temp_folder_path (string): Path for temporary folder (files get extracted here)
    
    Usage:
        Use it with the Python "with" statement:
        ...
        with XPSReader(file_name) as xps:
            ### USE the xps object here ###
        ...
    '''
    def __init__(self, file_path, header_size=[3,4], temp_folder_path='temp'):
        self.file_path = file_path
        self.header_size = header_size
        self.temp_folder_path = temp_folder_path
        self.pages_path = os.path.join(self.temp_folder_path, 'Documents', '1', 'Pages')  # Directory in the unzipped archive under which the page files are located

    def __enter__(self):
        '''
        Enter method, gets called when the class is instanced in a "with" statement. DON'T USE IT DIRECTLY!
        '''
        class XPSReaderInternal:
            '''
            Class for reading the contents of XPS files
            '''
            def __init__(self, file_path, header_size=[3,4], temp_folder_path='temp', pages_path = ''):
                self.file_path = file_path
                self.header_size = header_size
                self.temp_folder_path = temp_folder_path
                self.pages_path = pages_path
                self.pages_files = []  # The list of all pages files will be stored here

                # Remove previous temporary files if there are any
                self._cleanup()

                # Unzip the xps file
                with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                    zip_ref.extractall(self.temp_folder_path)

                # Get the list of pages files and create generators
                if os.path.exists(self.pages_path):
                    pages_files = [p for p in os.listdir(self.pages_path) if os.path.isfile(os.path.join(self.pages_path, p))]  # Get all files in folder
                    pages_files = [p.split('.')[0].zfill(5)+'.'+'.'.join(p.split('.')[1:]) for p in pages_files]  # Zero-fill the page numbers for sorting
                    pages_files.sort()
                    self.pages_files = [p.lstrip('0') for p in pages_files]  # Remove the zeros used for sorting
                    self._page_gen = self._page_reader_generator()
                    self._row_gen = self._row_reader_generator()
                else:
                    logging.error('Could not find path ' + self.pages_path + ' The structure of the archive might be different')  # If this error is thrown self.pages_path is incorrect
                    self._cleanup()
                    sys.exit(1)

            def _page_reader_generator(self):
                '''
                Generator for returning pages one-by-one
                '''
                for page in self.pages_files:
                    data = minidom.parse(os.path.join(self.pages_path, page))

                    # #use getElementsByTagName() to get tag
                    glyphs = data.getElementsByTagName('Glyphs')

                    # Each glyph contains a single element in the table
                    counter = 0
                    header = []
                    row = []
                    page_content = []
                    prev_origin_y = ""
                    for glyph in glyphs:
                        if counter < self.header_size[0]*self.header_size[1]:
                            if (counter+1)%self.header_size[0] == 0:
                                header.append(glyph.attributes['UnicodeString'].value)
                        else:
                            table_element = glyph.attributes['UnicodeString'].value.lstrip()
                            origin_y = glyph.attributes['OriginY'].value.lstrip()
                            if not origin_y == prev_origin_y:
                                if not counter == self.header_size[0]*self.header_size[1]:
                                    time = datetime.strptime(row.pop(), '%y.%m.%d %H:%M')
                                    row.insert(0,time)
                                    page_content.append(row)
                                    row = []
                                prev_origin_y = origin_y
                            row.append(table_element)    
                        counter += 1
                    yield (page_content, header)

            def _row_reader_generator(self):
                '''
                Generator for returning rows one-by-one
                '''
                for page in self.pages_files:
                    data = minidom.parse(os.path.join(self.pages_path, page))

                    # #use getElementsByTagName() to get tag
                    glyphs = data.getElementsByTagName('Glyphs')

                    # Each glyph contains a single element in the table
                    counter = 0
                    header = []
                    row = []
                    prev_origin_y = ""
                    for glyph in glyphs:
                        if counter < self.header_size[0]*self.header_size[1]:
                            if (counter+1)%self.header_size[0] == 0:
                                header.append(glyph.attributes['UnicodeString'].value)
                        else:
                            table_element = glyph.attributes['UnicodeString'].value.lstrip()
                            origin_y = glyph.attributes['OriginY'].value.lstrip()
                            if not origin_y == prev_origin_y:
                                if not counter == self.header_size[0]*self.header_size[1]:
                                    time = datetime.strptime(row.pop(), '%y.%m.%d %H:%M')
                                    row.insert(0,time)
                                    yield (row,header)
                                    row = []
                                prev_origin_y = origin_y
                            row.append(table_element) 
                        counter += 1


            def _cleanup(self):
                '''
                Cleanup function, (removes temporary files)
                '''
                if os.path.exists(self.temp_folder_path):
                    shutil.rmtree(self.temp_folder_path)

            def pages(self):
                '''
                Return a generator object to iterate through the data page-by-page
                Use it in a for loop or use the next() method to get elements
                
                Yields:
                    - page (tuple): ([row1, row2, ...], header) where row is [datetime, data1, data2, ...] and header is [head1, head2, ...]
                '''
                return self._page_gen

            def rows(self):
                '''
                Return a generator object to iterate through the data row-by-row
                Use it in a for loop or use the next() method to get elements
                
                Yields:
                    - row (tuple): ([datetime, data1, data2, ...], header) where header is [head1, head2, ...]
                '''
                return self._row_gen

        self.xps_reader_obj = XPSReaderInternal(self.file_path, self.header_size, self.temp_folder_path, self.pages_path)  # Return an XPSReaderInternal object to be used inside the "with" statement
        return self.xps_reader_obj

    def __exit__(self, exc_type, exc_value, traceback):
        '''
        Exit method, gets called whenexiting the "with" statement. DON'T USE IT DIRECTLY!
        '''
        self.xps_reader_obj._cleanup()


if __name__=='__main__':

    # Example use-cases for the XPSReader class

    # XPS filee's path:
    XPS_FILE_PATH = sys.argv[1]

    # Iterate through all the rows in the archive:
    with XPSReader(XPS_FILE_PATH) as xps:
        rows = xps.rows()
        for row, header in rows:
            # DO MAGIC WITH THE ROWS AND CORRESPONDING HEADERS HERE
            print(row)


    # Iterate through all the pages in the archive:
    with XPSReader(XPS_FILE_PATH) as xps:
        pages = xps.pages()
        for page, header in pages:
            # DO MAGIC WITH THE PAGES AND CORRESPONDING HEADERS HERE
            print(page)

    
    # Iterate through only a certain number of pages, rows:
    number_of_rows_i_want = 10
    with XPSReader(XPS_FILE_PATH) as xps:
        rows = xps.rows()
        if rows:
            for i in range(number_of_rows_i_want):
                try:
                    row, header = next(rows)
                    print(row)
                except StopIteration:
                    break

    # For random access convert either rows or pages into list. WARNING! THIS LOADS ALL OF THE DATA INTO MEMORY!
    random_row_i_want = 152
    with XPSReader(XPS_FILE_PATH) as xps:
        random_rows = list(xps.rows())
        if random_row_i_want < len(random_rows):
            random_row, random_header = random_rows[random_row_i_want]
            print(random_row)   
            
