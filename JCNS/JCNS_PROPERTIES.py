import bpy
from bpy.props import EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, StringProperty
from .UTILS import HashUtils

def update_name(self, context):
	parentObj = self.id_data
	try:
		#print(parentObj)
		if parentObj != None:
			split = parentObj.name.split(" ",1)
			if len(split) == 2:
				parentObj.name = f"{split[0]} {self.Name}"
	except:
		pass

def update_location(self, context):
	if self.id_data.parent:
		self.id_data.location = bpy.data.objects[self.ArmatureName].matrix_world @ bpy.data.objects[self.ArmatureName].pose.bones[self.BoneName].head - self.id_data.parent.location
	else:
		self.id_data.location = bpy.data.objects[self.ArmatureName].matrix_world @ bpy.data.objects[self.ArmatureName].pose.bones[self.BoneName].head

def update_armature_infos(self, context):
	for source in self.id_data.children:
		try:
			source.constraint_src_settings.ArmatureName = self.ArmatureName
		except: pass

	try:
		armature = bpy.data.objects[self.ArmatureName]
		for bone in armature.pose.bones:
			if bone.name == self.Name:
				self.Type = "0"
				self.BoneName = bone.name
				update_location(self, context)
				for child in self.id_data.children:
					child.location -= self.id_data.location
				break
	except: pass

def	update_bone_info(self, context):
	if self.BoneName != "" and self.BoneName != self.Name:
		self.Name = self.BoneName
		update_location(self, context)
		if self.id_data.children:
			for child in self.id_data.children:
				try:
					update_location(child.constraint_src_settings, context)
				except:
					pass

