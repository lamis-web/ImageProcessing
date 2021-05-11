# Orthanc Manager
Orthanc Server에 올려져 있는 dicom 이미지들은 localhost:8042에서 하나 씩 지워야 하는데, 이 수고를 덜어주기 위해 환자 이름, Study 이름 값만 부여해서 삭제 할 수 있게 만든 python script.

---

### requirement
```
pip install pydicom
pip install requests
pip install progress
```

### How to use
```shell
$ python3 orthanc_manager.py --help
usage: orthanc_manager.py [-h] [--patients PATIENTS [PATIENTS ...]]
                          [--studies STUDIES [STUDIES ...]]

Process some integers.

optional arguments:
  -h, --help            show this help message and exit
  --patients PATIENTS [PATIENTS ...], -p PATIENTS [PATIENTS ...]
                        get all the instances from orthanc server
  --studies STUDIES [STUDIES ...], -i STUDIES [STUDIES ...]
```