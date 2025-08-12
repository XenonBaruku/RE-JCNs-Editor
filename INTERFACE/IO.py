import bpy

from .PANELS import JCNS_IO_Panel
from bpy.types import Panel
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty, PointerProperty
from bpy.types import Operator, OperatorFileListElement, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper

from ..JCNS.JCNS_IO import ImportJCNSFile
from ..JCNS.EXCEPTIONS import ERROR_NotImplemented

import os

class JCNS_Import(bpy.types.Operator, ImportHelper):
    '''Import RE Engine Joint Constraints File'''
    bl_idname = "jcns.import"
    bl_label = 'Import JCNS'
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = "*.jcns.*"
    filter_glob: StringProperty(
        default="*.jcns.*", 
        options={"HIDDEN"}, 
        maxlen=255
    ) 
    files: CollectionProperty( 
        name="File Path", 
        type=OperatorFileListElement
    ) 
    armature: StringProperty( 
        name="", 
        description = "Set the armature that JCNS relys.\nThis is optional for some types of JCNS, and can be set later."
    ) 
    apply_settings: BoolProperty( 
        name="Apply Constraints (Not implemented)", 
        description = "Apply constraint settings as blender constraints on armature.\nNote that Blender constraints CANNOT be exported to a JCNS file. Please check the \"Import JCNS data\" option below instead of this if you'd like to edit a JCNS file.\nThis setting affects armature. Please make sure this won't cause any mess.",
        default=True
    ) 
    import_data: BoolProperty(
        name="Import JCNS data", 
        description = "Import editable JCNS data. These data are required while exporting.\nIt is recommended to leave this option enabled.",
        default=True
    ) 
    ignore_references: BoolProperty(
        name="Force Import All Constraints", 
        description = "For JCNS version >= 21, there's an area that stores constraint references. Only constrints referenced there works in game. \nSometimes there might be more constraints in file but aren't referenced (or not referenced properly). \nEnabling this would ignore the reference infos and force import all constraints found in file.",
    ) 
    debug_mode: BoolProperty( 
        name="Show debug info", 
        default=True
    ) 
    
    def draw(self, context) -> None:
        JCNS_IO_Panel.draw_general_options(self, import_menu=True)
        JCNS_IO_Panel.draw_advanced_options(self, import_menu=True)

        try:
            if bpy.data.armatures.get(bpy.context.object.name):
                self.armature = bpy.context.object.name
        except:
            pass

    def execute(self, context) -> None:
        options = {
            "armature": self.armature, 
            "apply_settings": self.apply_settings, 
            "import_data": self.import_data, 
            "ignore_references": self.ignore_references,
            "debug_mode": self.debug_mode,
        }
        if self.files:
            folder = (os.path.dirname(self.filepath))
            filepaths = [os.path.join(folder, file.name) for file in self.files]
        else:
            filepaths = [str(self.filepath)]

        for filepath in filepaths:
            if options["debug_mode"] == True:
                _ = ImportJCNSFile(filepath, options, collection=None)
                continue
            try:
                _ = ImportJCNSFile(filepath, options, collection=None)
            except Exception as e:
                self.report({"ERROR"}, "Failed to load file {}: {}".format(str(filepath), str(e)))
                return {"CANCELLED"}
        return {"FINISHED"}
    
class JCNS_Export(bpy.types.Operator, ExportHelper):
    '''Export to RE Engine Joint Constraints File'''
    bl_idname = "jcns.export"
    bl_label = 'Export JCNS'
    bl_options = {'PRESET'}

    filter_glob: StringProperty(default="*.jcns*", options={'HIDDEN'})

    filename_ext: EnumProperty(
		name="Game",
		description="Set which game to export the jcns for",
		items= [
                (".11", "Resident Evil 2 Remake", "Resident Evil 2 Remake"),
                (".12", "Resident Evil 3 Remake", "Resident Evil 3 Remake"),
				(".16", "Resident Evil 8", "Resident Evil 8"),
                (".21", "Monster Hunter Rise", "Monster Hunter Rise"),
                (".22", "Resident Evil 4 Remake", "Resident Evil 4 Remake"),
				(".29", "Monster Hunter Wilds", "Monster Hunter Wilds"),
			   ]
		) 
    targetCollection: bpy.props.StringProperty(
        name="",
        description = "Set the JCNS collection to be exported.\nNote: JCNS collections are usually green and end with .jcns",
    ) 
    
    def draw(self, context) -> None:
        JCNS_IO_Panel.draw_general_options(self)
        JCNS_IO_Panel.draw_advanced_options(self)

    def execute(self, context) -> None:
        raise ERROR_NotImplemented