# Mushroom
Code for the mushroom detection/harvesting project

## Data reader API
The data_reader_api package provides a REST API interface for reading data for the mushroom project. Currently the XPS file reading is implemented.

### XPS Reader
The following endpoints are defined for the XPS reader:
 - xps_reader/reset:
   - PUT: expects a list of xps file names (without extension) in json format (e.g: [file1, file2, ...]) or an empty list: []. The XPS Reader objects for the listed files will be reset. If an empty list is given, all the existing XPS readers are reset.
 - xps_reader/<string:filename>:
   - GET: get all of the contents of an XPS file as a json object
   - PUT: expects a dictionary {"key":value, "key2":value2} in json format. Used to set attributes of the XPS reader objects. Example: {"header_size":[3,6]} sets the ```header_size``` attribute of the XPS reader associated with file ```filename``` to [3,6]
 - xps_reader/<string:filename>/row:
   - GET: get the next row as a json object
 - xps_reader/<string:filename>/page:
   - GET: get the next page as a json object

### Build Docker imaage
Go to folder data_reader_api
Run command: docker build --tag data-reader-api:v1.0.0 data_reader_api
Check the created image with: docker images
