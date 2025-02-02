from pathlib import Path

class Config:
    SUPPORTED_EXTENSIONS = [
        ".jpg",".png", ".3fr", ".ari", ".arw", ".bay", ".braw", ".crw", ".cr2", ".cr3", ".cap", ".data", ".dcs", 
        ".dcr", ".dng", ".drf", ".eip", ".erf", ".fff", ".gpr", ".iiq", ".k25", ".kdc", ".mdc", 
        ".mef", ".mos", ".mrw", ".nef", ".nrw", ".obm", ".orf", ".pef", ".ptx", ".pxn", ".r3d", 
        ".raf", ".raw", ".rwl", ".rw2", ".rwz", ".sr2", ".srf", ".srw", ".tif", ".x3f"
    ]
    
    APP_NAME = "File Copier Pro"
    VERSION = "1.0.0"
    DEFAULT_SOURCE = str(Path.home() / "Pictures")
    DEFAULT_DEST = str(Path.home() / "Desktop/CopiedFiles")