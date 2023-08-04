from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
from vtkmodules.vtkCommonColor import vtkNamedColors


# import vtkmodules.vtkInteractionStyle
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
# from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty
)
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


def buildVolumeRenderer(reader):
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
    opacityTransferFunction.AddPoint(20, 0.0)
    opacityTransferFunction.AddPoint(255, 0.2)

    # Create transfer mapping scalar value to color.
    colorTransferFunction = vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
    colorTransferFunction.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
    colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.2, 0.0)

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
    ren1.SetBackground(colors.GetColor3d('Wheat'))
    ren1.ResetCameraClippingRange()
    ren1.ResetCamera()
    return renWin
