class ERROR_Unsupported(Exception):
    def __str__(self): 
        return "Unsupported file version."
    
class ERROR_InvalidFile(Exception):
    def __str__(self): 
        return "Invalid file."
    
class ERROR_NotImplemented(Exception):
    def __str__(self): 
        return "Not implemented."