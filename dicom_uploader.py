import os
import sys
import os.path
import httplib2
import base64
from pydicom import dcmread
#if len(sys.argv) != 6:
#    print("Usage: %s [hostname] [HTTP port] [path] [username] [password] ex) %s 127.0.0.1 8042 . admin password" % (sys.argv[0], sys.argv[0]))
#    sys.exit(0)

if len(sys.argv) != 4:
    print("Usage: python %s [path] [username] [password]\n  ex ) python %s . admin password" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)

URL = 'http://%s:%d/instances' % ('127.0.0.1', 8042)

success_count = 0
total_file_count = 0

# Upload a single file to Orthanc through the REST API
def UploadFile(path):
    global success_count
    global total_file_count

    with open(path, 'rb') as f:
        content = f.read()
    total_file_count += 1

    try:
        sys.stdout.write("Importing %s" % path)
        h = httplib2.Http()
        headers = { 'content-type' : 'application/dicom' }

        if len(sys.argv) == 4:
            username = sys.argv[2]
            password = sys.argv[3]
            creds_str = username + ':' + password
            creds_str_bytes = creds_str.encode("ascii")
            creds_str_bytes_b64 = b'Basic ' + base64.b64encode(creds_str_bytes)
            headers['authorization'] = creds_str_bytes_b64.decode("ascii")

        response, content = h.request(URL, 'POST', body = content, headers = headers)

        if response.status == 200:
            sys.stdout.write(" => success\n")
            success_count += 1
        else:
            sys.stdout.write(" => failure\n")

    except:
        type, value, traceback = sys.exc_info()
        sys.stderr.write(str(value))
        sys.stdout.write(" => unable to connect\n")

def construct_subj_id(dirname):
    return "TE" + "600" + dirname

# Recursively upload dcm files in a directory
for root, dirs, files in os.walk(sys.argv[1]):
    for f in files:
        ext = f.split('.')[-1]
        if ext == 'dcm' or ext == '':
          path = os.path.join(root, f)
          try:
            ds = dcmread(path)
            subj_id = os.path.basename(os.path.dirname(os.path.dirname(path)))
            ds.PatientID = ds.PatientName = subj_id
            parent_dirname = os.path.basename(os.path.dirname(path))
            if parent_dirname == 'Axial':
              accession_number = subj_id + '_' + parent_dirname
            elif parent_dirname == 'Coronal':
              accession_number = subj_id + '_' + parent_dirname
            else:
              print('Wrong parent_dirname!!!!!!!!!!!!!!!!!!!!!!')
            ds.AccessionNumber = accession_number
            #print(subj_id, accession_number)
            ds.save_as(path)
            UploadFile(path)
          except Error:
            raise Error

if success_count == total_file_count:
    print("\nSummary: all %d DICOM file(s) have been imported successfully" % success_count)
else:
    print("\nSummary: %d out of %d files have been imported successfully as DICOM instances" % (success_count, total_file_count))
