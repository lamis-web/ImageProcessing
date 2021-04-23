import os
import sys
import os.path
import httplib2
import base64
from pydicom import dcmread

if len(sys.argv) != 4:
    print("Usage: python %s [path] [username] [password]" % (
        sys.argv[0]))
    sys.exit(0)

HOST_URL = '127.0.0.1'
ORTHANC_PORT = 8042
ORTHANC_URL = 'http://%s:%d/instances' % (HOST_URL, ORTHANC_PORT)
SUCCESS_COUNT = 0
TOTAL_COUNT = 0
FAILURE_PATH = []


def UploadFile(dicom_path: str):
    """[Upload single instance of DICOM image]

    Args:
        dicom_path ([str]): [path to the single DICOM image]
    """

    global SUCCESS_COUNT
    global TOTAL_COUNT

    with open(dicom_path, 'rb') as dicom_image:
        content = dicom_image.read()
        TOTAL_COUNT += 1

        try:
            sys.stdout.write("Importing %s" % dicom_path)

            h = httplib2.Http()
            headers = {'content-type': 'application/dicom'}

            username = sys.argv[2]
            password = sys.argv[3]
            creds_str = username + ':' + password
            creds_str_bytes = creds_str.encode("ascii")
            creds_str_bytes_b64 = b'Basic ' + base64.b64encode(creds_str_bytes)
            headers['authorization'] = creds_str_bytes_b64.decode("ascii")

            response, content = h.request(
                ORTHANC_URL, 'POST', body=content, headers=headers)

            if response.status == 200:
                sys.stdout.write(" => success\n")
                SUCCESS_COUNT += 1
            else:
                sys.stdout.write(" => failure\n")
                FAILURE_PATH.append(dicom_path)

        except:
            type, value, traceback = sys.exc_info()
            sys.stderr.write(str(value))
            sys.stdout.write(" => unable to connect\n")


if __name__ == '__main__':
    # Recursively upload dcm files in a directory
    for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            file_extension = file.split('.')[-1]
            if file_extension == 'dcm' or file_extension == '':
                dicom_path = os.path.join(root, file)

                try:
                    subj_id = os.path.basename(
                        os.path.dirname(os.path.dirname(dicom_path)))
                    parent_dirname = os.path.basename(
                        os.path.dirname(dicom_path))
                    print(parent_dirname)
                    # if parent_dirname == 'Axial':
                    #     accession_number = subj_id + '_' + parent_dirname
                    # elif parent_dirname == 'Coronal':
                    #     accession_number = subj_id + '_' + parent_dirname
                    # else:
                    #     print('Wrong parent_dirname')
                    # # print(subj_id, accession_number)
                    # dicom_instance = dcmread(dicom_path)
                    # dicom_instance.PatientID = dicom_instance.PatientName = subj_id
                    # dicom_instance.AccessionNumber = accession_number
                    # dicom_instance.save_as(dicom_path)
                    UploadFile(dicom_path)
                except OSError as err:
                    sys.stdout.write("OS error: {0}".format(err))
                except:
                    sys.stdout.write("Unexpected error:", sys.exc_info()[0])

    if SUCCESS_COUNT == TOTAL_COUNT:
        print("\nSummary: all %d DICOM file(s) have been imported successfully" %
              SUCCESS_COUNT)
    else:
        print("\nSummary: %d out of %d files have been imported successfully as DICOM instances" % (
            SUCCESS_COUNT, TOTAL_COUNT))
        print("\n", FAILURE_PATH)
