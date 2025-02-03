import base64
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFileDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QUrl, QEvent, QObject, pyqtSlot
import subprocess

from flask import json


class Bridge(QObject):
    def __init__(self):
        super().__init__()
        self.selected_folder = None

    @pyqtSlot(result=str)
    def chooseFolder(self):
        """Hiển thị hộp thoại chọn thư mục và trả về đường dẫn"""
        folder = QFileDialog.getExistingDirectory(None, "Chọn thư mục để lưu ảnh")
        if folder:
            self.selected_folder = folder
            return folder
        return ""

    @pyqtSlot(str)
    def receiveFromJS(self, image_data):
        """Nhận dữ liệu ảnh từ HTML và lưu vào thư mục"""
        if not self.selected_folder:
            print("⚠️ Chưa chọn thư mục!")
            return

        parseData = json.loads(image_data)
        fileName = parseData['fileName']
        data = parseData['data']
        
        file_path = f"{self.selected_folder}/{fileName}"
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(data.split(",")[1]))  # Giải mã Base64
    

        print(f"✅ Ảnh đã lưu tại: {file_path}")
        
class EditImagePage(QWidget):
    def __init__(self):
        super().__init__()
        self.start_server()
        self.init_ui()
        self.view = None
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        # Start Flask server
        # Create QWebEngineView to display Pintura editor
        self.view = QWebEngineView()
        self.view.setUrl(QUrl("http://localhost:5000"))
        self.channel = QWebChannel()
        self.bridge = Bridge()
        self.channel.registerObject("qtBridge", self.bridge)
        self.view.page().setWebChannel(self.channel)
    
        layout.addWidget(self.view)
    
    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.save_folder = folder
            return self.save_folder
        return None

    def start_server(self):
        subprocess.Popen(["python", "server/server.py"])
