import React, { useState, useContext } from 'react';
import AppBar from '@material-ui/core/AppBar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Link from '@material-ui/core/Link';
import { createMuiTheme } from '@material-ui/core/styles';
import { ThemeProvider } from '@material-ui/styles';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Paper from '@material-ui/core/Paper';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import { useHistory } from 'react-router-dom';
import UserAuthContext from '../context/UserAuthContext';
import logo from '../../public/assets/android-chrome-384x384.png';

const theme = createMuiTheme({
  palette: {
    primary: {
      light: '#534bae',
      main: '#2C2C2E',
      dark: '#534bae',
      contrastText: '#fff',
    },
    secondary: {
      light: '#330e62',
      main: '#4a148c',
      dark: '#6e43a3',
      contrastText: '#fff',
    },
    dark: {
      light: '#534bae',
      main: '#000051',
      dark: '#000051',
      contrastText: '#fff',
    },
  },
});

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        lamis.life
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const useStyles = makeStyles(theme => ({
  body: {
    height: '100vh',
    backgroundColor: '#F2F2F7',
  },
  icon: {
    marginRight: theme.spacing(2),
  },
  heroContent: {
    padding: theme.spacing(16, 0, 10),
  },
  heroButtons: {
    marginTop: theme.spacing(4),
  },
  loginForm: {
    display: 'flex',
    justifyContent: 'center',
  },
  paper: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    '& > *': {
      background: 'linear-gradient(45deg, #b0bec5 30%, #cfd8dc 90%)',
      margin: theme.spacing(1.2),
      width: theme.spacing(18),
      height: theme.spacing(18),
    },
  },
  paperButton: {
    height: '100%',
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
  },
  form: {
    width: '100%', // Fix IE 11 issue.
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  invalid: {
    color: theme.palette.secondary.main,
  },
  footer: {
    padding: theme.spacing(6),
  },
}));

