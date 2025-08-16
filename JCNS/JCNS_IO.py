import bpy
import os

from .JCNS_PARSER import FileJCNS, FileBufferJCNS
from .UTILS import BlenderUtils, Version2GameDict
from .EXCEPTIONS import ERROR_Unsupported
from .JCNS_PROPERTIES import (
	getJointSettings,
	getConstraintSettings, 
	getConstraintExtraInfo,
	getConstraintSrcSettings,
	getConstraintSrcExtraInfo,
	getSimpleCnsSettings,
	getSimpleCnsSrcSettings,

	setJointSettings,
	setConstraintSettings, 
	setConstraintExtraInfo,
	setConstraintSrcSettings,
	setConstraintSrcExtraInfo,
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
		if options["debug_mode"]:
			jcns_file.printDebugInfo()
		if options["import_data"]:
			#headerObj = BlenderUtils.add_empty(f"{filename} Header", [("TYPE", "JCNS_HEADER")], collection=filename)
			#BlenderUtils.lockObjTransforms(headerObj)
			JCNSCollection = BlenderUtils.getJCNSCollection(filename)
			JCNSCollection.color_tag = "COLOR_04"

			if len(jcns_file.ExtraJointList) > 0:
				JointCollection = BlenderUtils.getCollection(f"Joints {filename}", JCNSCollection)
				for Joint in jcns_file.ExtraJointList:
					JointSettingsObj = BlenderUtils.add_empty(f"Joint_{jcns_file.ExtraJointList.index(Joint)} {Joint.Name}", [("TYPE", "JCNS_JointSettings")], None, JointCollection)
					getJointSettings(Joint, JointSettingsObj)
					#BlenderUtils.lockObjTransforms(ConstraintSettingsObj, lockLocation=False)

			if len(jcns_file.ConstraintList) > 0:
				ConstraintCollection = BlenderUtils.getCollection(f"Constraints {filename}", JCNSCollection)
				#ConstraintListObj = BlenderUtils.add_empty(f"Constraints {filename}", [("TYPE", "JCNS_ConstraintList")], collection=filename)
				#BlenderUtils.lockObjTransforms(ConstraintListObj)
				for Constraint in jcns_file.ConstraintList:
					ConstraintSettingsObj = BlenderUtils.add_empty(f"Constraint_{jcns_file.ConstraintList.index(Constraint)} {Constraint.Name}", [("TYPE", "JCNS_ConstraintSettings")], None, ConstraintCollection)
					getConstraintSettings(Constraint, ConstraintSettingsObj)
					#BlenderUtils.lockObjTransforms(ConstraintSettingsObj, lockLocation=False)
					for Source in Constraint.SourceList:
						SourceSettingsObj = BlenderUtils.add_empty(f"Constraint_{jcns_file.ConstraintList.index(Constraint)}_SOURCE_{Constraint.SourceList.index(Source)} {Source.Name}", [("TYPE", "JCNS_ConstraintSrcSettings")], ConstraintSettingsObj, ConstraintCollection)
						getConstraintSrcSettings(Source, SourceSettingsObj)
						#BlenderUtils.lockObjTransforms(SourceSettingsObj, lockLocation=False)
						for Info in Source.ExtraInfoList:
							ExtraSrcInfoObj = BlenderUtils.add_empty(f"Constraint_{jcns_file.ConstraintList.index(Constraint)}_SOURCE_{Constraint.SourceList.index(Source)}_EXTRA_INFO_{Source.ExtraInfoList.index(Info)}", [("TYPE", "JCNS_ConstraintSrcExtraInfo")], SourceSettingsObj, ConstraintCollection)
							getConstraintSrcExtraInfo(Info, ExtraSrcInfoObj)
					for Info in Constraint.ExtraInfoList:
						ExtraCnsInfoObj = BlenderUtils.add_empty(f"Constraint_{jcns_file.ConstraintList.index(Constraint)}_EXTRA_INFO_{Constraint.ExtraInfoList.index(Info)}", [("TYPE", "JCNS_ConstraintExtraInfo")], ConstraintSettingsObj, ConstraintCollection)
						getConstraintExtraInfo(Info, ExtraCnsInfoObj)
			
			if len(jcns_file.SimpleCnsList) > 0:
				SimpleCnsCollection = BlenderUtils.getCollection(f"SimpleConstraints {filename}", JCNSCollection)
				#SimpleCnsListObj = BlenderUtils.add_empty(f"SimpleConstraints {filename}", [("TYPE", "JCNS_SCList")], collection=filename)
				#BlenderUtils.lockObjTransforms(SimpleCnsListObj)
				for SimpleCns in jcns_file.SimpleCnsList:
					SimpleCnsSettingsObj = BlenderUtils.add_empty(f"SimpleConstraint_{jcns_file.SimpleCnsList.index(SimpleCns)}", [("TYPE", "JCNS_SimpleCnsSettings")], None, SimpleCnsCollection, display_type=3)
					getSimpleCnsSettings(SimpleCns, SimpleCnsSettingsObj)
					try:
						SimpleCnsSettingsObj.location = bpy.data.objects[SimpleCns.ArmatureName].matrix_world @ bpy.data.objects[SimpleCns.ArmatureName].pose.bones[SimpleCns.BoneName].head
					except:
						pass
					#BlenderUtils.lockObjTransforms(SimpleCnsSettingsObj, lockLocation=False)
					for Source in SimpleCns.SourceList:
						SimpleCnsSrcObj = BlenderUtils.add_empty(f"SimpleConstraint_{jcns_file.SimpleCnsList.index(SimpleCns)}_SOURCE_{SimpleCns.SourceList.index(Source)}", [("TYPE", "JCNS_SimpleCnsSrcSettings")], SimpleCnsSettingsObj, SimpleCnsCollection, display_type=3)
						getSimpleCnsSrcSettings(Source, SimpleCnsSrcObj)
						try:
							SimpleCnsSrcObj.location = bpy.data.objects[Source.ArmatureName].matrix_world @ bpy.data.objects[Source.ArmatureName].pose.bones[Source.BoneName].head - SimpleCnsSettingsObj.location
						except:
							pass
						#BlenderUtils.lockObjTransforms(SimpleCnsSrcObj, lockLocation=False)

		print("DONE Importing.\n =========================== ")
	else:
		raise ERROR_Unsupported