class ConstraintSettings_Properties(bpy.types.PropertyGroup):
	Type: EnumProperty(
		name = "Type",
		description = "Object Type",
		items = [ 
			("0",  "Bone", ""),
			("1",  "Material/RSZObject Property", ""),
			("2",  "BlendShape/Custom/etc", ""),
		]
	)
	ArmatureName: StringProperty(
		name = "Armature",
		description = "Armature of current constraint.",
		default = "",
		update = update_armature_infos
	)
	BoneName:StringProperty(
		name = "Bone",
		description = "Bone that constraint applies to",
		default = "",
		update = update_bone_info
	)
	Name: StringProperty(
		name = "Object Name",
		description = "Name of object that constraint applies on. Could be name of bone, material, blendshape, RSZobject, etc.",
		default = "",
		update = update_name
	)
	Property: StringProperty(
		name = "Property",
		description = "Property that constraint applies on.",
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
	targetObject.constraint_settings.Type                =  str(Constraint.Type)
	targetObject.constraint_settings.ArmatureName        =  Constraint.ArmatureName
	targetObject.constraint_settings.BoneName            =  Constraint.BoneName
	targetObject.constraint_settings.Name                =  Constraint.Name
	targetObject.constraint_settings.Property            =  Constraint.Property if Constraint.Property else ""
	targetObject.constraint_settings.TransformationType  =  str(Constraint.TransformationType)
	targetObject.constraint_settings.TransformationAxis  =  str(Constraint.TransformationAxis)
	
	targetObject.constraint_settings.UNKNOWN_1  =  Constraint.UNKNOWN_1
	targetObject.constraint_settings.UNKNOWN_2  =  Constraint.UNKNOWN_2
	targetObject.constraint_settings.UNKNOWN_3  =  Constraint.UNKNOWN_3
	targetObject.constraint_settings.UNKNOWN_4  =  Constraint.UNKNOWN_4
	targetObject.constraint_settings.UNKNOWN_5  =  (Constraint.UNKNOWN_5.w, Constraint.UNKNOWN_5.x, Constraint.UNKNOWN_5.y, Constraint.UNKNOWN_5.z)

def setConstraintSettings(Constraint, targetObject):
	Constraint.Type                =  int(targetObject.constraint_settings.Type)
	Constraint.Name                =  targetObject.constraint_settings.Name
	Constraint.Property            =  targetObject.constraint_settings.Property
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



class ConstraintExtraInfo_Properties(bpy.types.PropertyGroup):
	UNKNOWN_1: FloatProperty(
		name = "UNKNOWN_1",
		default = 0.0,
	)
	UNKNOWN_2: FloatProperty(
		name = "UNKNOWN_2",
		default = 0.0,
	)
	UNKNOWN_3: IntProperty(
		name = "UNKNOWN_3",
		default = 0,
	)
	UNKNOWN_4: IntProperty(
		name = "UNKNOWN_4",
		default = 0,
	)
	UNKNOWN_5: IntProperty(
		name = "UNKNOWN_5",
		default = 0,
	)
	UNKNOWN_6: IntProperty(
		name = "UNKNOWN_6",
		default = 0,
	)

def getConstraintExtraInfo(ExtraInfo, targetObject):
	targetObject.constraint_extra_info.UNKNOWN_1     =  ExtraInfo.UNKNOWN_1
	targetObject.constraint_extra_info.UNKNOWN_2     =  ExtraInfo.UNKNOWN_2
	targetObject.constraint_extra_info.UNKNOWN_3     =  ExtraInfo.UNKNOWN_3
	targetObject.constraint_extra_info.UNKNOWN_4     =  ExtraInfo.UNKNOWN_4
	targetObject.constraint_extra_info.UNKNOWN_5     =  ExtraInfo.UNKNOWN_5
	targetObject.constraint_extra_info.UNKNOWN_6     =  ExtraInfo.UNKNOWN_6

def setConstraintExtraInfo(ExtraInfo, targetObject):
	ExtraInfo.UNKNOWN_1    =  targetObject.constraint_extra_info.UNKNOWN_1
	ExtraInfo.UNKNOWN_2    =  targetObject.constraint_extra_info.UNKNOWN_2
	ExtraInfo.UNKNOWN_3    =  targetObject.constraint_extra_info.UNKNOWN_3
	ExtraInfo.UNKNOWN_4    =  targetObject.constraint_extra_info.UNKNOWN_4
	ExtraInfo.UNKNOWN_5    =  targetObject.constraint_extra_info.UNKNOWN_5
	ExtraInfo.UNKNOWN_6    =  targetObject.constraint_extra_info.UNKNOWN_6



class ConstraintSrcSettings_Properties(bpy.types.PropertyGroup):
	Type: EnumProperty(
		name = "Type",
		description = "Source Type",
		items = [ 
			("0",  "Bone", ""),
			("1",  "BlendShape/Custom/etc", ""),
		]
	)
	ArmatureName: StringProperty(
		name = "Armature",
		description = "Armature of current constraint.",
		default = "",
		update = update_armature_infos
	)
	BoneName: StringProperty(
		name = "Bone",
		description = "Bone that constrain from.",
		default = "",
		update = update_bone_info
	)
	Name: StringProperty(
		name = "Source Name",
		description = "Name of source that constrain from. Could be bone name, blendshape, etc.",
		default = "",
		update = update_name
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
	UNKNOWN_0: IntProperty(
		name = "UNKNOWN_0",
		default = 0,
		min = 0,
		max = 255,
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
	UNKNOWN_7: IntProperty(
		name = "UNKNOWN_7",
		default = 0,
		min = 0,
		max = 255,
	)
	UNKNOWN_8: FloatVectorProperty(
		name = "UNKNOWN_8",
		size = 4,
		default = (0.0, 0.0, 0.0, 0.0),
		subtype = "QUATERNION",
	)

def getConstraintSrcSettings(ConstraintSrc, targetObject):
	targetObject.constraint_src_settings.Type                =  str(ConstraintSrc.Type)
	targetObject.constraint_src_settings.ArmatureName        =  ConstraintSrc.ArmatureName
	targetObject.constraint_src_settings.BoneName            =  ConstraintSrc.BoneName
	targetObject.constraint_src_settings.Name                =  ConstraintSrc.Name
	targetObject.constraint_src_settings.TransformationAxis  =  str(ConstraintSrc.TransformationAxis)
	targetObject.constraint_src_settings.FromRange           =  (ConstraintSrc.FromRange[0], ConstraintSrc.FromRange[1], ConstraintSrc.FromRange[2])
	targetObject.constraint_src_settings.ToRange             =  (ConstraintSrc.ToRange[0], ConstraintSrc.ToRange[1], ConstraintSrc.ToRange[2])
	
	targetObject.constraint_src_settings.UNKNOWN_0  =  ConstraintSrc.UNKNOWN_0
	targetObject.constraint_src_settings.UNKNOWN_1  =  ConstraintSrc.UNKNOWN_1
	targetObject.constraint_src_settings.UNKNOWN_2  =  ConstraintSrc.UNKNOWN_2
	targetObject.constraint_src_settings.UNKNOWN_3  =  ConstraintSrc.UNKNOWN_3
	targetObject.constraint_src_settings.UNKNOWN_4  =  ConstraintSrc.UNKNOWN_4
	targetObject.constraint_src_settings.UNKNOWN_4  =  ConstraintSrc.UNKNOWN_5
	targetObject.constraint_src_settings.UNKNOWN_6  =  ConstraintSrc.UNKNOWN_6
	targetObject.constraint_src_settings.UNKNOWN_7  =  ConstraintSrc.UNKNOWN_7
	targetObject.constraint_src_settings.UNKNOWN_8  =  (ConstraintSrc.UNKNOWN_8.w, ConstraintSrc.UNKNOWN_8.x, ConstraintSrc.UNKNOWN_8.y, ConstraintSrc.UNKNOWN_8.z)

def setConstraintSrcSettings(ConstraintSrc, targetObject):
	ConstraintSrc.Type                =  int(targetObject.constraint_src_settings.Type)
	ConstraintSrc.Name                =  targetObject.constraint_src_settings.Name
	ConstraintSrc.TransformationType  =  int(targetObject.constraint_src_settings.TransformationType)
	ConstraintSrc.TransformationAxis  =  int(targetObject.constraint_src_settings.TransformationAxis)
	
	ConstraintSrc.UNKNOWN_0           =  targetObject.constraint_src_settings.UNKNOWN_0
	ConstraintSrc.UNKNOWN_1           =  targetObject.constraint_src_settings.UNKNOWN_1
	ConstraintSrc.UNKNOWN_2           =  targetObject.constraint_src_settings.UNKNOWN_2
	ConstraintSrc.UNKNOWN_3           =  targetObject.constraint_src_settings.UNKNOWN_3
	ConstraintSrc.UNKNOWN_4           =  targetObject.constraint_src_settings.UNKNOWN_4
	ConstraintSrc.UNKNOWN_5           =  targetObject.constraint_src_settings.UNKNOWN_5
	ConstraintSrc.UNKNOWN_6           =  targetObject.constraint_src_settings.UNKNOWN_6
	ConstraintSrc.UNKNOWN_7           =  targetObject.constraint_src_settings.UNKNOWN_7
	ConstraintSrc.UNKNOWN_8.x         =  targetObject.constraint_src_settings.UNKNOWN_8[1]
	ConstraintSrc.UNKNOWN_8.y         =  targetObject.constraint_src_settings.UNKNOWN_8[2]
	ConstraintSrc.UNKNOWN_8.z         =  targetObject.constraint_src_settings.UNKNOWN_8[3]
	ConstraintSrc.UNKNOWN_8.z         =  targetObject.constraint_src_settings.UNKNOWN_8[0]

	for _ in range(len(ConstraintSrc.FromRange)):
		ConstraintSrc.FromRange[_] = targetObject.constraint_src_settings.FromRange[_]
	for _ in range(len(ConstraintSrc.ToRange)):
		ConstraintSrc.ToRange[_] = targetObject.constraint_src_settings.ToRange[_]



class ConstraintSrcExtraInfo_Properties(bpy.types.PropertyGroup):
	UNKNOWN_1: FloatProperty(
		name = "UNKNOWN_1",
		default = 0.0,
	)
	UNKNOWN_2: FloatProperty(
		name = "UNKNOWN_2",
		default = 0.0,
	)
	UNKNOWN_3: FloatProperty(
		name = "UNKNOWN_3",
		default = 0.0,
	)
	UNKNOWN_4: FloatProperty(
		name = "UNKNOWN_4",
		default = 0.0,
	)
	UNKNOWN_5: FloatProperty(
		name = "UNKNOWN_5",
		default = 0.0,
	)
	UNKNOWN_6: FloatProperty(
		name = "UNKNOWN_6",
		default = 0.0,
	)
	UNKNOWN_7: IntProperty(
		name = "UNKNOWN_7",
		default = 0,
	)

def getConstraintSrcExtraInfo(ExtraInfo, targetObject):
	targetObject.constraint_src_extra_info.UNKNOWN_1     =  ExtraInfo.UNKNOWN_1
	targetObject.constraint_src_extra_info.UNKNOWN_2     =  ExtraInfo.UNKNOWN_2
	targetObject.constraint_src_extra_info.UNKNOWN_3     =  ExtraInfo.UNKNOWN_3
	targetObject.constraint_src_extra_info.UNKNOWN_4     =  ExtraInfo.UNKNOWN_4
	targetObject.constraint_src_extra_info.UNKNOWN_5     =  ExtraInfo.UNKNOWN_5
	targetObject.constraint_src_extra_info.UNKNOWN_6     =  ExtraInfo.UNKNOWN_6
	targetObject.constraint_src_extra_info.UNKNOWN_7     =  ExtraInfo.UNKNOWN_7

def setConstraintSrcExtraInfo(ExtraInfo, targetObject):
	ExtraInfo.UNKNOWN_1    =  targetObject.constraint_src_extra_info.UNKNOWN_1
	ExtraInfo.UNKNOWN_2    =  targetObject.constraint_src_extra_info.UNKNOWN_2
	ExtraInfo.UNKNOWN_3    =  targetObject.constraint_src_extra_info.UNKNOWN_3
	ExtraInfo.UNKNOWN_4    =  targetObject.constraint_src_extra_info.UNKNOWN_4
	ExtraInfo.UNKNOWN_5    =  targetObject.constraint_src_extra_info.UNKNOWN_5
	ExtraInfo.UNKNOWN_6    =  targetObject.constraint_src_extra_info.UNKNOWN_6
	ExtraInfo.UNKNOWN_7    =  targetObject.constraint_src_extra_info.UNKNOWN_7



def update_armature_infos_sc(self, context):
	for source in self.id_data.children:
		try:
			source.simplecns_src_settings.ArmatureName = self.ArmatureName
		except: pass

	try:
		armature = bpy.data.objects[self.ArmatureName]
		for bone in armature.pose.bones:
			if HashUtils.generate_murmurhash_32(bone.name) == int(self.Hash, 16):
				self.BoneName = bone.name
				update_location(self, context)
				for child in self.id_data.children:
					child.location -= self.id_data.location
				break
	except:
		pass

def update_bone_info_sc(self, context):
	if self.BoneName != "" and HashUtils.generate_murmurhash_32(self.BoneName) != int(self.Hash, 16):
		self.Hash = str(hex(HashUtils.generate_murmurhash_32(self.BoneName))).replace("0x", "").upper()
		update_location(self, context)
		if self.id_data.children:
			for child in self.id_data.children:
				try:
					update_location(child.simplecns_src_settings, context)
				except:
					pass
	
class SimpleCnsSettings_Properties(bpy.types.PropertyGroup):
	ArmatureName: StringProperty(
		name = "Armature",
		description = "Armature of current constraint.",
		default = "",
		update = update_armature_infos_sc
	)
	BoneName:StringProperty(
		name = "Bone",
		description = "Bone that constraint applies to",
		default = "",
		update = update_bone_info_sc
	)
	Hash: StringProperty(
		name = "Hash",
		description = "32-bit Murmur3 Hash of bone that constraint applies to. \nThis would be updated automatically, and only appears when the armature or bone is not set or there's something wrong with them in the settings.\n\nDo NOT modify this unless you know what you are doing.",
		default = "",
		maxlen = 8,
	)

def getSimpleCnsSettings(SimpleCns, targetObject):
	targetObject.simplecns_settings.Hash          =  str(hex(SimpleCns.Hash)).replace("0x", "").upper()
	targetObject.simplecns_settings.ArmatureName  =  SimpleCns.ArmatureName
	targetObject.simplecns_settings.BoneName      =  SimpleCns.BoneName

def setSimpleCnsSettings(SimpleCns, targetObject):
	SimpleCns.BoneName     =  targetObject.simplecns_settings.BoneName
	SimpleCns.Hash         =  int(targetObject.simplecns_settings.Hash, 16)
	



class SimpleCnsSrcSettings_Properties(bpy.types.PropertyGroup):
	ArmatureName: StringProperty(
		name = "Armature",
		description = "Armature of current constraint.",
		default = "",
		update = update_armature_infos_sc
	)
	BoneName: StringProperty(
		name = "Bone",
		description = "Bone that constrain from.",
		default = "",
		update = update_bone_info_sc
	)
	Hash: StringProperty(
		name = "Hash",
		description = "Hash of bone that constrain from.\nThis would be updated automatically, and only appears when the armature or bone is not set or there's something wrong with them in the settings.\n\nDo NOT modify this unless you know what you are doing.",
		default = "",
		maxlen = 8,
	)
	Weight: FloatProperty(
		name = "Weight",
		default = 0.0,
	)

def getSimpleCnsSrcSettings(SimpleCnsSrc, targetObject):
	targetObject.simplecns_src_settings.Hash          =  str(hex(SimpleCnsSrc.Hash)).replace("0x", "").upper()
	targetObject.simplecns_src_settings.ArmatureName  =  SimpleCnsSrc.ArmatureName
	targetObject.simplecns_src_settings.BoneName      =  SimpleCnsSrc.BoneName
	targetObject.simplecns_src_settings.Weight        =  SimpleCnsSrc.Weight

def setSimpleCnsSrcSettings(SimpleCnsSrc, targetObject):
	SimpleCnsSrc.BoneName    =  targetObject.simplecns_src_settings.BoneName
	SimpleCnsSrc.Hash        =  int(targetObject.simplecns_src_settings.Hash, 16)
	SimpleCnsSrc.Weight      =  targetObject.simplecns_src_settings.Weight
