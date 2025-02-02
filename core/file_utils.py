import shutil
import re
from pathlib import Path
from typing import List, Tuple

class FileUtils:
    @staticmethod
    def has_extension(filename: str) -> bool:
        return bool(re.match(r'.+\.[a-zA-Z0-9]+$', filename))

    @staticmethod
    def validate_paths(source: Path, dest: Path) -> Tuple[bool, str]:
        if not source.exists():
            return False, "Thư mục nguồn không tồn tại"
        if not dest.exists():
            dest.mkdir(parents=True, exist_ok=True)
        return True, ""

    @staticmethod
    def generate_new_name(original: Path, new_ext: str) -> Path:
        """Tạo tên file mới với phần mở rộng mới"""
        if not new_ext.startswith("."):
            new_ext = f".{new_ext}"  # Đảm bảo phần mở rộng bắt đầu bằng dấu chấm
        return original.with_suffix(new_ext)