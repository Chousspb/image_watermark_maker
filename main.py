from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from dotenv import load_dotenv

load_dotenv()

source_directory_path = "Source_folder"
destination_directory_path = "Output_folder"

watermark_text = os.getenv("TEXT")
font = ImageFont.truetype("/Users/Admin/image_watermark/Philosopher.ttf", size=50)

for filename in os.listdir(source_directory_path):
    if os.path.isfile(os.path.join(source_directory_path, filename)) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        image = Image.open(os.path.join(source_directory_path, filename))
        if "exif" in image.info:
            image = ImageOps.exif_transpose(image)
        draw = ImageDraw.Draw(image)

        text_box = draw.textbbox((0, 0), watermark_text, font=font)


        x_reps = int(image.width / (text_box[2] * 2)) + 1
        y_reps = int(image.height / (text_box[3] * 2)) + 1

        watermark = Image.new("RGBA", (text_box[2] * x_reps, text_box[3] * y_reps), (0, 0, 0, 0))

        watermark_draw = ImageDraw.Draw(watermark)

        for i in range(x_reps):
            for j in range(y_reps):
                watermark_draw.text((i * text_box[2] * 2, j * text_box[3] * 2), watermark_text, font=font, fill=(255, 255, 255, 128))

        watermark = watermark.resize(image.size)
        watermark = watermark.convert(image.mode)
        image = Image.blend(image, watermark, alpha=0.035)
        if "exif" in image.info:
            image = ImageOps.exif_transpose(image)

        image.save(os.path.join(destination_directory_path, filename))

