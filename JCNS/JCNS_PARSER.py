import struct
from .UTILS import BinaryUtils, Vec4, Version2GameDict
from .EXCEPTIONS import ERROR_InvalidFile

class FileBufferJCNS:
    def __init__(self, data):
        self.cursor = 0
        self.data = data
        self.version = 0

    def read(self, data_type, data_size):
        result = struct.unpack(data_type, self.data[self.cursor:self.cursor+data_size])[0]
        self.cursor += data_size
        return result
    def seek(self, offset, /, *, relative = False, isTargetAnOffset = False):
        if not relative:
            self.cursor = offset
        else:
            self.cursor += offset
        if isTargetAnOffset:
            self.cursor = self.read("Q", 8)
    def tell(self):
        return self.cursor
    def write(self, data_type, data_to_write):
        if type(data_to_write) == list or type(data_to_write) == tuple:
            self.data += struct.pack(str(len(data_to_write))+data_type, *data_to_write)
        else:
            self.data += struct.pack(data_type, *data_to_write)

class FileJCNS:
    def __init__(self):
        self.Version              =  0
        self.Signature            =  0
        # Skipped a few data. They are usually the same in most files.
        
        self.FileEntry            =  0
        self.ExtraJointEntry      =  0
        self.ConstraintEntry      =  0
        self.SimpleCnsTableEntry  =  0
        self.SimpleCnsHashEntry   =  0
        self.AimCnsTableEntry     =  0
        self.SectionTypeEntry     =  0
        self.ReferenceTableEntry  =  0

        self.ExtraJointCount      =  0
        self.ConstraintCount      =  0
        self.ConstraintEnd        =  0
        self.ReferenceCount       =  0
        self.SimpleCnsCount       =  0
        self.SimpleCnsHashCount   =  0
        self.AimConstraintCount   =  0
        self.SettingCount         =  0

        self.ExtraJointList       =  []
        self.ConstraintList       =  []
        self.ReferenceList        =  []
        self.SimpleCnsList        =  []
        self.SimpleCnsHashList    =  []
        self.AimConstraintList    =  []


    def read(self, FileBuffer: FileBufferJCNS):
        self.Version            =  BinaryUtils.readUInt32(FileBuffer)
        self.Signature          =  BinaryUtils.readUInt32(FileBuffer)
        if not self.Version in Version2GameDict and self.Signature == 1936614250: 
            raise ERROR_InvalidFile
        FileBuffer.version      =  self.Version
        ## Usually we don't need these info, since they are the same in most jcns files.
        ## However, if they're proved necessary, just uncomment this part to make it work!
        ## (And maybe have to do some fixes)
        # self.UnknownQWORD1      = BinaryUtils.readUInt64(FileBuffer)
        # self.InfoEntry          = BinaryUtils.readUInt64(FileBuffer)
        # self.UnknownQWORD2      = BinaryUtils.readUInt64(FileBuffer)
        # FileBuffer.seek(self.InfoEntry)
        # self.UnknownQWORD3      = BinaryUtils.readUInt64(FileBuffer)
        # self.UnknownQWORD4      = BinaryUtils.readUInt64(FileBuffer)
        FileBuffer.cursor += 24
        # This shall be the same in most files too.
        # But we don't know if there will be a weirdo likes to move the entries...
        # Doing this just in case.
        self.FileEntry          =  BinaryUtils.readUInt64(FileBuffer)
        FileBuffer.seek(self.FileEntry, isTargetAnOffset=True)

        self.ExtraJointEntry          =  BinaryUtils.readUInt64(FileBuffer)
        self.ConstraintEntry          =  BinaryUtils.readUInt64(FileBuffer)
        self.ConstraintEnd            =  BinaryUtils.readUInt64(FileBuffer)
        FileBuffer.cursor += 16 + 8 * (FileBuffer.version <= 12)
        if FileBuffer.version >= 16:
            self.SimpleCnsTableEntry      =  BinaryUtils.readUInt64(FileBuffer)
            self.SimpleCnsHashEntry       =  BinaryUtils.readUInt64(FileBuffer)
            if self.Version == 29:    #  Not sure the first appeared version.
                self.AimCnsTableEntry     =  BinaryUtils.readUInt64(FileBuffer)
            FileBuffer.cursor += 8 * (self.Version >= 22) + 8 * (self.Version == 29)
            self.SectionTypeEntry         =  BinaryUtils.readUInt64(FileBuffer)
            if self.Version > 16:
                self.ReferenceTableEntry  =  BinaryUtils.readUInt64(FileBuffer)

        self.ExtraJointCount          =  BinaryUtils.readUInt16(FileBuffer)
        self.ConstraintCount          =  BinaryUtils.readUInt16(FileBuffer)
        if self.Version > 16:
            self.ReferenceCount       =  BinaryUtils.readUInt16(FileBuffer)
        if self.Version == 29:
            FileBuffer.cursor += 6
            self.SimpleCnsCount       =  BinaryUtils.readUInt16(FileBuffer)
            self.SimpleCnsHashCount   =  BinaryUtils.readUInt16(FileBuffer)
            self.AimCnsCount          =  BinaryUtils.readUInt16(FileBuffer)
            self.SettingCount         =  BinaryUtils.readUInt16(FileBuffer)

        FileBuffer.seek(self.ExtraJointEntry)
        for _ in range(self.ExtraJointCount):
            ExtraJoint = ExtraJointInfo()
            ExtraJoint.read(FileBuffer)
            self.ExtraJointList.append(ExtraJoint)
        FileBuffer.seek(self.ConstraintEntry)
        for _ in range(self.ConstraintCount):
            #print("Parsing constraint {}...".format(_))
            #print("Current file cursor: {}".format(FileBuffer.cursor))
            Constraint = ConstraintInfo()
            Constraint.read(FileBuffer)
            self.ConstraintList.append(Constraint)

    def printDebugInfo(self):
        print(
            f"""
            [JCNS INFO]
            Version: {self.Version}
            Signature: {self.Signature}
            FileEntry: {self.FileEntry}
            ExtraJointEntry: {self.ExtraJointEntry}
            ConstraintEntry: {self.ConstraintEntry}
            ConstraintEnd: {self.ConstraintEnd}
            SimpleCnsTableEntry: {self.SimpleCnsTableEntry}
            SimpleCnsHashEntry: {self.SimpleCnsHashEntry}
            AimCnsTableEntry:{self.AimCnsTableEntry}
            SectionTypeEntry: {self.SectionTypeEntry}
            ReferenceTableEntry: {self.ReferenceTableEntry}
            ExtraJointCount: {self.ExtraJointCount}
            ConstraintCount: {self.ConstraintCount}
            ReferenceCount: {self.ReferenceCount}
            SimpleCnsCount: {self.SimpleCnsCount}
            SimpleCnsHashCount: {self.SimpleCnsHashCount}
            AimConstraintCount: {self.AimConstraintCount}
            SettingCount: {self.SettingCount}
            """
        )
    def getProperties(self):
        return [
            self.Version
        ]

