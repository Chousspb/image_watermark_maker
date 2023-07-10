from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from dotenv import load_dotenv
import time

start = time.time()

load_dotenv()

source_directory_path = "Source_folder"
destination_directory_path = "Output_folder"

watermark_text = os.getenv("TEXT")  # Текст водяного знака
font = ImageFont.truetype("/Users/Admin/image_watermark/Philosopher.ttf", size=60)  # Путь к шрифту и размер шрифта

for filename in os.listdir(source_directory_path):  # Перебор файлов в папке
    if os.path.isfile(os.path.join(source_directory_path, filename)) and filename.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.gif', '.HEIC')):  # Проверка на файл и расширение
        image = Image.open(os.path.join(source_directory_path, filename))  # Открытие файла
        if "exif" in image.info:  # Проверка на EXIF
            image = ImageOps.exif_transpose(image)  # Поворот изображения
        draw = ImageDraw.Draw(image)  # Создание объекта для рисования

        text_box = draw.textbbox((0, 0), watermark_text, font=font)  # Получение размера текста

        x_reps = int(image.width / (text_box[2] * 1.5)) + 1  # Количество повторений по горизонтали
        y_reps = int(image.height / (text_box[3] * 1.5)) + 1  # Количество повторений по вертикали

        watermark = Image.new("RGBA", (text_box[2] * x_reps, text_box[3] * y_reps),
                              (0, 0, 0, 0))  # Создание изображения для водяного знака

        watermark_draw = ImageDraw.Draw(watermark)  # Создание объекта для рисования водяного знака

        for i in range(x_reps):
            for j in range(y_reps):
                watermark_draw.text((i * text_box[2] * 1.5, j * text_box[3] * 1.5), watermark_text, font=font,
                                    fill=(255, 255, 255, 128))  # Рисование текста

        watermark = watermark.resize(image.size)  # Изменение размера водяного знака
        watermark = watermark.convert(image.mode)  # Приведение к формату изображения
        image = Image.blend(image, watermark, alpha=0.05)  # Наложение водяного знака на изображение
        if "exif" in image.info:
            image = ImageOps.exif_transpose(image)  # Поворот изображения

        image.save(os.path.join(destination_directory_path, filename))  # Сохранение изображения

end = time.time() - start  # Время выполнения
print(f"Выполнено за: {end:.2f} секунд")
