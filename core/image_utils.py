from PIL import Image

class ImageUtils:
    @staticmethod
    def add_logo(image_path: str, logo_path: str, position: str, output_path: str, spacing: int = 10):
        """
        Chèn logo vào ảnh tại vị trí cố định với khoảng cách (spacing).

        :param image_path: Đường dẫn đến ảnh gốc.
        :param logo_path: Đường dẫn đến logo.
        :param position: Vị trí chèn logo ('top-left', 'top-right', 'bottom-left', 'bottom-right').
        :param output_path: Đường dẫn lưu ảnh kết quả.
        :param spacing: Khoảng cách từ logo đến các cạnh (mặc định: 10px).
        """
        # Mở ảnh gốc và logo
        image = Image.open(image_path).convert("RGBA")
        logo = Image.open(logo_path).convert("RGBA")

        # Tính toán vị trí chèn logo với spacing
        image_width, image_height = image.size
        logo_width, logo_height = logo.size

        if position == "top-left":
            position = (spacing, spacing)
        elif position == "top-right":
            position = (image_width - logo_width - spacing, spacing)
        elif position == "bottom-left":
            position = (spacing, image_height - logo_height - spacing)
        elif position == "bottom-right":
            position = (image_width - logo_width - spacing, image_height - logo_height - spacing)
        else:
            raise ValueError("Vị trí không hợp lệ. Chọn từ: 'top-left', 'top-right', 'bottom-left', 'bottom-right'.")

        # Chèn logo vào ảnh
        image.paste(logo, position, logo)

         # Chuyển đổi ảnh từ RGBA sang RGB nếu định dạng đầu ra là JPEG
        if output_path.lower().endswith(".jpg") or output_path.lower().endswith(".jpeg"):
            image = image.convert("RGB")

        # Lưu ảnh kết quả
        image.save(output_path)