class ExtraJointInfo:
    def __init__(self):
        self.Name  =  ""
        self.Bones = []
    def read(self, FileBuffer: FileBufferJCNS):
        self.Name  = ""
        
class ConstraintInfo:
    def __init__(self):
        self.StandaloneCnsInfoOffset  =  0
        self.SourceTableOffset        =  0

        self.ObjectName               =  ""
        self.MaterialProperty         =  ""
        
        self.StandaloneCnsInfoCount   =  0
        self.SourceCount              =  0
        self.UNKNOWN_1                =  0  # Mix?
        self.TransformationType       =  0
        self.UNKNOWN_2                =  0
        self.TransformationAxis       =  0
        self.UNKNOWN_3                =  0
        self.UNKNOWN_4                =  0
        self.UNKNOWN_5_Vec4           =  Vec4()

        self.UNKNOWN_6                =  0

        self.ExtraInfoList            =  []
        self.SourceList               =  []

    def read(self, FileBuffer: FileBufferJCNS):
        self.ExtraInfoOffset     =  BinaryUtils.readUInt64(FileBuffer)
        self.SourceInfoOffset    =  BinaryUtils.readUInt64(FileBuffer)
        self.ObjectName          =  BinaryUtils.readWString(FileBuffer, isOffset=True)
        #print("Object Name: {}".format(self.ObjectName))
        if (FileBuffer.version >= 16):
            self.MaterialProperty    =  BinaryUtils.readWString(FileBuffer, isOffset=True)
            #print("Material Property: {}".format(self.MaterialProperty))
        FileBuffer.cursor += 8
        self.ExtraInfoCount      =  BinaryUtils.readUInt8(FileBuffer)
        self.SourceCount         =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_1           =  BinaryUtils.readUInt8(FileBuffer)  # Mix?
        self.TransformationType  =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_2           =  BinaryUtils.readUInt8(FileBuffer)
        self.TransformationAxis  =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_3           =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_4           =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_5           =  Vec4(BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer))
        self.EndPos              =  FileBuffer.tell() + 16 * (FileBuffer.version >= 21)

        if FileBuffer.version == 29:
            FileBuffer.cursor += 9
            self.UNKNOWN_6       =  BinaryUtils.readUInt8(FileBuffer)
        FileBuffer.seek(self.ExtraInfoOffset)
        #for _ in range(self.ExtraInfoCount):
        #    ExtraInfo = ExtraConstraintInfo()
        #    ExtraInfo.read(FileBuffer)
        #    self.ExtraInfoList.append(ExtraInfo)
        FileBuffer.seek(self.SourceInfoOffset)
        for _ in range(self.SourceCount):
            #print("Parsing constraint source {}...".format(_))
            #print("Current file cursor: {}".format(FileBuffer.cursor))
            Source = ConstraintSource_V2() if FileBuffer.version >= 16 else ConstraintSource_V1()
            Source.read(FileBuffer)
            self.SourceList.append(Source)

        FileBuffer.seek(self.EndPos)
    
    def getProperties(self):
        return [
            self.ObjectName, 
            self.MaterialProperty, 
            self.UNKNOWN_1, 
            self.TransformationType, 
            self.UNKNOWN_2, 
            self.TransformationAxis,
            self.UNKNOWN_3,
            self.UNKNOWN_4,
            self.UNKNOWN_5,
        ]
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class ExtraConstraintInfo: 
    def __init__(self):
        self.UNKNOWN_1  =  0
        self.UNKNOWN_2  =  0
        self.UNKNOWN_3  =  0
        self.UNKNOWN_4  =  0
        self.UNKNOWN_5  =  0
        self.UNKNOWN_6  =  0
    def read(self, FileBuffer: FileBufferJCNS):
        self.UNKNOWN_1  =  BinaryUtils.readFloat32(FileBuffer)
        self.UNKNOWN_2  =  BinaryUtils.readFloat32(FileBuffer)
        self.UNKNOWN_3  =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_4  =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_5  =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_6  =  BinaryUtils.readUInt8(FileBuffer)

