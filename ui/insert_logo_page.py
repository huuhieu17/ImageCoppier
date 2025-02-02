from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox, QMessageBox, QLineEdit, QSpinBox
)
from PyQt6.QtCore import pyqtSlot
from pathlib import Path
from core.image_utils import ImageUtils

class AddLogoPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Chọn folder ảnh gốc
        self.folder_path_edit = QLineEdit()
        self.folder_path_edit.setPlaceholderText("Chọn folder chứa ảnh gốc...")
        self.folder_browse_btn = QPushButton("Chọn folder ảnh gốc")
        layout.addWidget(QLabel("Folder ảnh gốc:"))
        layout.addWidget(self.folder_path_edit)
        layout.addWidget(self.folder_browse_btn)

        # Chọn logo
        self.logo_path_edit = QLineEdit()
        self.logo_path_edit.setPlaceholderText("Chọn logo...")
        self.logo_browse_btn = QPushButton("Chọn logo")
        layout.addWidget(QLabel("Logo:"))
        layout.addWidget(self.logo_path_edit)
        layout.addWidget(self.logo_browse_btn)

        # Chọn vị trí
        self.position_combo = QComboBox()
        self.position_combo.addItems(["top-left", "top-right", "bottom-left", "bottom-right"])
        layout.addWidget(QLabel("Vị trí logo:"))
        layout.addWidget(self.position_combo)

        # Nhập khoảng cách (spacing)
        self.spacing_input = QSpinBox()
        self.spacing_input.setRange(0, 1000)  # Giới hạn từ 0 đến 1000px
        self.spacing_input.setValue(10)  # Giá trị mặc định
        layout.addWidget(QLabel("Khoảng cách (px):"))
        layout.addWidget(self.spacing_input)
        
          # Chọn định dạng đầu ra
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(["JPEG", "PNG"])
        layout.addWidget(QLabel("Định dạng đầu ra:"))
        layout.addWidget(self.output_format_combo)

        # Nút thực hiện
        self.add_logo_btn = QPushButton("Chèn logo vào tất cả ảnh")
        self.add_logo_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        layout.addWidget(self.add_logo_btn)
        

        # Kết nối sự kiện
        self.folder_browse_btn.clicked.connect(self.browse_folder)
        self.logo_browse_btn.clicked.connect(self.browse_logo)
        self.add_logo_btn.clicked.connect(self.add_logo_to_all_images)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Chọn folder chứa ảnh gốc")
        if folder_path:
            self.folder_path_edit.setText(folder_path)

    def browse_logo(self):
        logo_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn logo (png)", "", "Images (*.png *.jpg *.jpeg)"
        )
        if logo_path:
            self.logo_path_edit.setText(logo_path)

    @pyqtSlot()
    def add_logo_to_all_images(self):
        folder_path = self.folder_path_edit.text()
        logo_path = self.logo_path_edit.text()
        position = self.position_combo.currentText()
        spacing = self.spacing_input.value()
        output_format = self.output_format_combo.currentText().lower()
        
        if not folder_path or not logo_path:
            QMessageBox.critical(self, "Lỗi", "Vui lòng chọn folder ảnh gốc và logo.")
            return

        # Lấy danh sách ảnh trong folder
        image_extensions = ["*.png", "*.jpg", "*.jpeg"]
        image_paths = []
        for ext in image_extensions:
            image_paths.extend(Path(folder_path).glob(ext))

        if not image_paths:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy ảnh trong folder.")
            return

        # Tạo folder lưu ảnh kết quả
        output_folder = Path(folder_path) / "output"
        output_folder.mkdir(exist_ok=True)

        # Chèn logo vào từng ảnh
        success_count = 0
        for image_path in image_paths:
            try:
                output_path = output_folder / f"{image_path.stem}_with_logo.{output_format}"
                ImageUtils.add_logo(str(image_path), logo_path, position, str(output_path), spacing)
                success_count += 1
            except Exception as e:
                print(f"Lỗi khi xử lý ảnh {image_path.name}: {str(e)}")

        # Hiển thị kết quả
        QMessageBox.information(
            self,
            "Hoàn thành",
            f"Đã chèn logo vào {success_count}/{len(image_paths)} ảnh. Kết quả được lưu tại: {output_folder}",
        )