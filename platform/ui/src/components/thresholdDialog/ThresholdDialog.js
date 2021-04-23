import './ThresholdDialog.styl';

import React, { PureComponent, useEffect } from 'react';
import { withTranslation } from '../../contextProviders';
import cornerstone from 'cornerstone-core';

import PropTypes from 'prop-types';

/**
 * Written by Dongha Kang.
 */
class ThresholdDialog extends PureComponent {
  constructor(props) {
    super(props);

    // TODO: needs to be fixed, {level, window / min, max}
    this.state = {
      thresholdLevel: props.thresholdLevel,
      thresholdWindow: props.thresholdWindow,
      thresholdMinLevel: props.thresholdMinLevel,
      thresholdMaxLevel: props.thresholdMaxLevel,
      thresholdMinWindow: props.thresholdMinWindow,
      thresholdMaxWindow: props.thresholdMaxWindow,
    };

    this.valueLevel = React.createRef(this.thresholdLevel);
    this.valueWindow = React.createRef(this.thresholdWindow);
    this.valueLevelManual = React.createRef(this.thresholdLevel);
    this.valueWindowManual = React.createRef(this.thresholdWindow);

    this.handleLevelChange = this.handleLevelChange.bind(this);
    this.handleWindowChange = this.handleWindowChange.bind(this);
    this.handleLevelChangeManual = this.handleLevelChangeManual.bind(this);
    this.handleWindowChangeManual = this.handleWindowChangeManual.bind(this);
  }

  static propTypes = {
    thresholdMinLevel: PropTypes.number.isRequired,
    thresholdMaxLevel: PropTypes.number.isRequired,
    thresholdMinWindow: PropTypes.number.isRequired,
    thresholdMaxWindow: PropTypes.number.isRequired,
    thresholdLevel: PropTypes.number.isRequired,
    thresholdWindow: PropTypes.number.isRequired,

    onAirClick: PropTypes.func,
    onBoneClick: PropTypes.func,
    onDPIClick: PropTypes.func,
    onTissueClick: PropTypes.func,
  };

  static defaultProps = {};

  componentDidUpdate(prevProps) {
    // if (
    //   this.props.thresholdLevel !== prevProps.thresholdLevel ||
    //   this.props.thresholdLevel !== this.state.thresholdLevel
    // ) {
    //   this.setState({
    //     thresholdLevel: this.props.thresholdLevel,
    //   });
    // }
    // if (
    //   this.props.thresholdWindow !== prevProps.thresholdWindow ||
    //   this.props.thresholdWindow !== this.state.thresholdWindow
    // ) {
    //   this.setState({
    //     thresholdWindow: this.props.thresholdWindow,
    //   });
    // }
  }

  calcLevelWindow = (min, max) => {
    let level = parseInt((min + max) / 2.0);
    let window = parseInt(max - min);

    return [level, window];
  };

  handleLevelChange = event => {
    const target = event.target;
    let value = target.value;

    const name = target.name;

    this.setState({ [name]: value });

    if (name === 'thresholdLevel' && this.props.onThresholdLevelChanged) {
      this.props.onThresholdLevelChanged(parseInt(value));
    }

    this.valueLevel.current.value = parseInt(value);
  };

  handleWindowChange = event => {
    const target = event.target;
    let value = target.value;

    const name = target.name;

    this.setState({ [name]: value });

    if (name === 'thresholdWindow' && this.props.onThresholdWindowChanged) {
      this.props.onThresholdWindowChanged(parseInt(value));
    }

    this.valueWindow.current.value = parseInt(value);
  };

  handleLevelChangeManual = event => {
    const target = event.target;
    let value = target.value;

    const name = target.name;


    this.setState({ [name]: value });

    if (name === 'thresholdLevel' && this.props.onThresholdLevelChanged) {
      this.props.onThresholdLevelChanged(parseInt(value));
    }

    this.valueLevelManual.current.value = parseInt(value);
  };

  handleWindowChangeManual = event => {
    const target = event.target;
    let value = target.value;

    const name = target.name;

    this.setState({ [name]: value });

    if (name === 'thresholdWindow' && this.props.onThresholdWindowChanged) {
      this.props.onThresholdWindowChanged(parseInt(value));
    }

    this.valueWindowManual.current.value = parseInt(value);
  };

  onLungClick = () => {
    // let val = this.calcLevelWindow(-1024, -800);
    this.onButtonClick([-500, 1500]);
  };

  onEmphysemaClick = () => {
    // let val = this.calcLevelWindow(-800, -200);
    this.onButtonClick([-700, 750]);
  };


  onButtonClick = (val) => {
    this.props.onPresetClick(val[0], val[1]);
    this.setState({
      thresholdLevel: val[0],
      thresholdWindow: val[1],
    });

    this.valueLevel.current.value = val[0]
    this.valueWindow.current.value = val[1]
    this.valueLevelManual.current.value = val[0]
    this.valueWindowManual.current.value = val[1]
  }

  render() {
    return (
      <div className="ThresholdDialog">
        <div className="noselect triple-row-style">
          <div className="threshold-content level-content">
            <label htmlFor="thresholdLevel">Level:</label>
            <input
              type="range"
              name="thresholdLevel"
              //TODO:  Needs to be fixed below
              min={this.props.thresholdMinLevel}
              max={this.props.thresholdMaxLevel}
              step={10}
              value={this.state.thresholdLevel}
              onChange={this.handleLevelChange}
              ref={this.valueLevelManual}
            />
            <input
              name="thresholdLevel"
              className="thresholdLevelValue"
              type="number"
              defaultValue={this.state.thresholdLevel}
              onChange={this.handleLevelChangeManual}
              ref={this.valueLevel}
            ></input>
          </div>
          <div className="threshold-content window-content">
            <label htmlFor="thresholdWindow">Window:</label>
            <input
              type="range"
              name="thresholdWindow"
              //TODO:  Needs to be fixed below
              min={this.props.thresholdMinWindow}
              max={this.props.thresholdMaxWindow}
              step={10}
              value={this.state.thresholdWindow}
              onChange={this.handleWindowChange}
              ref={this.valueWindowManual}
            />
            <input
              name="thresholdWindow"
              className="thresholdWindowValue"
              type="number"
              defaultValue={this.state.thresholdWindow}
              onChange={this.handleWindowChangeManual}
              ref={this.valueWindow}
            ></input>
          </div>
          <div className="threshold-content preset-content">
            <span className="thresholdPreset">Preset:</span>
            <div className="preset-button">
              <button className="btn" onClick={this.onLungClick}>
                Lung
              </button>
              <button className="btn" onClick={this.onEmphysemaClick}>
                Emphysema Narrow
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

const connectedComponent = withTranslation('ThresholdDialog')(ThresholdDialog);
export { connectedComponent as ThresholdDialog };
export default connectedComponent;
