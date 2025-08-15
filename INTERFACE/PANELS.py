import bpy
from bpy.types import Panel
from bpy.types import Operator


class JCNS_IO_Panel:
    @staticmethod
    def draw_general_options(panel: Panel | Operator, /, *, import_menu: bool = False) -> None:
        layout = panel.layout
        box = panel.layout.box()
        #row = box.row()
        box.label(text="Settings", icon="SETTINGS")
        if not import_menu:
            box.row().prop(panel, "filename_ext")
            box.row().label(text="Collection: ")
            #box.row().prop_search(panel, "targetCollection", bpy.context.collection, "collections")
            box.row().prop(panel, "targetCollection")

            if panel.targetCollection in bpy.data.collections:
                collection = bpy.data.collections[panel.targetCollection]
                if not collection.get("~TYPE") == "RE_JCNS_COLLECTION" and not collection.name.endswith(".jcns"):
                    row = box.row()
                    row.alert=True
                    row.label(icon = "ERROR",text="Collection is not a jcns collection.")
            elif panel.targetCollection == "":
                row = box.row()
                row.alert=True
                row.label(icon = "ERROR",text="Collection is not a jcns collection.")
            else:
                row = layout.row()
                row.label(icon="ERROR",text="Chosen collection doesn't exist.")
                row.alert=True

        if import_menu:
            box.row().label(text="Armature (Optional): ")
            box.row().prop_search(panel, "armature", bpy.context.scene, "objects", text="")
            box.row().prop(panel, "apply_settings")
            box.row().prop(panel, "import_data")
            box.row().label()

    def draw_advanced_options(panel: Panel | Operator, /, *, import_menu: bool = False) -> None:
        box = panel.layout.box()
        #row = box.row()
        box.label(text="Advanced", icon="FILE_CACHE")

        if import_menu:
            box.row().prop(panel, "ignore_references")
            box.row().prop(panel, "debug_mode")
        
        

class JCNS_PT_Constraint_Settings_Panel(Panel):
    bl_label = "JCNS Constraint Settings"
    bl_idname = "JCNS_PT_Constraint_Settings_Panel"
    bl_space_type = "PROPERTIES"   
    bl_region_type = "WINDOW"
    bl_category = "JCNS Constraint Settings"
    bl_context = "object"

    @classmethod
    def poll(self,context):
        return context and context.object.mode == "OBJECT" and context.active_object and context.active_object.get("TYPE",None) == "JCNS_ConstraintSettings"

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        constraint_settings = object.constraint_settings
        
        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment='CENTER'
        col2.use_property_split = True
        col2.prop(constraint_settings, "Type")
        if int(constraint_settings.Type) == 0:
            col2.prop_search(constraint_settings, "ArmatureName", context.scene, "objects")
            armature = bpy.data.armatures.get(constraint_settings.ArmatureName)
            if (not armature) or armature == "":
                col2.label(icon = "ERROR",text="Invalid armature.")
            bone = None
            try:
                if armature:
                    col2.prop_search(constraint_settings, "BoneName", armature, "bones")
                    bone = bpy.data.armatures.get(constraint_settings.ArmatureName).bones[constraint_settings.BoneName]
            except:
                pass
            if (not bone) or bone == "":
                col2.prop(constraint_settings, "Name")
                if armature and armature != "":
                    col2.label(icon = "ERROR",text="Couldn't found specified bone in armature.")
        elif int(constraint_settings.Type) == 1:
            col2.prop(constraint_settings, "Name")
            col2.prop(constraint_settings, "Property")
        else:
            col2.prop(constraint_settings, "Name")
        col2.separator()
        col2.prop(constraint_settings, "TransformationType")
        col2.prop(constraint_settings, "TransformationAxis")
        col2.separator()
        col2.prop(constraint_settings, "UNKNOWN_1")
        col2.prop(constraint_settings, "UNKNOWN_2")
        col2.prop(constraint_settings, "UNKNOWN_3")
        col2.prop(constraint_settings, "UNKNOWN_4")
        col2.separator()
        col2.prop(constraint_settings, "UNKNOWN_5")

