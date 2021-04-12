import { connect } from 'react-redux';
import cornerstone from 'cornerstone-core';
import { getEnabledElement } from '../../../../extensions/cornerstone/src/state';

import { ThresholdDialog } from '@ohif/ui';
import OHIF from '@ohif/core';
import csTools from 'cornerstone-tools';
import { commandsManager } from './../App.js';
// Our target output kills the `as` and "import" throws a keyword error
// import { import as toolImport, getToolState } from 'cornerstone-tools';
import cloneDeep from 'lodash.clonedeep';
const toolImport = csTools.import;
const scrollToIndex = toolImport('util/scrollToIndex');
const { setViewportSpecificData } = OHIF.redux.actions;

// state를 해당 컴포넌트로 연결
const mapStateToProps = state => {
  // Get activeViewport's `cine` and `stack`
  const { viewportSpecificData, activeViewportIndex } = state.viewports;
  const { threshold } = viewportSpecificData[activeViewportIndex] || {};
  const dom = commandsManager.runCommand('getActiveViewportEnabledElement');

  console.log('Threshold DOM', dom);
  console.log('Current Index', activeViewportIndex);

  console.log(cornerstone.getViewport(dom).voi);

  // cornerstone.getViewport(dom).voi.windowWidth = 1400;
  let viewport = cornerstone.getViewport(dom);
  viewport.voi.windowWidth = 1400;
  viewport.voi.windowCenter = -800;
  cornerstone.setViewport(dom, viewport);

  const thresholdData = threshold || {
    // TODO: need to change the hard coded data
    thresholdLevel: 100,
    thresholdWindow: 1000,
    thresholdMinLevel: -1000,
    thresholdMaxLevel: 3000,
    thresholdMinWindow: -1000,
    thresholdMaxWindow: 3000,
  };

  // New props we're creating?
  return {
    activeEnabledElement: dom,
    activeViewportThresholdData: thresholdData,
    activeViewportIndex: state.viewports.activeViewportIndex,
  };
};

// dispatch의 함수를 props에 연결
const mapDispatchToProps = dispatch => {
  return {
    dispatchSetViewportSpecificData: (viewportIndex, data) => {
      dispatch(setViewportSpecificData(viewportIndex, data));
    },
  };
};

const mergeProps = (propsFromState, propsFromDispatch, ownProps) => {
  const {
    activeEnabledElement,
    activeViewportThresholdData,
    activeViewportIndex,
  } = propsFromState;

  return {
    thresholdLevel: activeViewportThresholdData.thresholdLevel,
    thresholdWindow: activeViewportThresholdData.thresholdWindow,
    thresholdMinLevel: activeViewportThresholdData.thresholdMinLevel,
    thresholdMaxLevel: activeViewportThresholdData.thresholdMaxLevel,
    thresholdMinWindow: activeViewportThresholdData.thresholdMinWindow,
    thresholdMaxWindow: activeViewportThresholdData.thresholdMaxWindow,
    onThresholdLevelChanged: level => {
      console.log(level, ' LEVELLL');
    },

    onAirClick: () => {
      console.log('pressed something');
    },
    onBoneClick: () => {
      console.log('pressed something');
    },
    onDPIClick: () => {
      console.log('pressed something');
    },
    onTissueClick: () => {
      console.log('pressed something');
    },
  };
};

const ConnectedThresholdDialog = connect(
  mapStateToProps,
  mapDispatchToProps,
  mergeProps
)(ThresholdDialog);

export default ConnectedThresholdDialog;
