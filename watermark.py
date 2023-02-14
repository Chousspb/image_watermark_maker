from PIL import Image, ImageDraw, ImageFont
import os

source_directory_path = "Source_folder"
destination_directory_path = "Output_folder"

watermark_text = "t.me/shmeksiutka_bot "
font = ImageFont.truetype("/Users/Admin/image_watermark/Philosopher.ttf", size=80)

for filename in os.listdir(source_directory_path):
    if os.path.isfile(os.path.join(source_directory_path, filename)) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        image = Image.open(os.path.join(source_directory_path, filename))

        draw = ImageDraw.Draw(image)

        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)

        x_reps = int(image.width / text_bbox[2]) + 1
        y_reps = int(image.height / text_bbox[3]) + 1

        watermark = Image.new("RGBA", (text_bbox[2] * x_reps, text_bbox[3] * y_reps), (0, 0, 0, 0))

        watermark_draw = ImageDraw.Draw(watermark)

        for i in range(x_reps):
            for j in range(y_reps):
                x = i * text_bbox[2]
                y = j * text_bbox[3]
                watermark_draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

        watermark = watermark.resize(image.size)
        watermark = watermark.convert(image.mode)
        image = Image.blend(image, watermark, alpha=0.05)

        image.save(os.path.join(destination_directory_path, filename))
