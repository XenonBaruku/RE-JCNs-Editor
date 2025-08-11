bl_info = {
    "name": "RE JCNS",
    "author": "XenonValstrax",
    "blender": (2, 93, 0),
    "version": (0, 0, 1),
    "description": "Import & Export RE Engine Joint Constraints (.jcns.*) files. (Currently Work In Progress)",
    "warning": "",
    "category": "Import-Export",
}

import bpy
from bpy.types import Context, Menu, Panel, Operator

from .INTERFACE.IO import JCNS_Import, JCNS_Export
from .INTERFACE.PANELS import JCNS_IO_Panel, JCNS_PT_Constraint_Settings_Panel, JCNS_PT_ConstraintSrc_Settings_Panel
from .JCNS.JCNS_PROPERTIES import ConstraintSettings_Properties, ConstraintSrcSettings_Properties

def draw_import_menu(self: Menu, context: Context) -> None:
    self.layout.operator(JCNS_Import.bl_idname, text="RE JCNS (.jcns.*)", icon="CONSTRAINT")
def draw_export_menu(self: Menu, context: Context) -> None:
    self.layout.operator(JCNS_Export.bl_idname, text="RE JCNS (.jcns.*)", icon="CONSTRAINT")

ClassList = [
    JCNS_Import,
    JCNS_Export,
    JCNS_PT_Constraint_Settings_Panel,
    JCNS_PT_ConstraintSrc_Settings_Panel,
    ConstraintSettings_Properties,
    ConstraintSrcSettings_Properties,
]

def register() -> None:
    for _ in ClassList:
        bpy.utils.register_class(_)
    bpy.types.Object.constraint_settings = bpy.props.PointerProperty(type=ConstraintSettings_Properties)
    bpy.types.Object.constraint_src_settings = bpy.props.PointerProperty(type=ConstraintSrcSettings_Properties)
    bpy.types.TOPBAR_MT_file_import.append(draw_import_menu)
    bpy.types.TOPBAR_MT_file_export.append(draw_export_menu)
    pass

def unregister() -> None:
    for _ in ClassList:
        bpy.utils.unregister_class(_)
    bpy.types.TOPBAR_MT_file_import.remove(draw_import_menu)
    bpy.types.TOPBAR_MT_file_export.remove(draw_export_menu)
    pass

if __name__ == "__main__":
    register()