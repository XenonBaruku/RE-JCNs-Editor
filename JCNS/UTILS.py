import bpy
import struct
import numpy as np
#import re

class Vec3:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z =  x, y, z
    def toTuple(self, /, *, magnitude=1.0): return tuple((self.x / magnitude, self.y / magnitude, self.z / magnitude))
    def swapYZ(self): self.y, self.z = self.z, self.y
class Vec4:
    def __init__(self, x = 0, y = 0, z = 0, w = 0):
        self.x, self.y, self.z, self.w =  x, y, z, w
    def toTuple(self, /, *, magnitude=1.0): return tuple((self.x / magnitude, self.y / magnitude, self.z / magnitude, self.w / magnitude))
    def swapYZ(self): self.y, self.z = self.z, self.y

class BinaryUtils:
    def read(FileBuffer, data_type, data_size):
        ret = struct.unpack(data_type, FileBuffer.data[FileBuffer.cursor:FileBuffer.cursor+data_size])[0]
        FileBuffer.cursor += data_size
        return ret
    def seek(FileBuffer, offset, /, *, relative = False, isTargetAnOffset = False):
        if not relative:
            FileBuffer.cursor = offset
        else:
            FileBuffer.cursor += offset
        if isTargetAnOffset:
            FileBuffer.cursor = FileBuffer.read("Q", 8)
    def tell(FileBuffer):
        return FileBuffer.cursor

    def readInt8(FileBuffer):    return FileBuffer.read("b", 1)
    def readUInt8(FileBuffer):   return FileBuffer.read("B", 1)
    def readInt16(FileBuffer):   return FileBuffer.read("h", 2)
    def readUInt16(FileBuffer):  return FileBuffer.read("H", 2)
    def readInt32(FileBuffer):   return FileBuffer.read("i", 4)
    def readUInt32(FileBuffer):  return FileBuffer.read("I", 4)
    def readInt64(FileBuffer):   return FileBuffer.read("q", 8)
    def readUInt64(FileBuffer):  return FileBuffer.read("Q", 8)
    def readFloat32(FileBuffer): return FileBuffer.read("f", 4)
    def readWString(FileBuffer, isOffset = False):
        WSTR = ""
        if isOffset:
            Offset = FileBuffer.read("Q", 8)
            if Offset == 0: return None
            ReturnPos = FileBuffer.tell()
            FileBuffer.seek(Offset) 
        while(True):
            char = FileBuffer.read("H", 2)
            if char != 0:
                WSTR += chr(char)
            else:
                break
        if isOffset:
            FileBuffer.seek(ReturnPos)
        return WSTR
    
class HashUtils:
    def generate_murmurhash_32(key, seed = 0xFFFFFFFF):
        if type(key) == str:
            key = key.encode("utf-16LE")
        def fmix(h):
            h ^= h >> 16
            h  = (h * 0x85ebca6b) & seed
            h ^= h >> 13
            h  = (h * 0xc2b2ae35) & seed
            h ^= h >> 16
            return h
        length = len(key)
        nblocks = int(length / 4)
        h1 = seed
        c1 = 0xcc9e2d51
        c2 = 0x1b873593
        for block_start in range(0, nblocks * 4, 4):
            k1 = key[block_start + 3] << 24 | \
                 key[block_start + 2] << 16 | \
                 key[block_start + 1] <<  8 | \
                 key[block_start + 0]
            k1 = (c1 * k1) & seed
            k1 = (k1 << 15 | k1 >> 17) & seed
            k1 = (c2 * k1) & seed
            h1 ^= k1
            h1 = (h1 << 13 | h1 >> 19) & seed
            h1 = (h1 * 5 + 0xe6546b64) & seed
        tail_index = nblocks * 4
        k1 = 0
        tail_size = length & 3
        if tail_size >= 3:
            k1 ^= key[tail_index + 2] << 16
        if tail_size >= 2:
            k1 ^= key[tail_index + 1] << 8
        if tail_size >= 1:
            k1 ^= key[tail_index + 0]
        if tail_size > 0:
            k1 = (k1 * c1) & seed
            k1 = (k1 << 15 | k1 >> 17) & seed
            k1 = (k1 * c2) & seed
            h1 ^= k1
        unsigned_val = fmix(h1 ^ length)
        return unsigned_val

