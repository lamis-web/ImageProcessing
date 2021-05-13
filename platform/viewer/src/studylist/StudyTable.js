import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { DataGrid } from '@material-ui/data-grid';
import { Button } from '@material-ui/core';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import FormControl from '@material-ui/core/FormControl';
import NativeSelect from '@material-ui/core/NativeSelect';
import { cloneDeep } from 'lodash';
import Axios from 'axios';
import { mutate } from 'swr';

const columns = [
  { field: 'id', type: 'number', headerName: 'ID', width: 70 },
  { field: 'projectName', headerName: 'Project', width: 120 },
  { field: 'StudyInstanceUID', headerName: 'StudyInstanceUID', width: 200 },
  { field: 'PatientID', headerName: 'Patient ID', width: 200 },
  { field: 'PatientName', headerName: 'Patient Name', width: 200 },
  { field: 'modalities', headerName: 'Modalities', width: 120 },
  { field: 'StudyDate', headerName: 'Study Date', width: 130 },
  { field: 'StudyDescription', headerName: 'Study Description', width: 250 },
];

const StudyTable = props => {
  const { projectList, currentProject, studyArray } = props;
  const [rowData, setRowData] = useState([]);
  const [rowSelected, setRowSelected] = useState([]);
  const [dialog, setDialog] = useState(false);

  function constructTableData(currentProject, studyArray) {
    let tableRows = [];
    let counter = 0;
    let studyArrayClone = cloneDeep(studyArray);
    if (studyArrayClone) {
      studyArrayClone.forEach(study => {
        study['id'] = String(counter);
        study['projectName'] = currentProject;
        counter += 1;
        tableRows.push(study);
      });
    }
    return tableRows;
  }

  function openDialog() {
    setDialog(true);
  }

  function closeDialog() {
    setDialog(false);
  }

  useEffect(() => {
    setRowData(() => constructTableData(currentProject, studyArray));
  }, [currentProject, studyArray]);

  return (
    <div style={{ height: '60vh', width: '100%' }}>
      <div style={{ height: '90%' }}>
        <DataGrid
          rows={rowData}
          columns={columns}
          pageSize={10}
          checkboxSelection
          selectionModel={rowSelected}
          onSelectionModelChange={row => {
            setRowSelected(row.selectionModel);
          }}
        />
      </div>
      <div style={{ height: '10%' }}>
        <Button onClick={openDialog}>Add To Project</Button>
        <AddToProjectDialog
          projectList={projectList}
          dialog={dialog}
          closeDialog={closeDialog}
          studyArray={studyArray}
          rowSelected={rowSelected}
        />
      </div>
    </div>
  );
};

StudyTable.propTypes = {
  projectList: PropTypes.array.isRequired,
  currentProject: PropTypes.string.isRequired,
  studyArray: PropTypes.array.isRequired,
};

const AddToProjectDialog = props => {
  const { projectList, dialog, closeDialog, studyArray, rowSelected } = props;
  const [project, setProject] = useState('Unassigned');

  const FastAPI_URL =
    process.env.NODE_ENV == 'production'
      ? process.env.PROD_FastAPI_URL
      : process.env.DEV_FastAPI_URL;

  function constructStudyObject(study) {
    const studyClone = cloneDeep(study);

    studyClone['id'] = 0;
    studyClone['project_title'] = project;

    if (!('StudyInstanceUID' in studyClone)) {
      // console.error('StudyInstanceUID does not exist');
      studyClone['instance_uid'] = null;
    } else {
      studyClone['instance_uid'] = studyClone['StudyInstanceUID'];
      delete studyClone['StudyInstanceUID'];
    }
    if (studyClone['AccessionNumber'] === undefined) {
      // console.error('AccessionNumber does not exist');
      studyClone['access_number'] = null;
    } else {
      studyClone['access_number'] = studyClone['AccessionNumber'];
      delete studyClone['AccessionNumber'];
    }
    if (!('PatientID' in studyClone)) {
      // console.error('PatientID does not exist');
      studyClone['patient_id'] = null;
    } else {
      studyClone['patient_id'] = studyClone['PatientID'];
      delete studyClone['PatientID'];
    }
    if (!('PatientName' in studyClone)) {
      // console.error('PatientName does not exist');
      studyClone['patient_name'] = null;
    } else {
      studyClone['patient_name'] = studyClone['PatientName'];
      delete studyClone['PatientName'];
    }
    if (!('StudyDate' in studyClone)) {
      // console.error('StudyDate does not exist');
      studyClone['study_date'] = null;
    } else {
      studyClone['study_date'] = studyClone['StudyDate'];
      delete studyClone['StudyDate'];
    }
    if (!('StudyDescription' in studyClone)) {
      // console.error('StudyDescription does not exist');
      studyClone['study_description'] = null;
    } else {
      studyClone['study_description'] = studyClone['StudyDescription'];
      delete studyClone['StudyDescription'];
    }
    if (!('modalities' in studyClone)) {
      // console.error('modalities does not exist');
      studyClone['modalities'] = null;
    } else {
      studyClone['modalities'] = studyClone['modalities'].replace(
        String.fromCharCode(92),
        '/'
      );
    }
    return studyClone;
  }

  function constructStudiesToAdd() {
    let rowToAdd = [];
    rowSelected.forEach(index => {
      const study = constructStudyObject(studyArray[index]);
      rowToAdd.push(study);
    });
    return rowToAdd;
  }

  const addToProject = () => {
    const studiesToAdd = constructStudiesToAdd();
    Axios.post(FastAPI_URL + '/studies/', studiesToAdd).then(() => {
      mutate(FastAPI_URL + '/initgrid/');
      closeDialog();
    });
  };

  return (
    <Dialog
      open={dialog}
      onClose={closeDialog}
      aria-labelledby="form-dialog-title"
    >
      <DialogTitle id="form-dialog-title">Add to Project</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Please choose a project to add selected studies.
        </DialogContentText>
        <FormControl>
          <NativeSelect
            value={project}
            onChange={e => {
              setProject(e.target.value);
            }}
            style={{ color: 'black' }}
          >
            <option key={'unassigined'}>Unassigned</option>
            {projectList &&
              projectList.map(project => (
                <option key={project.title}>{project.title}</option>
              ))}
          </NativeSelect>
        </FormControl>
      </DialogContent>
      <DialogActions>
        {project !== 'Unassigned' && (
          <Button onClick={addToProject} color="primary">
            Add
          </Button>
        )}
        <Button onClick={closeDialog} color="primary">
          Cancel
        </Button>
      </DialogActions>
    </Dialog>
  );
};

AddToProjectDialog.propTypes = {
  projectList: PropTypes.array.isRequired,
  dialog: PropTypes.bool.isRequired,
  closeDialog: PropTypes.func.isRequired,
  studyArray: PropTypes.array.isRequired,
  rowSelected: PropTypes.array.isRequired,
};

export default StudyTable;
