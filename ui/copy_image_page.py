from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox, QLineEdit, QComboBox, QHBoxLayout
from PyQt6.QtCore import pyqtSlot, QThread
from core.worker import FileWorker
from core.file_utils import FileUtils
from config import Config

class CopyImagePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker = None
        self.setup_connections()
    
    def init_ui(self):
        layout = QVBoxLayout(self)

        # File Input Section
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Nhập tên file (cách nhau bằng dấu phẩy)")
        
        # Extension Selection
        self.src_ext_combo = QComboBox()
        self.dest_ext_combo = QComboBox()
        self.src_ext_combo.addItems(Config.SUPPORTED_EXTENSIONS)
        self.dest_ext_combo.addItems(Config.SUPPORTED_EXTENSIONS)

        # Path Selection
        self.src_path_edit = QLineEdit(Config.DEFAULT_SOURCE)
        self.dest_path_edit = QLineEdit(Config.DEFAULT_DEST)
        
        # Buttons
        self.src_browse_btn = QPushButton("Chọn...")
        self.dest_browse_btn = QPushButton("Chọn...")
        self.start_btn = QPushButton("Bắt đầu sao chép")
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white;")

        # Status Area
        self.status_area = QTextEdit()
        self.status_area.setReadOnly(True)

        # Layout Assembly
        layout.addWidget(QLabel("Tên file:"))
        layout.addWidget(self.file_input)
        
        ext_layout = QHBoxLayout()
        ext_layout.addWidget(QLabel("Đuôi nguồn:"))
        ext_layout.addWidget(self.src_ext_combo)
        ext_layout.addWidget(QLabel("Đuôi đích:"))
        ext_layout.addWidget(self.dest_ext_combo)
        layout.addLayout(ext_layout)

        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Thư mục nguồn:"))
        path_layout.addWidget(self.src_path_edit)
        path_layout.addWidget(self.src_browse_btn)
        layout.addLayout(path_layout)

        dest_path_layout = QHBoxLayout()
        dest_path_layout.addWidget(QLabel("Thư mục đích:"))
        dest_path_layout.addWidget(self.dest_path_edit)
        dest_path_layout.addWidget(self.dest_browse_btn)
        layout.addLayout(dest_path_layout)

        layout.addWidget(self.start_btn)
        layout.addWidget(QLabel("Trạng thái:"))
        layout.addWidget(self.status_area)

    def setup_connections(self):
        self.src_browse_btn.clicked.connect(self.browse_source)
        self.dest_browse_btn.clicked.connect(self.browse_dest)
        self.start_btn.clicked.connect(self.start_processing)  # Kết nối nút "Bắt đầu sao chép"

    def browse_source(self):
        path = QFileDialog.getExistingDirectory(self, "Chọn thư mục nguồn")
        if path:
            self.src_path_edit.setText(path)

    def browse_dest(self):
        path = QFileDialog.getExistingDirectory(self, "Chọn thư mục đích")
        if path:
            self.dest_path_edit.setText(path)

    @pyqtSlot()
    def start_processing(self):
        # Validation logic
        source = Path(self.src_path_edit.text())
        dest = Path(self.dest_path_edit.text())
        
        valid, msg = FileUtils.validate_paths(source, dest)
        if not valid:
            QMessageBox.critical(self, "Lỗi", msg)
            return
        
        # Prepare parameters
        params = {
            'source': source,
            'dest': dest,
            'file_names': self.file_input.text().split(','),
            'src_ext': self.src_ext_combo.currentText(),
            'dest_ext': self.dest_ext_combo.currentText()
        }
        
        # Create worker thread
        self.worker = FileWorker()
        self.worker_thread = QThread()
        
        # Connect signals
        self.worker.message.connect(self.update_status)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        
        # Start processing
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(lambda: self.worker.process_files(params))
        self.worker_thread.start()

    def update_status(self, message: str):
        self.status_area.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def on_finished(self):
        self.worker_thread.quit()
        self.worker_thread.wait()
        QMessageBox.information(self, "Hoàn thành", "Đã sao chép xong tất cả file!")

    def on_error(self, message: str):
        QMessageBox.critical(self, "Lỗi", message)
        self.worker_thread.quit()