class JCNS_PT_Constraint_Extra_Info_Panel(Panel):
    bl_label = "JCNS Constraint Extra Info"
    bl_idname = "JCNS_PT_Constraint_Extra_Info_Panel"
    bl_space_type = "PROPERTIES"   
    bl_region_type = "WINDOW"
    bl_category = "JCNS Constraint Extra Info"
    bl_context = "object"

    @classmethod
    def poll(self,context):
        return context and context.object.mode == "OBJECT" and context.active_object and context.active_object.get("TYPE",None) == "JCNS_ConstraintExtraInfo"

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        constraint_extra_info = object.constraint_extra_info
        
        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment='CENTER'
        col2.use_property_split = True
        col2.prop(constraint_extra_info, "UNKNOWN_1")
        col2.prop(constraint_extra_info, "UNKNOWN_2")
        col2.separator()
        col2.prop(constraint_extra_info, "UNKNOWN_3")
        col2.prop(constraint_extra_info, "UNKNOWN_4")
        col2.prop(constraint_extra_info, "UNKNOWN_5")
        col2.prop(constraint_extra_info, "UNKNOWN_6")

class JCNS_PT_ConstraintSrc_Settings_Panel(Panel):
    bl_label = "JCNS Constraint Source Settings"
    bl_idname = "JCNS_PT_ConstraintSrc_Settings_Panel"
    bl_space_type = "PROPERTIES"   
    bl_region_type = "WINDOW"
    bl_category = "JCNS Constraint Source Settings"
    bl_context = "object"

    @classmethod
    def poll(self,context):
        return context and context.object.mode == "OBJECT" and context.active_object and context.active_object.get("TYPE",None) == "JCNS_ConstraintSrcSettings"

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        constraint_src_settings = object.constraint_src_settings
        
        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment='CENTER'
        col2.use_property_split = True
        col2.prop(constraint_src_settings, "Type")
        if int(constraint_src_settings.Type) == 0:
            armature = bpy.data.armatures.get(constraint_src_settings.ArmatureName)
            if (not armature) or armature == "":
                col2.label(icon = "ERROR",text="Invalid armature.")
            bone = None
            try:
                if armature:
                    col2.prop_search(constraint_src_settings, "BoneName", armature, "bones")
                    bone = bpy.data.armatures.get(constraint_src_settings.ArmatureName).bones[constraint_src_settings.BoneName]
                else:
                    col2.label(icon = "ERROR",text="Constraint armature is not set.")
            except:
                pass
            if (not bone) or bone == "":
                col2.prop(constraint_src_settings, "Name")
                if armature and armature != "":
                    col2.label(icon = "ERROR",text="Couldn't found specified bone in armature.")
        else:
            col2.prop(constraint_src_settings, "Name")
        col2.separator()
        #col2.prop(constraint_src_settings, "TransformationType")
        col2.prop(constraint_src_settings, "TransformationAxis")
        col2.separator()
        col2.prop(constraint_src_settings, "FromRange")
        col2.prop(constraint_src_settings, "ToRange")
        col2.separator()
        col2.prop(constraint_src_settings, "UNKNOWN_0")
        col2.separator()
        col2.prop(constraint_src_settings, "UNKNOWN_1")
        col2.prop(constraint_src_settings, "UNKNOWN_2")
        col2.prop(constraint_src_settings, "UNKNOWN_3")
        col2.prop(constraint_src_settings, "UNKNOWN_4")
        col2.prop(constraint_src_settings, "UNKNOWN_5")
        col2.prop(constraint_src_settings, "UNKNOWN_6")
        col2.prop(constraint_src_settings, "UNKNOWN_7")
        col2.separator()
        col2.prop(constraint_src_settings, "UNKNOWN_8")

