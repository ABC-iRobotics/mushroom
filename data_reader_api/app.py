from flask import Flask, make_response, jsonify, request
from flask_restful import Resource, Api, reqparse
import datetime
import os

from xps_reader.api import XPSReader

app = Flask(__name__, template_folder='template')
api = Api(app)

DATA_FOLDER = '/data'
XPS_READERS = []

def get_xps_reader(filename):
    global XPS_READERS
    xpsr = None
    for xps_reader in XPS_READERS:
        if xps_reader.file_path == os.path.join(DATA_FOLDER, 'xps_files', filename) + '.xps':
            xpsr = xps_reader
            break
    return xpsr
    
def process_xps_data(rows):
    document = {'rows':[]}
    for row in rows:
        data_row = {}
        data = row[0]
        header = row[1]
        data_row['date'] = data[0]
        for i in range(len(header)):
            data_row[header_formatter(header[i])] = data[i+1]
        document['rows'].append(data_row)
    return document
    
def header_formatter(header_name):
    modified_header = header_name.lower()
    modified_header = modified_header.replace(" ", "_")
    return modified_header

class XPSReadersReset(Resource):
    def put(self):
        global XPS_READERS
        json_data = request.get_json(force=True)
        headers = {'Content-Type': 'application/json'}
        if type(json_data) == type([]):
            if json_data:
                for filename in json_data:
                    for xps_reader in XPS_READERS:
                        if xps_reader.file_path == os.path.join(DATA_FOLDER, 'xps_files', filename) + '.xps':
                            if hasattr(xps_reader, 'xps_reader_obj'):
                                xps_reader.__exit__(None,None,None)
                                del xps_reader.xps_reader_obj
            else:
                for xps_reader in XPS_READERS:
                    if hasattr(xps_reader, 'xps_reader_obj'):
                        xps_reader.__exit__(None,None,None)
                        del xps_reader.xps_reader_obj
            return make_response('',200,headers)
        else:
            return make_response('The request content must be a list of filenames: ["filename1", filename2, ...] or an empty list []',400,headers)

class XPSReaderGetAll(Resource):
    def get(self, filename):
        global XPS_READERS
        headers = {'Content-Type': 'application/json'}
        xps_reader = get_xps_reader(filename)
        try:
            if xps_reader != None:
                with XPSReader((os.path.join(DATA_FOLDER,'xps_files',filename))+'.xps', header_size=xps_reader.header_size, temp_folder_path=filename+'_temp_all') as xps:
                    rows = process_xps_data(xps.rows())
            else:
                xps_reader = XPSReader(os.path.join(DATA_FOLDER, 'xps_files', filename) + '.xps', temp_folder_path=filename+'_temp')
                XPS_READERS.append(xps_reader)
                with XPSReader((os.path.join(DATA_FOLDER,'xps_files',filename))+'.xps', temp_folder_path=filename+'_temp_all') as xps:
                    rows = process_xps_data(xps.rows())
        except FileNotFoundError:
            return make_response('The requested file: ' + filename + '.xps does not exist',404,headers)
        except ValueError:
            return make_response('The header of file: ' + filename + '.xps has different format, use PUT to set the correct header size!',500,headers)
        return make_response(jsonify(rows),200,headers)

    def put(self, filename):
        global XPS_READERS
        json_data = request.get_json(force=True)
        headers = {'Content-Type': 'application/json'}
        for xps_reader in XPS_READERS:
            if xps_reader.file_path == os.path.join(DATA_FOLDER, 'xps_files', filename) + '.xps':
                if 'header_size' in [k for k in json_data.keys()]:
                    xps_reader.header_size = json_data['header_size']
                if 'temp_folder_path' in [k for k in json_data.keys()]:
                    xps_reader.temp_folder_path = json_data['temp_folder_path']
                if hasattr(xps_reader, 'xps_reader_obj'):
                    xps_reader.__exit__(None,None,None)
                    del xps_reader.xps_reader_obj
        return make_response('',200,headers)


class XPSReaderGetRow(Resource):
    def get(self, filename):
        global XPS_READERS
        headers = {'Content-Type': 'application/json'}
        xps_reader = get_xps_reader(filename)
        if xps_reader == None:
            xps_reader = XPSReader(os.path.join(DATA_FOLDER, 'xps_files', filename) + '.xps', temp_folder_path=filename+'_temp')
            XPS_READERS.append(xps_reader)
        if hasattr(xps_reader, 'xps_reader_obj'):
            try:
                return make_response(jsonify(next(xps_reader.xps_reader_obj.rows())),200,headers)
            except StopIteration:
                try:
                    xps_reader.__enter__()
                    return make_response(jsonify(next(xps_reader.xps_reader_obj.rows())),200,headers)
                except FileNotFoundError:
                    return make_response('The requested file: ' + filename + '.xps does not exist',404,headers)
                except ValueError:
                    return make_response('The header of file: ' + filename + '.xps has different format, use PUT to set the correct header size!',500,headers)
        else:
            try:
                xps_reader.__enter__()
                return make_response(jsonify(next(xps_reader.xps_reader_obj.rows())),200,headers)
            except FileNotFoundError:
                return make_response('The requested file: ' + filename + '.xps does not exist',404,headers)
            except ValueError:
                return make_response('The header of file: ' + filename + '.xps has different format, use PUT to set the correct header size!',500,headers)
        

class XPSReaderGetPage(Resource):
    def get(self, filename):
        global XPS_READERS
        headers = {'Content-Type': 'application/json'}
        xps_reader = get_xps_reader(filename)
        if xps_reader == None:
            xps_reader = XPSReader(os.path.join(DATA_FOLDER, 'xps_files', filename) + '.xps', temp_folder_path=filename+'_temp')
            XPS_READERS.append(xps_reader)
        if hasattr(xps_reader, 'xps_reader_obj'):
            try:
                return make_response(jsonify(next(xps_reader.xps_reader_obj.pages())),200,headers)
            except StopIteration:
                try:
                    xps_reader.__enter__()
                    return make_response(jsonify(next(xps_reader.xps_reader_obj.pages())),200,headers)
                except FileNotFoundError:
                    return make_response('The requested file: ' + filename + '.xps does not exist',404,headers)
                except ValueError:
                    return make_response('The header of file: ' + filename + '.xps has different format, use PUT to set the correct header size!',500,headers)
        else:
            try:
                xps_reader.__enter__()
                return make_response(jsonify(next(xps_reader.xps_reader_obj.pages())),200,headers)
            except FileNotFoundError:
                return make_response('The requested file: ' + filename + '.xps does not exist',404,headers)
            except ValueError:
                return make_response('The header of file: ' + filename + '.xps has different format, use PUT to set the correct header size!',500,headers)


if __name__ == '__main__':
    api.add_resource(XPSReadersReset, '/xps_reader/reset')
    api.add_resource(XPSReaderGetAll, '/xps_reader/<string:filename>')
    api.add_resource(XPSReaderGetRow, '/xps_reader/<string:filename>/row')
    api.add_resource(XPSReaderGetPage, '/xps_reader/<string:filename>/page')
    app.run(host='0.0.0.0', port=5000, debug=True)