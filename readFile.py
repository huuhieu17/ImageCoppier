import os
import shutil
import tkinter as tk
import time
import re
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox
from threading import Thread
import threading
def has_extension(filename):
    # Regular expression to check for an extension
    pattern = r'.+\.[a-zA-Z0-9]+$'
    return bool(re.match(pattern, filename))
def show_splash_screen():
    splash_screen = tk.Toplevel()
    splash_screen.overrideredirect(True)  # Remove window decorations
    splash_screen.geometry("300x200")  # Set size of splash screen window
    # Center splash screen on the screen
    splash_screen.eval('tk::PlaceWindow %s center' % splash_screen.winfo_toplevel())
    
    # Replace 'splash.png' with the path to your splash image
    splash_image = tk.PhotoImage(file="splash.png")
    label = tk.Label(splash_screen, image=splash_image)
    label.pack(pady=10)
    
    # Display splash screen for 2 seconds
    time.sleep(2)
    splash_screen.destroy()

def select_source_folder():
    folder_selected = filedialog.askdirectory()
    source_folder_entry.delete(0, tk.END)
    source_folder_entry.insert(0, folder_selected)

def select_destination_folder():
    folder_selected = filedialog.askdirectory()
    destination_folder_entry.delete(0, tk.END)
    destination_folder_entry.insert(0, folder_selected)

def update_status(message):
    status_text.config(state=tk.NORMAL)
    status_text.insert(tk.END, message + "\n")
    status_text.see(tk.END)
    status_text.config(state=tk.DISABLED)

def copy_files():
    file_names = file_name_search_entry.get().split(',')
    file_search_extension = search_extension_var.get()
    file_extension = file_extension_var.get()
    source_folder = source_folder_entry.get()
    destination_folder = destination_folder_entry.get()

    
    if not file_names or not source_folder or not destination_folder or not file_search_extension or not file_extension:
        messagebox.showerror("Lỗi", "Vui lòng nhập đủ thông tin.")
        return

    if not os.path.exists(source_folder):
        messagebox.showerror("Lỗi", "Thư mục nguồn không tồn tại.")
        return

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    copied_files = 0
    update_status("Bắt đầu tìm kiếm các file...")
    pattern = r"\b\w+\.[a-zA-Z]{2,4}\b"

    for file_name in file_names:
        update_status(f"Bắt đầu: {file_name}")
        if(re.findall(pattern, file_name)) :
            file_name_with_extension = file_name.strip().lower()
        else:
            full_path = file_name+file_search_extension
            file_name_with_extension = full_path.strip().lower()

        for root, dirs, files in os.walk(source_folder):
            for file in files:
                print(file, file_name_with_extension)
                if file.lower() == file_name_with_extension:
                    target_file_name = file
                    if(has_extension(target_file_name)):
                        target_file_name = os.path.splitext(target_file_name)[0]
                    source_target_file = os.path.join(source_folder, target_file_name + file_extension.upper())
                    destination_file = os.path.join(destination_folder, target_file_name + file_extension.upper())
                    if os.path.exists(source_target_file):
                        shutil.copy2(source_target_file, destination_file)
                        copied_files += 1
                        update_status(f"Đã sao chép: {source_target_file} tới {destination_file}")
                    else:
                        update_status(f"Không tìm thấy file RAW: {source_target_file}")
                        

    if copied_files > 0:
        messagebox.showinfo("Thành công", f"Đã sao chép {copied_files} file thành công.")
        update_status(f"Đã sao chép {copied_files} file thành công.")
    else:
        messagebox.showinfo("Không tìm thấy file", "Không tìm thấy file nào khớp với yêu cầu.")
        update_status("Không tìm thấy file nào khớp với yêu cầu.")

def show_main_ui():
    # Tạo giao diện người dùng
    root = tk.Tk()
    root.title("ImageCopy ProMax Vip VCL - Develop By Steve")

    tk.Label(root, text="Tên file:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    global file_name_search_entry
    file_name_search_entry = tk.Entry(root, width=50)
    file_name_search_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Phần mở rộng file:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    global search_extension_var
    search_extension_var = tk.StringVar(root)
    search_extension_var.set(".cr3")  # Giá trị mặc định

    # Danh sách các đuôi file
    file_extensions = [
        ".jpg",".png", ".3fr", ".ari", ".arw", ".bay", ".braw", ".crw", ".cr2", ".cr3", ".cap", ".data", ".dcs", 
        ".dcr", ".dng", ".drf", ".eip", ".erf", ".fff", ".gpr", ".iiq", ".k25", ".kdc", ".mdc", 
        ".mef", ".mos", ".mrw", ".nef", ".nrw", ".obm", ".orf", ".pef", ".ptx", ".pxn", ".r3d", 
        ".raf", ".raw", ".rwl", ".rw2", ".rwz", ".sr2", ".srf", ".srw", ".tif", ".x3f"
    ]

    file_extension_menu = tk.OptionMenu(root, search_extension_var, *file_extensions)
    file_extension_menu.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Thư mục nguồn:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    global source_folder_entry
    source_folder_entry = tk.Entry(root, width=50)
    source_folder_entry.grid(row=2, column=1, padx=10, pady=5)
    tk.Button(root, text="Chọn...", command=select_source_folder).grid(row=2, column=2, padx=10, pady=5)


    tk.Label(root, text="Thư mục đích:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    global destination_folder_entry
    destination_folder_entry = tk.Entry(root, width=50)
    destination_folder_entry.grid(row=3, column=1, padx=10, pady=5)
    tk.Button(root, text="Chọn...", command=select_destination_folder).grid(row=3, column=2, padx=10, pady=5)

    tk.Label(root, text="Phần mở rộng file sao chép:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    global file_extension_var
    file_extension_var = tk.StringVar(root)
    file_extension_var.set(file_extensions[0])  # Giá trị mặc định
    file_extension_menu = tk.OptionMenu(root, file_extension_var, *file_extensions)
    file_extension_menu.grid(row=4, column=1, padx=10, pady=5)

    tk.Button(root, text="Sao chép file", command=copy_files).grid(row=5, column=0, columnspan=3, pady=20)

    # Khung hiển thị trạng thái
    global status_text
    status_text = tk.Text(root, height=10, width=80, state=tk.DISABLED)
    status_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
    root.mainloop()
    
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x_offset = (window.winfo_screenwidth() - width) // 2
    y_offset = (window.winfo_screenheight() - height) // 2
    window.geometry(f"+{x_offset}+{y_offset}")


if __name__ == "__main__":
    show_main_ui()
