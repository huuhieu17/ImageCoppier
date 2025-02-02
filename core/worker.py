from PyQt6.QtCore import QObject, pyqtSignal, QCoreApplication
from pathlib import Path
import shutil
import re
from typing import List, Dict
from datetime import datetime
from core.file_utils import FileUtils

class FileWorker(QObject):
    # Signals
    progress = pyqtSignal(int, int)  # current, total
    message = pyqtSignal(str)        # status messages
    file_copied = pyqtSignal(str, str)  # source, destination
    finished = pyqtSignal()
    error = pyqtSignal(str)
    cancelled = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._is_running = False
        self._should_cancel = False

    def process_files(self, params: Dict):
        """Main processing function"""
        try:
            self._is_running = True
            self._should_cancel = False
            
            # Extract parameters
            source_dir = Path(params['source'])
            dest_dir = Path(params['dest'])
            file_names = params['file_names']
            src_ext = params['src_ext']
            dest_ext = params['dest_ext']
            
            # Validate paths
            valid, msg = FileUtils.validate_paths(source_dir, dest_dir)
            if not valid:
                self.error.emit(msg)
                return
            
            # Get file list based on input
            if not file_names or all(name.strip() == '' for name in file_names):
                # Process all files with source extension
                files_to_process = self._get_all_files(source_dir, src_ext)
            else:
                # Process specific files
                files_to_process = self._get_specific_files(source_dir, file_names, src_ext)
            
            total_files = len(files_to_process)
            if total_files == 0:
                self.message.emit("Không tìm thấy file phù hợp nào.")
                return
            
            # Process files
            self.message.emit(f"Bắt đầu xử lý {total_files} file...")
            processed_files = 0
            
            for src_file in files_to_process:
                if self._should_cancel:
                    self.cancelled.emit()
                    return
                
                 # Gửi signal và xử lý ngay lập tức
                self.message.emit(f"Đang copy: {src_file.name}")
                QCoreApplication.processEvents()  # Cập nhật UI ngay lập tức
                # Generate destination path
                dest_file = dest_dir / FileUtils.generate_new_name(Path(src_file.name), dest_ext)
                
                # Check if file exists
                if dest_file.exists():
                    self.message.emit(f"File đã tồn tại: {dest_file.name}")
                    continue
                
                # Copy file
                try:
                    shutil.copy2(src_file, dest_file)
                    processed_files += 1
                    self.file_copied.emit(str(src_file), str(dest_file))
                    self.progress.emit(processed_files, total_files)
                    self.message.emit(f"Đã copy: {src_file.name} -> {dest_file.name}")
                except Exception as e:
                    self.message.emit(f"Lỗi khi copy {src_file.name}: {str(e)}")
            
            self.message.emit(f"Hoàn thành! Đã xử lý {processed_files}/{total_files} file.")
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(f"Lỗi hệ thống: {str(e)}")
        finally:
            self._is_running = False

    def _get_all_files(self, directory: Path, extension: str) -> List[Path]:
        """Get all files with specified extension"""
        return list(directory.rglob(f"*{extension}"))

    def _get_specific_files(self, directory: Path, file_names: List[str], extension: str) -> List[Path]:
        """Get specific files based on input names"""
        files_to_process = []
        
        for name in file_names:
            name = name.strip()
            if not name:
                continue
                
            if FileUtils.has_extension(name):
                # Search for exact filename
                pattern = re.compile(re.escape(name), re.IGNORECASE)
            else:
                # Search for files starting with name and having correct extension
                pattern = re.compile(re.escape(name) + r'.*' + re.escape(extension) + r'$', re.IGNORECASE)
            
            # Find matching files
            for file_path in directory.rglob('*'):
                if pattern.match(file_path.name):
                    files_to_process.append(file_path)
        
        return files_to_process

    def cancel(self):
        """Request cancellation of current operation"""
        if self._is_running:
            self._should_cancel = True
            self.message.emit("Đang dừng tiến trình...")