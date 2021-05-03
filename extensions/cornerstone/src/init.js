import OHIF from '@ohif/core';
import { SimpleDialog } from '@ohif/ui';
import cornerstone from 'cornerstone-core';
import csTools from 'cornerstone-tools';
import { cornerstoneWADOImageLoader } from 'cornerstone-wado-image-loader';
import merge from 'lodash.merge';
import initCornerstoneTools from './initCornerstoneTools.js';
import measurementServiceMappingsFactory from './utils/measurementServiceMappings/measurementServiceMappingsFactory';

/**
 *  Also, Modified by Dongha Kang
 *
 * @param {Object} servicesManager
 * @param {Object} configuration
 * @param {Object|Array} configuration.csToolsConfig
 */
export default function init({ servicesManager, configuration }) {
  const { UIDialogService, MeasurementService } = servicesManager.services;
  // - Annotation을 넣을때, UI. 작동 안됨.
  // const callInputDialog = (data, event, callback) => {
  //   if (UIDialogService) {
  //     let dialogId = UIDialogService.create({
  //       centralize: true,
  //       isDraggable: false,
  //       content: SimpleDialog.InputDialog,
  //       useLastPosition: false,
  //       showOverlay: true,
  //       contentProps: {
  //         title: 'Enter your annotation',
  //         label: 'New label',
  //         measurementData: data ? { description: data.text } : {},
  //         onClose: () => {
  //           UIDialogService.dismiss({ id: dialogId });
  //         },
  //         onSubmit: value => {
  //           callback(value);
  //           UIDialogService.dismiss({ id: dialogId });

  //           console.log(data);
  //           console.log('init.js, dialogID: ' + dialogId);
  //         },
  //       },
  //     });
  //   }
  // };

  const { csToolsConfig } = configuration;
  const metadataProvider = OHIF.cornerstone.metadataProvider;

  cornerstone.metaData.addProvider(
    metadataProvider.get.bind(metadataProvider),
    9999
  );

  // ~~
  const defaultCsToolsConfig = csToolsConfig || {
    globalToolSyncEnabled: true,
    showSVGCursors: true,
    autoResizeViewports: false,
  };

  // Initialize cornerstone tools here
  initCornerstoneTools(defaultCsToolsConfig);

  // --> able to analyze csTools like this. csTools.ArrowAnnotateTool.name
  console.log(csTools.ArrowAnnotateTool)

  const toolsGroupedByType = {
    touch: [csTools.PanMultiTouchTool, csTools.ZoomTouchPinchTool],
    annotations: [
      csTools.ArrowAnnotateTool,
      csTools.BidirectionalTool,
      csTools.LengthTool,
      csTools.AngleTool,
      csTools.FreehandRoiTool,
      csTools.EllipticalRoiTool,
      csTools.DragProbeTool,
      csTools.RectangleRoiTool,
    ],
    other: [
      csTools.PanTool,
      csTools.ZoomTool,
      csTools.WwwcTool,
      csTools.WwwcRegionTool,
      csTools.MagnifyTool,
      csTools.StackScrollTool,
      csTools.StackScrollMouseWheelTool,
      csTools.OverlayTool,
    ],
  };

  let tools = [];
  Object.keys(toolsGroupedByType).forEach(toolsGroup =>
    tools.push(...toolsGroupedByType[toolsGroup])
  );

  /* Measurement Service */
  _connectToolsToMeasurementService(MeasurementService);

  /* Add extension tools configuration here. */
  const internalToolsConfig = {
    //   // TODO: Error occurred from here, This will unable the UIDialogService
    // ArrowAnnotate: {
    // configuration: {
    //   getTextCallback: (callback, eventDetails) =>
    //     callInputDialog(null, eventDetails, callback),
    //   changeTextCallback: (data, eventDetails, callback) =>
    //     callInputDialog(data, eventDetails, callback),
    // },
    // },
  };

  /* Abstract tools configuration using extension configuration. */
  const parseToolProps = (props, tool) => {
    const { annotations } = toolsGroupedByType;
    // An alternative approach would be to remove the `drawHandlesOnHover` config
    // from the supported configuration properties in `cornerstone-tools`
    const toolsWithHideableHandles = annotations.filter(
      tool => !['RectangleRoiTool', 'EllipticalRoiTool'].includes(tool.name)
    );

    let parsedProps = { ...props };

    /**
     * drawHandles - Never/Always show handles
     * drawHandlesOnHover - Only show handles on handle hover (pointNearHandle)
     *
     * Does not apply to tools where handles aren't placed in predictable
     * locations.
     */
    if (
      configuration.hideHandles !== false &&
      toolsWithHideableHandles.includes(tool)
    ) {
      if (props.configuration) {
        parsedProps.configuration.drawHandlesOnHover = true;
      } else {
        parsedProps.configuration = { drawHandlesOnHover: true };
      }
    }

    return parsedProps;
  };

  /* Add tools with its custom props through extension configuration. */
  tools.forEach(tool => {
    const toolName = tool.name.replace('Tool', '');
    const externalToolsConfig = configuration.tools || {};
    const externalToolProps = externalToolsConfig[toolName] || {};
    const internalToolProps = internalToolsConfig[toolName] || {};
    const props = merge(
      internalToolProps,
      parseToolProps(externalToolProps, tool)
    );
    csTools.addTool(tool, props);
  });

  // TODO -> We need a better way to do this with maybe global tool state setting all tools passive.
  const BaseAnnotationTool = csTools.importInternal('base/BaseAnnotationTool');
  tools.forEach(tool => {
    if (tool.prototype instanceof BaseAnnotationTool) {
      // BaseAnnotationTool would likely come from csTools lib exports
      const toolName = new tool().name;
      csTools.setToolPassive(toolName); // there may be a better place to determine name; may not be on uninstantiated class
    }
  });

  csTools.setToolActive('Pan', { mouseButtonMask: 4 });
  csTools.setToolActive('Zoom', { mouseButtonMask: 2 });
  csTools.setToolPassive('Wwwc', { mouseButtonMask: 1 });
  csTools.setToolActive('StackScrollMouseWheel', {}); // TODO: Empty options should not be required
  csTools.setToolActive('PanMultiTouch', { pointers: 2 }); // TODO: Better error if no options
  csTools.setToolActive('ZoomTouchPinch', {});
  csTools.setToolEnabled('Overlay', {});
}