class ConstraintSource_V2:
    def __init__(self):
        self.ExtraInfoOffset     =  0
        self.Name                =  ""

        self.ExtraInfoCount      =  0
        self.TransformationType  =  0
        self.UNKNOWN_1           =  0
        self.TransformationAxis  =  0
        self.UNKNOWN_2           =  0
        self.UNKNOWN_3           =  0
        self.UNKNOWN_4           =  0
        self.UNKNOWN_5           =  0
        self.UNKNOWN_6           =  0

        self.FromRange           =  []
        self.ToRange             =  []
        self.UNKNOWN_7           =  Vec4()

        self.ExtraInfoList       =  []

    def read(self, FileBuffer: FileBufferJCNS):
        self.ExtraInfoOffset     =  BinaryUtils.readUInt64(FileBuffer)
        self.Name                =  BinaryUtils.readWString(FileBuffer, isOffset=True)
        FileBuffer.cursor += 4
        self.ExtraInfoCount      =  BinaryUtils.readUInt32(FileBuffer)
        self.TransformationType  =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_1           =  BinaryUtils.readUInt8(FileBuffer)
        self.TransformationAxis  =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_2           =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_3           =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_4           =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_5           =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_6           =  BinaryUtils.readUInt8(FileBuffer)
        self.FromRange           =  [BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer)]
        self.ToRange             =  [BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer)]
        self.UNKNOWN_7           =  Vec4(BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer))
        self.EndPos              =  FileBuffer.tell()

        FileBuffer.seek(self.ExtraInfoOffset)
        for _ in range(self.ExtraInfoCount):
            ExtraInfo = ExtraSourceInfo()
            ExtraInfo.read()
            self.ExtraInfoList.append(ExtraInfo)
        
        FileBuffer.seek(self.EndPos)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class ConstraintSource_V1:
    def __init__(self):
        self.Name                =  ""
        self.FromRange           =  []
        self.ToRange             =  []
        self.UNKNOWN_1           =  0
        self.TransformationType  =  0
        self.TransformationAxis  =  0
        self.UNKNOWN_2           =  0
        self.UNKNOWN_3           =  0
        self.UNKNOWN_4           =  0
        self.UNKNOWN_5           =  0
        self.UNKNOWN_6           =  0
        self.UNKNOWN_7           =  Vec4()

    def read(self, FileBuffer: FileBufferJCNS):
        self.Name                =  BinaryUtils.readWString(FileBuffer, isOffset=True)
        FileBuffer.cursor += 4
        self.FromRange           =  [BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer)]
        self.ToRange             =  [BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer)]
        self.UNKNOWN_1           =  BinaryUtils.readUInt8(FileBuffer)
        self.TransformationType  =  BinaryUtils.readUInt8(FileBuffer)
        self.TransformationAxis  =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_2           =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_3           =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_4           =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_5           =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_6           =  BinaryUtils.readUInt8(FileBuffer)
        self.UNKNOWN_7           =  Vec4(BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer), BinaryUtils.readFloat32(FileBuffer))
        FileBuffer.cursor += 4

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class ExtraSourceInfo: 
    def __init__(self):
        self.UNKNOWN_1  =  0.0
        self.UNKNOWN_2  =  0.0
        self.UNKNOWN_3  =  0.0
        self.UNKNOWN_4  =  0.0
        self.UNKNOWN_5  =  0.0
        self.UNKNOWN_6  =  0.0
        self.UNKNOWN_7  =  0
    def read(self, FileBuffer: FileBufferJCNS):
        self.UNKNOWN_1  =  BinaryUtils.readFloat32(FileBuffer)
        self.UNKNOWN_2  =  BinaryUtils.readFloat32(FileBuffer)
        self.UNKNOWN_3  =  BinaryUtils.readFloat32(FileBuffer)
        self.UNKNOWN_4  =  BinaryUtils.readFloat32(FileBuffer)
        self.UNKNOWN_5  =  BinaryUtils.readFloat32(FileBuffer)
        self.UNKNOWN_6  =  BinaryUtils.readFloat32(FileBuffer)
        self.UNKNOWN_7  =  BinaryUtils.readUInt32(FileBuffer)