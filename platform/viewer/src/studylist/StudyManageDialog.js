import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import FormControl from '@material-ui/core/FormControl';
import NativeSelect from '@material-ui/core/NativeSelect';
import axios from 'axios';
import StudyTable from './StudyTable';
import { mutate } from 'swr';

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  formControl: {
    color: 'white',
    marginTop: theme.spacing(0.5),
    marginLeft: theme.spacing(2),
    minWidth: 120,
  },
}));

export const StudyManageDialog = props => {
  const { open, onClose, projectList, studyDict } = props;
  const [project, setProject] = useState('Unassigned');
  const [dialog, setDialog] = useState(false);
  const classes = useStyles();

  const handleClose = event => {
    event.stopPropagation();
    onClose();
  };

  function openDialog() {
    setDialog(true);
  }

  function closeDialog() {
    setDialog(false);
  }

  return (
    <Dialog
      fullWidth
      maxWidth={'lg'}
      open={open}
      onClose={handleClose}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle id="alert-dialog-title" className={classes.root}>
        <span>Project List</span>
        <FormControl className={classes.formControl}>
          <NativeSelect
            value={project}
            onChange={e => {
              setProject(e.target.value);
            }}
            inputProps={{
              name: 'age',
              id: 'age-native-helper',
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
        <Button
          color="primary"
          size="small"
          onClick={openDialog}
          style={{ marginLeft: '2vh' }}
        >
          Create New Project
        </Button>
        <CreateNewProjectDialog dialog={dialog} closeDialog={closeDialog} />
      </DialogTitle>
      {studyDict[project] && (
        <DialogContent dividers>
          <StudyTable
            projectList={projectList}
            currentProject={project}
            studyArray={studyDict[project]}
          />
        </DialogContent>
      )}
    </Dialog>
  );
};

StudyManageDialog.propTypes = {
  open: PropTypes.bool,
  onClose: PropTypes.func,
  projectList: PropTypes.array,
  studyDict: PropTypes.object,
};

export default StudyManageDialog;

const CreateNewProjectDialog = props => {
  const { dialog, closeDialog } = props;
  const [title, setTitle] = useState('');

  const FastAPI_URL =
    process.env.NODE_ENV == 'production'
      ? process.env.PROD_FastAPI_URL
      : process.env.DEV_FastAPI_URL;

  const createNewProject = props => {
    return axios.post(FastAPI_URL + '/projects/', { title: title }).then(() => {
      mutate(FastAPI_URL + '/initgrid/');
      closeDialog();
    });
  };
  const updateTextField = event => {
    setTitle(event.target.value);
  };

  return (
    <Dialog
      open={dialog}
      onClose={closeDialog}
      aria-labelledby="form-dialog-title"
    >
      <DialogTitle id="form-dialog-title">Create New Project</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Please enter new project name you want to create.
        </DialogContentText>
        <TextField
          autoFocus
          margin="dense"
          id="project title"
          label="Project Title"
          variant="filled"
          fullWidth
          onChange={updateTextField}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={createNewProject} color="primary">
          Add
        </Button>
        <Button onClick={closeDialog} color="primary">
          Cancel
        </Button>
      </DialogActions>
    </Dialog>
  );
};

CreateNewProjectDialog.propTypes = {
  dialog: PropTypes.bool,
  closeDialog: PropTypes.func,
};
