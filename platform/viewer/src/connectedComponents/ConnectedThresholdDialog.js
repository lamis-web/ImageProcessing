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

  // let viewport = cornerstone.getViewport(dom);
  // cornerstone.setViewport(dom, viewport);

  let thresholdData;
  try {
    // console.log(getEnabledElement(activeViewportIndex));
    // console.log(dom);
    // console.log(getEnabledElement(activeViewportIndex) === dom)
    let v = cornerstone.getViewport(dom);
    // cornerstone.setViewport(dom, viewport);
    thresholdData = threshold || {
      // TODO: need to change the hard coded data
      // thresholdLevel: 0,
      // thresholdWindow: 0,
      thresholdLevel: v.voi.windowCenter,
      thresholdWindow: v.voi.windowWidth,
      thresholdMinLevel: -2000,
      thresholdMaxLevel: 4000,
      thresholdMinWindow: 0,
      thresholdMaxWindow: 4000,
    };


  } catch {
    // // console.log("not now")
    thresholdData = threshold || {
      // TODO: need to change the hard coded data
      thresholdLevel: 0,
      thresholdWindow: 0,
      thresholdMinLevel: -2000,
      thresholdMaxLevel: 4000,
      thresholdMinWindow: 0,
      thresholdMaxWindow: 4000,
    };
    // // New props we're creating?
    // return {
    //   activeEnabledElement: dom,
    //   activeViewportThresholdData: thresholdData,
    //   activeViewportIndex: state.viewports.activeViewportIndex,
    // };
  }

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

  const dom = commandsManager.runCommand('getActiveViewportEnabledElement');
  // cornerstone.getViewport(dom).voi.windowWidth = 1400;


  return {
    thresholdLevel: activeViewportThresholdData.thresholdLevel,
    thresholdWindow: activeViewportThresholdData.thresholdWindow,
    thresholdMinLevel: activeViewportThresholdData.thresholdMinLevel,
    thresholdMaxLevel: activeViewportThresholdData.thresholdMaxLevel,
    thresholdMinWindow: activeViewportThresholdData.thresholdMinWindow,
    thresholdMaxWindow: activeViewportThresholdData.thresholdMaxWindow,
    onThresholdLevelChanged: level => {
      let viewport = cornerstone.getViewport(dom);
      viewport.voi.windowCenter = level;
      cornerstone.setViewport(dom, viewport);
    },
    onThresholdWindowChanged: window => {
      let viewport = cornerstone.getViewport(dom);
      viewport.voi.windowWidth = window;
      cornerstone.setViewport(dom, viewport);
    },

    onPresetClick: (level, window) => {
      console.log(level, window);
      let viewport = cornerstone.getViewport(dom);
      viewport.voi.windowCenter = level;
      viewport.voi.windowWidth = window;
      cornerstone.setViewport(dom, viewport);

    },
  };
};

const ConnectedThresholdDialog = connect(
  mapStateToProps,
  mapDispatchToProps,
  mergeProps
)(ThresholdDialog);

export default ConnectedThresholdDialog;
