import bpy
from bpy.props import EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, StringProperty

class ConstraintSettings_Properties(bpy.types.PropertyGroup):
	Name: StringProperty(
		name = "Object Name",
		description = "Name of object that constraint applies on. Could be bone name, material name, blendshape, etc.",
		default = "",
	)
	MaterialProperty: StringProperty(
		name = "Material Property",
		description = "Material Property that constraint applies on.",
		default = "",
	)
	TransformationType: EnumProperty(
		name = "Transformation",
		description = "Transformation Type.",
		items = [ 
			("0",  "Location", ""),
			("1",  "Rotation", ""),
            ("2",  "Scale", ""),
            ("3",  "BlendShape", ""),
            ("4",  "UNKNOWN_4", ""),
            ("5",  "UNKNOWN_5", ""),
            ("6",  "UNKNOWN_6", ""),
            ("7",  "MatProperty_Scalar", ""),
            ("8",  "MatProperty_Vec4", ""),
            ("9",  "MatProperty_Vec3", ""),
            ("10", "MatProperty_Vec2", ""),
            ("11", "MatProperty_Color", ""),
            ("12", "UNKNOWN_12", ""),
            ("13", "UNKNOWN_13", ""),
            ("14", "UNKNOWN_14", ""),
            ("15", "UNKNOWN_15", ""),
            ("16", "UNKNOWN_16", ""),
		]
	)
	TransformationAxis: EnumProperty(
		name = "Axis",
		description = "Transformation Axis.",
		items = [ 
			("0", "X", ""),
			("1", "Y", ""),
			("2", "Z", ""),
			("3", "W", ""),
		]
	)
	UNKNOWN_1: IntProperty(
		name = "UNKNOWN_1",
		default = 0,
		min = 0,
		max = 255,
	)
	UNKNOWN_2: IntProperty(
		name = "UNKNOWN_2",
		default = 0,
		min = 0,
		max = 255,
	)
	UNKNOWN_3: IntProperty(
		name = "UNKNOWN_3",
		default = 0,
		min = 0,
		max = 255,
	)
	UNKNOWN_4: IntProperty(
		name = "UNKNOWN_4",
		default = 0,
		min = 0,
		max = 255,
	)
	UNKNOWN_5: FloatVectorProperty(
		name = "UNKNOWN_5",
		size = 4,
		default = (0.0, 0.0, 0.0, 0.0),
		subtype = "QUATERNION",
	)

def getConstraintSettings(Constraint, targetObject):
	targetObject.constraint_settings.Name                =  Constraint.ObjectName
	targetObject.constraint_settings.MaterialProperty    =  Constraint.MaterialProperty if Constraint.MaterialProperty else ""
	targetObject.constraint_settings.TransformationType  =  str(Constraint.TransformationType)
	targetObject.constraint_settings.TransformationAxis  =  str(Constraint.TransformationAxis)
	
	targetObject.constraint_settings.UNKNOWN_1  =  Constraint.UNKNOWN_1
	targetObject.constraint_settings.UNKNOWN_2  =  Constraint.UNKNOWN_2
	targetObject.constraint_settings.UNKNOWN_3  =  Constraint.UNKNOWN_3
	targetObject.constraint_settings.UNKNOWN_4  =  Constraint.UNKNOWN_4
	targetObject.constraint_settings.UNKNOWN_5  =  (Constraint.UNKNOWN_5.w, Constraint.UNKNOWN_5.x, Constraint.UNKNOWN_5.y, Constraint.UNKNOWN_5.z)

def setConstraintSettings(Constraint, targetObject):
	Constraint.ObjectName          =  targetObject.constraint_settings.Name
	Constraint.MaterialProperty    =  targetObject.constraint_settings.MaterialProperty
	Constraint.TransformationType  =  int(targetObject.constraint_settings.TransformationType)
	Constraint.TransformationAxis  =  int(targetObject.constraint_settings.TransformationAxis)
	
	Constraint.UNKNOWN_1           =  targetObject.constraint_settings.UNKNOWN_1
	Constraint.UNKNOWN_2           =  targetObject.constraint_settings.UNKNOWN_2
	Constraint.UNKNOWN_3           =  targetObject.constraint_settings.UNKNOWN_3
	Constraint.UNKNOWN_4           =  targetObject.constraint_settings.UNKNOWN_4
	Constraint.UNKNOWN_5.x         =  targetObject.constraint_settings.UNKNOWN_5[1]
	Constraint.UNKNOWN_5.y         =  targetObject.constraint_settings.UNKNOWN_5[2]
	Constraint.UNKNOWN_5.z         =  targetObject.constraint_settings.UNKNOWN_5[3]
	Constraint.UNKNOWN_5.z         =  targetObject.constraint_settings.UNKNOWN_5[0]


