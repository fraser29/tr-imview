import os

from trame.app import get_server
# from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vtk, vuetify#, trame
from trame_client.widgets import trame


import vtkLogic
# from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper
# # noinspection PyUnresolvedReferences
# from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLRayCastImageDisplayHelper

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
# import vtkmodules.vtkRenderingOpenGL2  # noqa

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------
reader = vtkLogic.readData(os.path.join(CURRENT_DIRECTORY, "../DATA/example.vti"))
renderWindow = vtkLogic.getVolumeRenderWindow(reader)
# renderWindow = vtkLogic.getResliceRenderWindow3(reader)


# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
server.client_type = "vue2"
state, ctrl = server.state, server.controller

state.setdefault("active_ui", None)

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# GUI elements
# -----------------------------------------------------------------------------




# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
server = get_server()
server.client_type = "vue2"
ctrl = server.controller

with SinglePageLayout(server) as layout:
    layout.title.set_text("Trame image viewer")

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            view = vtk.VtkLocalView(renderWindow)
            # view = vtk.VtkRemoteView(renderWindow)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