export default function MainPage() {
  const userAuth = useContext(UserAuthContext);
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState(null);
  const history = useHistory();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [formvalid, setFormvalid] = useState(true);

  const logout = () => {
    handleMenuClose();
    userAuth.logout();
  };

  const handleMenuClick = event => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleOhifButtonClick = () => {
    history.push('/studylist/');
  };

  const handleOrthancButtonClick = () => {
    history.push('/orthanc-admin/');
  };

  const handleCytomineButtonClick = () => {
    history.push('/cytomine/');
  };

  const handleNAS1ButtonClick = () => {
    window.location.href = 'http://210.117.213.54:64431/';
  };

  const handleNAS2ButtonClick = () => {
    window.location.href = 'http://210.117.213.54:64647/';
  };

  const handleDataTableButtonClick = () => {
    history.push('/dataTable/');
  };

  const handleSubmit = event => {
    userAuth.login(event, username, password);
  };

  return (
    <React.Fragment>
      <CssBaseline />
      <ThemeProvider theme={theme}>
        <div className={classes.body}>
          <AppBar
            position="sticky"
            color="primary"
            style={{ maxHeight: '50px' }}
          >
            <Toolbar variant="dense">
              <img
                src={logo}
                style={{
                  minHeight: '25px',
                  height: '30px',
                  paddingRight: 3,
                }}
                alt="icon"
              />
              <Typography variant="h5" color="inherit" style={{ flex: 1 }}>
                LAMIS
              </Typography>
              {userAuth.state.logged_in && (
                <Button
                  color="inherit"
                  aria-controls="simple-menu"
                  aria-haspopup="true"
                  onClick={handleMenuClick}
                >
                  {userAuth.state.username}
                </Button>
              )}
              <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
              >
                <MenuItem onClick={handleMenuClose}>Profile</MenuItem>
                <MenuItem onClick={logout}>Logout</MenuItem>
              </Menu>
              {!userAuth.state.logged_in && <span>Sign In Required</span>}
            </Toolbar>
          </AppBar>
          <main>
            {/* Hero unit */}
            <div className={classes.heroContent}>
              <Container maxWidth="sm">
                <Typography
                  component="h1"
                  variant="h2"
                  align="center"
                  color="textPrimary"
                  gutterBottom
                >
                  Pulmorad
                </Typography>
                <Typography
                  variant="h5"
                  align="center"
                  color="textSecondary"
                  paragraph
                >
                  Pulmonary Imaging Assessment
                </Typography>
                <div className={classes.heroButtons}>
                  <Grid container spacing={2} justify="center">
                    <Grid item>
                      <Button variant="contained" color="primary">
                        Get Started
                      </Button>
                    </Grid>
                    <Grid item>
                      <Button variant="outlined" color="primary">
                        GitHub
                      </Button>
                    </Grid>
                  </Grid>
                </div>
              </Container>
            </div>
            {userAuth.state.logged_in && (
              <Container component="main" maxWidth="sm">
                <div className={classes.paper}>
                  <Paper elevation={3}>
                    <div className={classes.paperButton}>
                      <Button size="medium" onClick={handleOhifButtonClick}>
                        DICOM <br /> VIEWER
                      </Button>
                    </div>
                  </Paper>
                  <Paper elevation={3}>
                    <div className={classes.paperButton}>
                      <Button size="medium" onClick={handleOrthancButtonClick}>
                        ORTHANC <br /> ADMIN
                      </Button>
                    </div>
                  </Paper>
                  <Paper elevation={3}>
                    <div className={classes.paperButton}>
                      <Button size="medium" onClick={handleCytomineButtonClick}>
                        CYTOMINE
                      </Button>
                    </div>
                  </Paper>
                </div>
                <div className={classes.paper}>
                  <Paper elevation={3}>
                    <div className={classes.paperButton}>
                      <Button size="medium" onClick={handleNAS1ButtonClick}>
                        NAS1
                      </Button>
                    </div>
                  </Paper>
                  <Paper elevation={3}>
                    <div className={classes.paperButton}>
                      <Button size="medium" onClick={handleNAS2ButtonClick}>
                        NAS2
                      </Button>
                    </div>
                  </Paper>
                  <Paper elevation={3}>
                    <div className={classes.paperButton}>
                      <Button
                        size="medium"
                        onClick={handleDataTableButtonClick}
                      >
                        Data Table
                      </Button>
                    </div>
                  </Paper>
                </div>
              </Container>
            )}
            {!userAuth.state.logged_in && (
              <Container component="main" maxWidth="xs">
                <div className={classes.loginForm}>
                  <form
                    className={classes.form}
                    method="post"
                    noValidate
                    onSubmit={e => handleSubmit(e)}
                  >
                    <TextField
                      variant="outlined"
                      margin="normal"
                      required
                      fullWidth
                      id="username"
                      label="Username"
                      name="username"
                      autoComplete="username"
                      autoFocus
                      onChange={e => setUsername(e.target.value)}
                    />
                    <TextField
                      variant="outlined"
                      margin="normal"
                      required
                      fullWidth
                      name="password"
                      label="Password"
                      type="password"
                      id="password"
                      autoComplete="current-password"
                      onChange={e => setPassword(e.target.value)}
                    />
                    <FormControlLabel
                      control={<Checkbox value="remember" color="primary" />}
                      label="Remember me"
                    />
                    {!formvalid && (
                      <div>
                        <span className={classes.invalid}>
                          * Username or Password is Invalid
                        </span>
                      </div>
                    )}
                    <Button
                      type="submit"
                      fullWidth
                      variant="contained"
                      color="secondary"
                      className={classes.submit}
                    >
                      Sign In
                    </Button>
                    <Grid container direction="column" alignItems="center">
                      <Grid item xs>
                        <Link href="#" variant="body2">
                          Forgot password?
                        </Link>
                      </Grid>
                    </Grid>
                  </form>
                </div>
              </Container>
            )}
          </main>
          {/* Footer */}
          <footer className={classes.footer}>
            <Copyright />
          </footer>
          {/* End footer */}
        </div>
      </ThemeProvider>
    </React.Fragment>
  );
}
