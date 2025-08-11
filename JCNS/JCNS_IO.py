import bpy
import os

from .JCNS_PARSER import FileJCNS, FileBufferJCNS
from .UTILS import Vec3, Vec4, BlenderUtils, Version2GameDict
from .EXCEPTIONS import ERROR_Unsupported
from .JCNS_PROPERTIES import getConstraintSettings, setConstraintSettings, getConstraintSrcSettings, setConstraintSrcSettings

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
		jcns_file.read(jcns_filebuffer)
		if options["import_data"] == True:
			headerObj = BlenderUtils.add_empty(f"{filename} Header", [("TYPE", "JCNS_HEADER")], collection=filename)
			BlenderUtils.lockObjTransforms(headerObj)
			bpy.data.collections.get(filename).color_tag = "COLOR_04"

			jcns_file.printDebugInfo()
			if len(jcns_file.ConstraintList) > 0:
				ConstraintListObj = BlenderUtils.add_empty(f"{filename} Constraints", [("TYPE", "JCNS_ConstraintList")], headerObj, filename)
				BlenderUtils.lockObjTransforms(ConstraintListObj)
				for Constraint in jcns_file.ConstraintList:
					ConstraintSettingsObj = BlenderUtils.add_empty(f"Constraint_{jcns_file.ConstraintList.index(Constraint)} {Constraint.ObjectName}", [("TYPE", "JCNS_ConstraintSettings")], ConstraintListObj, filename)
					getConstraintSettings(Constraint, ConstraintSettingsObj)
					for Source in Constraint.SourceList:
						SourceSettingsObj = BlenderUtils.add_empty(f"Constraint_{jcns_file.ConstraintList.index(Constraint)}_SOURCE_{Constraint.SourceList.index(Source)} {Source.Name}", [("TYPE", "JCNS_ConstraintSrcSettings")], ConstraintSettingsObj, filename)
						getConstraintSrcSettings(Source, SourceSettingsObj)
						BlenderUtils.lockObjTransforms(SourceSettingsObj)
					BlenderUtils.lockObjTransforms(ConstraintSettingsObj)
		print("DONE Importing.\n =========================== ")
	else:
		raise ERROR_Unsupported
