import './ThresholdDialog.styl';

import React, { PureComponent } from 'react';
import { withTranslation } from '../../contextProviders';

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

  handleLevelChange = event => {
    const target = event.target;
    let value = target.value;

    const name = target.name;
    console.log([name]);

    this.setState({ [name]: value });

    if (name === 'thresholdLevel' && this.props.onThresholdLevelChanged) {
      this.props.onThresholdLevelChanged(parseInt(value));
    }
  };

  handleWindowChange = event => {
    this.setState({ thresholdWindow: event.target.value });
  };

  onAirClick = () => {
    console.log('air clicked');
    this.setState({
      thresholdLevel: -1024,
      thresholdWindow: -800,
    });
  };

  onDPIClick = () => {
    this.setState({
      thresholdLevel: -800,
      thresholdWindow: -200,
    });
  };

  onTissueClick = () => {
    this.setState({
      thresholdLevel: -250,
      thresholdWindow: 250,
    });
  };

  onBoneClick = () => {
    this.setState({
      thresholdLevel: 250,
      thresholdWindow: 3071,
    });
  };

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
            />
            <input
              className="thresholdLevelValue"
              type="text"
              value={this.state.thresholdLevel}
              onChange={this.handleWindowChange}
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
            />
            <input
              className="thresholdWindowValue"
              type="text"
              value={this.state.thresholdWindow}
              onChange={this.handleWindowChange}
            ></input>
          </div>
          <div className="threshold-content preset-content">
            <span className="thresholdPreset">Preset:</span>
            <div className="preset-button">
              <button className="btn" onClick={this.onAirClick}>
                Air
              </button>
              <button className="btn" onClick={this.onDPIClick}>
                DPI
              </button>

              <button className="btn" onClick={this.onTissueClick}>
                Tissue
              </button>
              <button className="btn" onClick={this.onBoneClick}>
                Bone
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