class JCNS_PT_ConstraintSrc_Extra_Info_Panel(Panel):
    bl_label = "JCNS Constraint Source Extra Info"
    bl_idname = "JCNS_PT_ConstraintSrc_Extra_Info_Panel"
    bl_space_type = "PROPERTIES"   
    bl_region_type = "WINDOW"
    bl_category = "JCNS Constraint Source Extra Info"
    bl_context = "object"

    @classmethod
    def poll(self,context):
        return context and context.object.mode == "OBJECT" and context.active_object and context.active_object.get("TYPE",None) == "JCNS_ConstraintSrcExtraInfo"

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        constraint_src_extra_info = object.constraint_src_extra_info
        
        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment='CENTER'
        col2.use_property_split = True
        col2.prop(constraint_src_extra_info, "UNKNOWN_1")
        col2.prop(constraint_src_extra_info, "UNKNOWN_2")
        col2.prop(constraint_src_extra_info, "UNKNOWN_3")
        col2.prop(constraint_src_extra_info, "UNKNOWN_4")
        col2.prop(constraint_src_extra_info, "UNKNOWN_5")
        col2.prop(constraint_src_extra_info, "UNKNOWN_6")
        col2.separator()
        col2.prop(constraint_src_extra_info, "UNKNOWN_7")
        


class JCNS_PT_SimpleCns_Settings_Panel(Panel):
    bl_label = "JCNS SimpleConstraint Settings"
    bl_idname = "JCNS_PT_SimpleCns_Settings_Panel"
    bl_space_type = "PROPERTIES"   
    bl_region_type = "WINDOW"
    bl_category = "JCNS SimpleConstraint Settings"
    bl_context = "object"

    @classmethod
    def poll(self,context):
        return context and context.object.mode == "OBJECT" and context.active_object and context.active_object.get("TYPE",None) == "JCNS_SimpleCnsSettings"

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        simplecns_settings = object.simplecns_settings
        
        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment='CENTER'
        col2.use_property_split = True
        col2.prop_search(simplecns_settings, "ArmatureName", context.scene, "objects")
        armature = bpy.data.armatures.get(simplecns_settings.ArmatureName)
        if (not armature) or armature == "":
                col2.label(icon = "ERROR",text="Invalid armature.")
        bone = None
        try:
            if armature:
                col2.prop_search(simplecns_settings, "BoneName", armature, "bones")
                bone = bpy.data.armatures.get(simplecns_settings.ArmatureName).bones[simplecns_settings.BoneName]
        except:
            pass
        #col2.prop(simplecns_settings, "Bone") 
        if (not bone) or bone == "":
            col2.prop(simplecns_settings, "Hash")
            if armature and armature != "":
                col2.label(icon = "ERROR",text="Couldn't found specified bone in armature.")
        
class JCNS_PT_SimpleCnsSrc_Settings_Panel(Panel):
    bl_label = "JCNS SimpleConstraint Source Settings"
    bl_idname = "JCNS_PT_SimpleCnsSrc_Settings_Panel"
    bl_space_type = "PROPERTIES"   
    bl_region_type = "WINDOW"
    bl_category = "JCNS SimpleConstraint Settings"
    bl_context = "object"

    @classmethod
    def poll(self,context):
        return context and context.object.mode == "OBJECT" and context.active_object and context.active_object.get("TYPE",None) == "JCNS_SimpleCnsSrcSettings"

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        simplecns_src_settings = object.simplecns_src_settings
        
        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment='CENTER'
        col2.use_property_split = True
        armature = bpy.data.armatures.get(simplecns_src_settings.ArmatureName)
        if (not armature) or armature == "":
                col2.label(icon = "ERROR",text="Invalid armature.")
        bone = None
        try:
            if armature:
                col2.prop_search(simplecns_src_settings, "BoneName", armature, "bones")
                bone = bpy.data.armatures.get(simplecns_src_settings.ArmatureName).bones[simplecns_src_settings.BoneName]
            else:
                col2.label(icon = "ERROR",text="Constraint armature is not set.")
        except:
            pass
        if (not bone) or bone == "":
            col2.prop(simplecns_src_settings, "Hash")
            if armature and armature != "":
                col2.label(icon = "ERROR",text="Couldn't found specified bone in armature.")
        col2.separator()
        col2.prop(simplecns_src_settings, "Weight")