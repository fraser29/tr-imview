from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkCommonColor import vtkNamedColors


from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
    vtkCellPicker,
    vtkProperty
)

from vtkmodules.vtkInteractionWidgets import (
    vtkResliceCursor,
    vtkResliceCursorWidget,
    vtkResliceCursorLineRepresentation,
    vtkImagePlaneWidget
)

from vtkmodules.vtkFiltersModeling import vtkOutlineFilter

from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper
# noinspection PyUnresolvedReferences
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLRayCastImageDisplayHelper

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa


def readData(fileName):
    # Read Data
    reader = vtkXMLImageDataReader()
    reader.SetFileName(fileName)
    reader.Update()
    return reader


def getVolumeRenderWindow(reader):
    # Extract Array/Field information
    dataset_arrays = []
    fields = [
        (reader.GetOutput().GetPointData(), vtkDataObject.FIELD_ASSOCIATION_POINTS),
        (reader.GetOutput().GetCellData(), vtkDataObject.FIELD_ASSOCIATION_CELLS),
    ]
    for field in fields:
        field_arrays, association = field
        for i in range(field_arrays.GetNumberOfArrays()):
            array = field_arrays.GetArray(i)
            array_range = array.GetRange()
            dataset_arrays.append(
                {
                    "text": array.GetName(),
                    "value": i,
                    "range": list(array_range),
                    "type": association,
                }
            )
    default_array = dataset_arrays[0]
    default_min, default_max = default_array.get("range")

    colors = vtkNamedColors()

    # This is a simple volume rendering example that
    # uses a vtkFixedPointVolumeRayCastMapper

    # Create the standard renderer, render window
    # and interactor.
    ren1 = vtkRenderer()

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    # iren.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

    # Create transfer mapping scalar value to opacity.
    opacityTransferFunction = vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(default_min, 0.0)
    opacityTransferFunction.AddPoint(default_max, 0.2)

    # Create transfer mapping scalar value to color.
    colorTransferFunction = vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(default_min, 0.0, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(default_max/2.0, 0.5, 0.5, 0.5)
    colorTransferFunction.AddRGBPoint(default_max, 1.0, 1.0, 1.0)

    # The property describes how the data will look.
    volumeProperty = vtkVolumeProperty()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetInterpolationTypeToLinear()

    # The mapper / ray cast function know how to render the data.
    volumeMapper = vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    # The volume holds the mapper and the property and
    # can be used to position/orient the volume.
    volume = vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    ren1.AddVolume(volume)
    ren1.SetBackground(colors.GetColor3d('WhiteSmoke'))
    ren1.ResetCameraClippingRange()
    ren1.ResetCamera()
    return renWin



def getResliceRenderWindow3(reader):
    
    
    # Reslice cursor callback
    def ResliceCursorCallback(obj,event):
        for i in range(0,3):
            ps = planeWidgetArray[i].GetPolyDataAlgorithm()
            origin = resliceCursorWidgetArray[i].GetResliceCursorRepresentation().GetPlaneSource().GetOrigin()
            ps.SetOrigin(origin)
            point1 = resliceCursorWidgetArray[i].GetResliceCursorRepresentation().GetPlaneSource().GetPoint1()
            ps.SetPoint1(point1)
            point2 = resliceCursorWidgetArray[i].GetResliceCursorRepresentation().GetPlaneSource().GetPoint2()
            ps.SetPoint2(point2)
            planeWidgetArray[i].UpdatePlacement()
    
    
    imageDims = reader.GetOutput().GetDimensions()

    # // Bounding box
    outline = vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())

    outlineMapper = vtkPolyDataMapper()
    outlineMapper.SetInputConnection(outline.GetOutputPort())

    outlineActor = vtkActor()
    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(1,1,0)

    # // Mapper and actors for volume
    volumeMapper = vtkPolyDataMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    volumeActor = vtkActor()
    volumeActor.SetMapper(volumeMapper)

    # // Renderers
    renWin = vtkRenderWindow()
    RendererArray = [None]*4
    for i in range(0,4):
        RendererArray[i] = vtkRenderer()
        renWin.AddRenderer(RendererArray[i])
    renWin.SetMultiSamples(0)

    # // Render window interactor
    iren = vtkRenderWindowInteractor()
    renWin.SetInteractor(iren)

    # // Picker
    picker = vtkCellPicker()
    picker.SetTolerance(0.005)

    # // Properties
    ipwProp = vtkProperty()

    # // 3D plane widgets
    planeWidgetArray = [None]*3
    for i in range(0,3):
        planeWidgetArray[i] = vtkImagePlaneWidget()
        planeWidgetArray[i].SetInteractor(iren)
        planeWidgetArray[i].SetPicker(picker)
        planeWidgetArray[i].RestrictPlaneToVolumeOn()
        color = [0, 0, 0 ]
        color[i] = 1
        planeWidgetArray[i].GetPlaneProperty().SetColor(color)
        planeWidgetArray[i].SetTexturePlaneProperty(ipwProp)
        planeWidgetArray[i].TextureInterpolateOff()
        planeWidgetArray[i].SetResliceInterpolateToLinear()
        planeWidgetArray[i].SetInputConnection(reader.GetOutputPort())
        planeWidgetArray[i].SetPlaneOrientation(i)
        planeWidgetArray[i].SetSliceIndex(int(imageDims[i] / 2))
        planeWidgetArray[i].DisplayTextOn()
        planeWidgetArray[i].SetDefaultRenderer(RendererArray[3])
        planeWidgetArray[i].SetWindowLevel(1358, -27, 0)
        planeWidgetArray[i].On()
        planeWidgetArray[i].InteractionOff()

    planeWidgetArray[1].SetLookupTable(planeWidgetArray[0].GetLookupTable()) 
    planeWidgetArray[2].SetLookupTable(planeWidgetArray[0].GetLookupTable())

    # // ResliceCursor
    resliceCursor = vtkResliceCursor()
    center = reader.GetOutput().GetCenter()
    resliceCursor.SetCenter(center[0], center[1], center[2])
    resliceCursor.SetThickMode(0)
    resliceCursor.SetThickness(10, 10, 10)
    resliceCursor.SetHole(0)
    resliceCursor.SetImage(reader.GetOutput())

    # // 2D Reslice cursor widgets
    resliceCursorRepArray = [None]*3
    resliceCursorWidgetArray = [None]*3
    viewUp = [[0, 0, -1],[0, 0, -1],[0, 1, 0]]
    for i in range(0,3):
        resliceCursorWidgetArray[i] = vtkResliceCursorWidget()
        resliceCursorRepArray[i] = vtkResliceCursorLineRepresentation()
        resliceCursorWidgetArray[i].SetInteractor(iren)
        resliceCursorWidgetArray[i].SetRepresentation(resliceCursorRepArray[i])
        resliceCursorRepArray[i].GetResliceCursorActor().GetCursorAlgorithm().SetResliceCursor(resliceCursor)
        resliceCursorRepArray[i].GetResliceCursorActor().GetCursorAlgorithm().SetReslicePlaneNormal(i)
        minVal = reader.GetOutput().GetScalarRange()[0]
        reslice = resliceCursorRepArray[i].GetReslice()
        reslice.SetInputConnection(reader.GetOutputPort())
        reslice.SetBackgroundColor(minVal, minVal, minVal, minVal)
        reslice.AutoCropOutputOn()
        reslice.Update()
        resliceCursorWidgetArray[i].SetDefaultRenderer(RendererArray[i])
        resliceCursorWidgetArray[i].SetEnabled(1)
        RendererArray[i].GetActiveCamera().SetFocalPoint(0, 0, 0)
        camPos = [0, 0, 0]
        camPos[i] = 1
        RendererArray[i].GetActiveCamera().SetPosition(camPos[0], camPos[1], camPos[2])
        RendererArray[i].GetActiveCamera().ParallelProjectionOn()
        RendererArray[i].GetActiveCamera().SetViewUp(viewUp[i][0], viewUp[i][1], viewUp[i][2])
        RendererArray[i].ResetCamera()
        resliceCursorWidgetArray[i].AddObserver('InteractionEvent',ResliceCursorCallback)
        range_color = reader.GetOutput().GetScalarRange()
        resliceCursorRepArray[i].SetWindowLevel(range_color[1] - range_color[0], (range_color[0] + range_color[1]) / 2.0, 0)
        planeWidgetArray[i].SetWindowLevel(range_color[1] - range_color[0], (range_color[0] + range_color[1]) / 2.0, 0)
        resliceCursorRepArray[i].SetLookupTable(resliceCursorRepArray[0].GetLookupTable())
        planeWidgetArray[i].GetColorMap().SetLookupTable(resliceCursorRepArray[0].GetLookupTable())
        
    # // Background
    RendererArray[0].SetBackground(0.3, 0.1, 0.1)
    RendererArray[1].SetBackground(0.1, 0.3, 0.1)
    RendererArray[2].SetBackground(0.1, 0.1, 0.3)
    RendererArray[3].AddActor(volumeActor)
    # RendererArray[3].AddActor(outlineActor)
    RendererArray[3].SetBackground(0.1, 0.1, 0.1)
    # renWin.SetSize(600, 600)

    # // Render
    RendererArray[0].SetViewport(0, 0, 0.5, 0.5)
    RendererArray[1].SetViewport(0.5, 0, 1, 0.5)
    RendererArray[2].SetViewport(0, 0.5, 0.5, 1)
    RendererArray[3].SetViewport(0.5, 0.5, 1, 1)
    renWin.Render()

    # // Camera in 3D view
    RendererArray[3].GetActiveCamera().Elevation(110)
    RendererArray[3].GetActiveCamera().SetViewUp(0, 0, -1)
    RendererArray[3].GetActiveCamera().Azimuth(45)
    RendererArray[3].GetActiveCamera().Dolly(1.15)
    RendererArray[3].ResetCameraClippingRange()

    iren.Initialize()
    iren.Start()
    return renWin