const _initMeasurementService = measurementService => {
  /* Initialization */
  const { toAnnotation, toMeasurement } = measurementServiceMappingsFactory(
    measurementService
  );
  const csToolsVer4MeasurementSource = measurementService.createSource(
    'CornerstoneTools',
    '4'
  );

  /* Matching Criterias */
  const matchingCriteria = {
    valueType: measurementService.VALUE_TYPES.POLYLINE,
    points: 2,
  };

  const matchingCriteriaAngle = {
    valueType: measurementService.VALUE_TYPES.POLYLINE,
    points: 3,
  };

  /* Mappings */
  measurementService.addMapping(
    csToolsVer4MeasurementSource,
    'Length',
    matchingCriteria,
    toAnnotation,
    toMeasurement
  );

  // Dongha Kang
  // -- added to avoid the warnings that saying
  // `Failed to map '${sourceInfo}' measurement for definition ${definition}:`,
  measurementService.addMapping(
    csToolsVer4MeasurementSource,
    'ArrowAnnotate',
    matchingCriteria,
    toAnnotation,
    toMeasurement
  );

  measurementService.addMapping(
    csToolsVer4MeasurementSource,
    'Angle',
    matchingCriteriaAngle,
    toAnnotation,
    toMeasurement
  );

  measurementService.addMapping(
    csToolsVer4MeasurementSource,
    'stack',
    matchingCriteria,
    toAnnotation,
    toMeasurement
  );

  measurementService.addMapping(
    csToolsVer4MeasurementSource,
    'stackPrefetch',
    matchingCriteria,
    toAnnotation,
    toMeasurement
  );

  return csToolsVer4MeasurementSource;
};

// TODO: 여기가 아마도 annotation 과 관련되 데이터들
const _connectToolsToMeasurementService = measurementService => {
  const csToolsVer4MeasurementSource = _initMeasurementService(
    measurementService
  );
  const {
    id: sourceId,
    addOrUpdate,
    getAnnotation,
  } = csToolsVer4MeasurementSource;

  /* Measurement Service Events */
  cornerstone.events.addEventListener(
    cornerstone.EVENTS.ELEMENT_ENABLED,
    event => {
      const {
        MEASUREMENT_ADDED,
        MEASUREMENT_UPDATED,
      } = measurementService.EVENTS;

      measurementService.subscribe(
        MEASUREMENT_ADDED,
        ({ source, measurement }) => {
          if (![sourceId].includes(source.id)) {
            const annotation = getAnnotation('Length', measurement.id);

            console.log(
              'Measurement Service [Cornerstone]: Measurement added',
              measurement
            );
            console.log('Mapped annotation:', annotation);
          }
        }
      );

      measurementService.subscribe(
        MEASUREMENT_UPDATED,
        ({ source, measurement }) => {
          if (![sourceId].includes(source.id)) {
            const annotation = getAnnotation('Length', measurement.id);

            console.log(
              'Measurement Service [Cornerstone]: Measurement updated',
              measurement
            );
            console.log('Mapped annotation:', annotation);
          }
        }
      );

      // MARK: 여기가 annotation을 등록, 그 후 움직일때 일어나는 코드
      const addOrUpdateMeasurement = csToolsAnnotation => {
        try {
          const { toolName, toolType, measurementData } = csToolsAnnotation;
          const csTool = toolName || measurementData.toolType || toolType;
          csToolsAnnotation.id = measurementData._measurementServiceId;
          const measurementServiceId = addOrUpdate(csTool, csToolsAnnotation);

          if (!measurementData._measurementServiceId) {
            addMeasurementServiceId(measurementServiceId, csToolsAnnotation);
          }
        } catch (error) {
          console.warn('Failed to add or update measurement:', error);
        }
      };

      const addMeasurementServiceId = (id, csToolsAnnotation) => {
        const { measurementData } = csToolsAnnotation;
        Object.assign(measurementData, { _measurementServiceId: id });
      };

      [
        csTools.EVENTS.MEASUREMENT_ADDED,
        csTools.EVENTS.MEASUREMENT_MODIFIED,
      ].forEach(csToolsEvtName => {
        event.detail.element.addEventListener(
          csToolsEvtName,
          ({ detail: csToolsAnnotation }) => {
            console.log(`Cornerstone Element Event: ${csToolsEvtName}`);
            addOrUpdateMeasurement(csToolsAnnotation);
          }
        );
      });
    }
  );
};
