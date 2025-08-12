import bpy
import os

from .JCNS_PARSER import FileJCNS, FileBufferJCNS
from .UTILS import Vec3, Vec4, BlenderUtils, Version2GameDict
from .EXCEPTIONS import ERROR_Unsupported
from .JCNS_PROPERTIES import (
	getConstraintSettings,  
	getConstraintSrcSettings,
	getSimpleCnsSettings,
	getSimpleCnsSrcSettings,

	setConstraintSettings, 
	setConstraintSrcSettings,
	setSimpleCnsSettings,
	setSimpleCnsSrcSettings,
	)

def ImportJCNSFile(filepath, options, collection=None):
	filename = os.path.split(filepath)[1].split(".jcns")[0] + ".jcns"
	try:
		JCNSVersion = int(os.path.splitext(filepath)[1].replace(".",""))
	except:
		print("Unable to parse JCNS version number in file path.")
		JCNSVersion = None
	if JCNSVersion in Version2GameDict:
		gameName = Version2GameDict[JCNSVersion]
	else:
		gameName = None

	with open(filepath, 'rb') as file:
		jcns_filebuffer = FileBufferJCNS(file.read())

	print(f"\n === JCNS Import Started === \nFilePath: {filepath}\nFileName: {filename}")

	if gameName:
		jcns_file = FileJCNS()
		jcns_file.read(jcns_filebuffer, options["armature"])
		if options["import_data"] == True:
			#headerObj = BlenderUtils.add_empty(f"{filename} Header", [("TYPE", "JCNS_HEADER")], collection=filename)
			#BlenderUtils.lockObjTransforms(headerObj)
			BlenderUtils.getJCNSCollection(filename)
			bpy.data.collections.get(filename).color_tag = "COLOR_04"

			jcns_file.printDebugInfo()
			if len(jcns_file.ConstraintList) > 0:
				ConstraintListObj = BlenderUtils.add_empty(f"Constraints {filename}", [("TYPE", "JCNS_ConstraintList")], collection=filename)
				BlenderUtils.lockObjTransforms(ConstraintListObj)
				for Constraint in jcns_file.ConstraintList:
					ConstraintSettingsObj = BlenderUtils.add_empty(f"Constraint_{jcns_file.ConstraintList.index(Constraint)} {Constraint.ObjectName}", [("TYPE", "JCNS_ConstraintSettings")], ConstraintListObj, filename)
					getConstraintSettings(Constraint, ConstraintSettingsObj)
					BlenderUtils.lockObjTransforms(ConstraintSettingsObj)
					for Source in Constraint.SourceList:
						SourceSettingsObj = BlenderUtils.add_empty(f"Constraint_{jcns_file.ConstraintList.index(Constraint)}_SOURCE_{Constraint.SourceList.index(Source)} {Source.Name}", [("TYPE", "JCNS_ConstraintSrcSettings")], ConstraintSettingsObj, filename)
						getConstraintSrcSettings(Source, SourceSettingsObj)
						BlenderUtils.lockObjTransforms(SourceSettingsObj)
						for Info in Source.ExtraInfoList:
							ExtraSrcInfoObj = BlenderUtils.add_empty(f"Constraint_{jcns_file.ConstraintList.index(Constraint)}_SOURCE_{Constraint.SourceList.index(Source)}_EXTRA_INFO_{Source.ExtraInfoList.index(Info)}", [("TYPE", "JCNS_ConstraintSrcExtraInfo")], SourceSettingsObj, filename)
					for Info in Constraint.ExtraInfoList:
						ExtraCnsInfoObj = BlenderUtils.add_empty(f"Constraint_{jcns_file.ConstraintList.index(Constraint)}_EXTRA_INFO_{Constraint.ExtraInfoList.index(Info)}", [("TYPE", "JCNS_ConstraintExtraInfo")], ConstraintSettingsObj, filename)
			
			if len(jcns_file.SimpleCnsList) > 0:
				SimpleCnsListObj = BlenderUtils.add_empty(f"SimpleConstraints {filename}", [("TYPE", "JCNS_SCList")], collection=filename)
				BlenderUtils.lockObjTransforms(SimpleCnsListObj)
				for SimpleCns in jcns_file.SimpleCnsList:
					SimpleCnsSettingsObj = BlenderUtils.add_empty(f"SimpleConstraint_{jcns_file.SimpleCnsList.index(SimpleCns)}", [("TYPE", "JCNS_SimpleCnsSettings")], SimpleCnsListObj, filename, display_type=3)
					getSimpleCnsSettings(SimpleCns, SimpleCnsSettingsObj)
					try:
						SimpleCnsSettingsObj.location = bpy.data.objects[SimpleCns.Armature].matrix_world @ bpy.data.objects[SimpleCns.Armature].pose.bones[SimpleCns.Bone].head
					except:
						pass
					BlenderUtils.lockObjTransforms(SimpleCnsSettingsObj, lockLocation=False)
					for Source in SimpleCns.SourceList:
						SimpleCnsSrcObj = BlenderUtils.add_empty(f"SimpleConstraint_{jcns_file.SimpleCnsList.index(SimpleCns)}_SOURCE_{SimpleCns.SourceList.index(Source)}", [("TYPE", "JCNS_SimpleCnsSrcSettings")], SimpleCnsSettingsObj, filename, display_type=3)
						getSimpleCnsSrcSettings(Source, SimpleCnsSrcObj)
						try:
							SimpleCnsSrcObj.location = bpy.data.objects[Source.Armature].matrix_world @ bpy.data.objects[Source.Armature].pose.bones[Source.Bone].head - SimpleCnsSettingsObj.location
						except:
							pass
						BlenderUtils.lockObjTransforms(SimpleCnsSrcObj, lockLocation=False)

		print("DONE Importing.\n =========================== ")
	else:
		raise ERROR_Unsupported