class ConstraintSrcSettings_Properties(bpy.types.PropertyGroup):
	Name: StringProperty(
		name = "Source Name",
		description = "Name of source that constrain from. Could be bone name, blendshape, etc.",
		default = "",
	)
	TransformationType: EnumProperty(
		name = "Transformation (Not Sure)",
		description = "Transformation Type.",
		items = [ 
			("0",  "Location", ""),
			("1",  "Rotation", ""),
            ("2",  "Scale", ""),
            ("3",  "BlendShape", ""),
            ("4",  "UNKNOWN_4", ""),
            ("5",  "UNKNOWN_5", ""),
            ("6",  "UNKNOWN_6", ""),
            ("7",  "MatProperty_Scalar", ""),
            ("8",  "MatProperty_Vec4", ""),
            ("9",  "MatProperty_Vec3", ""),
            ("10", "MatProperty_Vec2", ""),
            ("11", "MatProperty_Color", ""),
            ("12", "UNKNOWN_12", ""),
            ("13", "UNKNOWN_13", ""),
            ("14", "UNKNOWN_14", ""),
            ("15", "UNKNOWN_15", ""),
            ("16", "UNKNOWN_16", ""),
		]
	)
	TransformationAxis: EnumProperty(
		name = "Axis",
		description = "Transformation Axis.",
		items = [ 
			("0", "X", ""),
			("1", "Y", ""),
			("2", "Z", ""),
			("3", "W", ""),
		]
	)
	FromRange: FloatVectorProperty(
		name = "Map From",
		size = 3,
		default = (0.0, 0.0, 0.0),
		subtype = "NONE",
	)
	ToRange: FloatVectorProperty(
		name = "Map To",
		size = 3,
		default = (0.0, 0.0, 0.0),
		subtype = "NONE",
	)
	UNKNOWN_1: IntProperty(
		name = "UNKNOWN_1",
		default = 0,
		min = 0,
		max = 255,
	)
	UNKNOWN_2: IntProperty(
		name = "UNKNOWN_2",
		default = 0,
		min = 0,
		max = 255,
	)
	UNKNOWN_3: IntProperty(
		name = "UNKNOWN_3",
		default = 0,
		min = 0,
		max = 255,
	)
	UNKNOWN_4: IntProperty(
		name = "UNKNOWN_4",
		default = 0,
		min = 0,
		max = 255,
	)
	UNKNOWN_5: IntProperty(
		name = "UNKNOWN_5",
		default = 0,
		min = 0,
		max = 255,
	)
	UNKNOWN_6: IntProperty(
		name = "UNKNOWN_6",
		default = 0,
		min = 0,
		max = 255,
	)
	UNKNOWN_7: FloatVectorProperty(
		name = "UNKNOWN_7",
		size = 4,
		default = (0.0, 0.0, 0.0, 0.0),
		subtype = "QUATERNION",
	)

def getConstraintSrcSettings(ConstraintSrc, targetObject):
	targetObject.constraint_src_settings.Name                =  ConstraintSrc.Name
	targetObject.constraint_src_settings.TransformationType  =  str(ConstraintSrc.TransformationType)
	targetObject.constraint_src_settings.TransformationAxis  =  str(ConstraintSrc.TransformationAxis)
	targetObject.constraint_src_settings.FromRange           =  (ConstraintSrc.FromRange[0], ConstraintSrc.FromRange[1], ConstraintSrc.FromRange[2])
	targetObject.constraint_src_settings.ToRange             =  (ConstraintSrc.ToRange[0], ConstraintSrc.ToRange[1], ConstraintSrc.ToRange[2])
	
	targetObject.constraint_src_settings.UNKNOWN_1  =  ConstraintSrc.UNKNOWN_1
	targetObject.constraint_src_settings.UNKNOWN_2  =  ConstraintSrc.UNKNOWN_2
	targetObject.constraint_src_settings.UNKNOWN_3  =  ConstraintSrc.UNKNOWN_3
	targetObject.constraint_src_settings.UNKNOWN_4  =  ConstraintSrc.UNKNOWN_4
	targetObject.constraint_src_settings.UNKNOWN_4  =  ConstraintSrc.UNKNOWN_5
	targetObject.constraint_src_settings.UNKNOWN_6  =  ConstraintSrc.UNKNOWN_6
	targetObject.constraint_src_settings.UNKNOWN_7  =  (ConstraintSrc.UNKNOWN_7.w, ConstraintSrc.UNKNOWN_7.x, ConstraintSrc.UNKNOWN_7.y, ConstraintSrc.UNKNOWN_7.z)

def setConstraintSrcSettings(ConstraintSrc, targetObject, version = 2):
	ConstraintSrc.Name                =  targetObject.constraint_src_settings.Name
	ConstraintSrc.TransformationType  =  int(targetObject.constraint_src_settings.TransformationType)
	ConstraintSrc.TransformationAxis  =  int(targetObject.constraint_src_settings.TransformationAxis)
	
	ConstraintSrc.UNKNOWN_1           =  targetObject.constraint_src_settings.UNKNOWN_1
	ConstraintSrc.UNKNOWN_2           =  targetObject.constraint_src_settings.UNKNOWN_2
	ConstraintSrc.UNKNOWN_3           =  targetObject.constraint_src_settings.UNKNOWN_3
	ConstraintSrc.UNKNOWN_4           =  targetObject.constraint_src_settings.UNKNOWN_4
	ConstraintSrc.UNKNOWN_7.x         =  targetObject.constraint_src_settings.UNKNOWN_7[1]
	ConstraintSrc.UNKNOWN_7.y         =  targetObject.constraint_src_settings.UNKNOWN_7[2]
	ConstraintSrc.UNKNOWN_7.z         =  targetObject.constraint_src_settings.UNKNOWN_7[3]
	ConstraintSrc.UNKNOWN_7.z         =  targetObject.constraint_src_settings.UNKNOWN_7[0]

	for _ in range(len(ConstraintSrc.FromRange)):
		ConstraintSrc.FromRange[_] = targetObject.constraint_src_settings.FromRange[_]
	for _ in range(len(ConstraintSrc.ToRange)):
		ConstraintSrc.ToRange[_] = targetObject.constraint_src_settings.ToRange[_]