class BlenderUtils:
    def getCollection(collectionName,parentCollection = None,makeNew = False):
        if makeNew or not bpy.data.collections.get(collectionName):
            collection = bpy.data.collections.new(collectionName)
            collectionName = collection.name
            if parentCollection != None:
                parentCollection.children.link(collection)
            else:
                bpy.context.scene.collection.children.link(collection)
        return bpy.data.collections[collectionName]

    def getJCNSCollection(CollectionName):
        try:
            # JCNS Specific
            parentCollection = CollectionName.split(".")[0]
            for suffix in JCNS_suffix_List:
                if suffix in parentCollection.upper():
                    parentCollection = parentCollection.split(suffix)[0]
                    parentCollection = parentCollection.split(suffix.casefold())[0]
            parentCollection = bpy.data.collections.get(parentCollection)

            collection = BlenderUtils.getCollection(CollectionName, parentCollection)
        except: 
            collection = BlenderUtils.getCollection(CollectionName)
        return collection

    def add_empty(name, propertyList, parent = None, collection = None, display_size = 0.01, display_type = 0):
            type_list = ['PLAIN_AXES', 'ARROWS', 'CIRCLE', 'CUBE', 'SPHERE']
            obj = bpy.data.objects.new( name, None )
            obj.empty_display_size = display_size
            obj.empty_display_type = type_list[display_type]
            obj.parent = parent
            for property in propertyList:
                obj[property[0]] = property[1]
                
            if collection == None:
                collection = bpy.context.scene.collection
            else:
                collection = BlenderUtils.getJCNSCollection(collection)

            collection.objects.link(obj)

            return obj
    
    def lockObjTransforms(obj,lockLocation = True,lockRotation = True,lockScale = True):
        if lockLocation:
            constraint = obj.constraints.new(type = "LIMIT_LOCATION")
            constraint.use_min_x = True
            constraint.use_min_y = True
            constraint.use_min_z = True
            
            constraint.use_max_x = True
            constraint.use_max_y = True
            constraint.use_max_z = True
        if lockRotation:
            constraint = obj.constraints.new(type = "LIMIT_ROTATION")
            constraint.use_limit_x = True
            constraint.use_limit_y = True
            constraint.use_limit_z = True
        
        if lockScale:
            constraint = obj.constraints.new(type = "LIMIT_SCALE")
            constraint.use_min_x = True
            constraint.use_min_y = True
            constraint.use_min_z = True
            
            constraint.use_max_x = True
            constraint.use_max_y = True
            constraint.use_max_z = True
            
            constraint.min_x = 1.0
            constraint.max_x = 1.0
            constraint.min_y = 1.0
            constraint.max_y = 1.0
            constraint.min_z = 1.0
            constraint.max_z = 1.0

    def getBoneGlobalCoordinates(bone_name, armature_name):
        R = bpy.data.objects[armature_name].matrix_world.to_3x3()
        R = np.array(R)

        t = bpy.data.objects[armature_name].matrix_world.translation
        t = np.array(t) 

        local_location = bpy.data.objects[armature_name].data.bones[bone_name].head_local
        local_location = np.array(local_location)

        loc = np.dot(R, local_location) + t 

        return [loc[0], loc[1], loc[2]]

Version2GameDict = {
    11: "RE2R",
    12: "RE3R",
	16: "RE8",
	21: "MHRS",
	22: "RE4R",
	29: "MHWILDS"
	}
JCNS_suffix_List = [
    #"_[Hh][Jj]", "_[Ss][Cc]", "_[Cc][Ss]", "_[Rr][Ss]", "_[Dd][Rr][Vv]"
    "_HJ", "_JC",  
    "_SC", "_CS", 
    "_BS", 
    "_MB", #"_MBLEND", 
    "_RE", #"_RE00", "_RE01", "_RE1", 
    "_RS", #"_RS00", "_RS01", "_RS1", "_RS02", "_RS2", "_RS3", "_RS4", 
    "_AIM", 
    "_DRV", 
    "_DP", "_WST_ARM_DP", 
    "_ZIPPERCOPY",
    "_SKIRT", #"_SKIRT_ARMOR", 
]