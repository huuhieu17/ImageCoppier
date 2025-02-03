from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
    QStackedWidget, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from ui.copy_image_page import CopyImagePage  # Trang copy ảnh
from ui.image_edit import EditImagePage
from ui.insert_logo_page import AddLogoPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SFoto Tool (1.0.1)")
        self.resize(1000, 800)
        self.init_ui()

    def init_ui(self):
        # Layout chính
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar menu
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #2c3e50;
                color: white;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #34495e;
                font-weight: 700;
                padding: 10px;
                border: 0;
                font-size: 18px;
                outline: none;
            }
        """)
        self.sidebar.addItems(["Copy Ảnh", "Chèn logo", "Sửa ảnh"])  # Thêm các chức năng
        self.sidebar.currentRowChanged.connect(self.change_page)  # Kết nối sự kiện chọn menu

        # Stacked widget để quản lý các trang
        self.stacked_widget = QStackedWidget()

        # Thêm các trang vào stacked widget
        self.copy_image_page = CopyImagePage()  # Trang copy ảnh
        self.insert_logo_page = AddLogoPage()  # Thêm trang chèn logo
        self.edit_image_page = EditImagePage()
        self.stacked_widget.addWidget(self.copy_image_page)
        self.stacked_widget.addWidget(self.insert_logo_page)
        self.stacked_widget.addWidget(self.edit_image_page)  # Trang placeholder

        # Thêm sidebar và stacked widget vào layout chính
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)

        # Đặt widget chính
        self.setCentralWidget(main_widget)

    def change_page(self, index: int):
        """Chuyển trang khi chọn menu"""
        self.stacked_widget.setCurrentIndex(index)