import os
from PIL import Image
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
# Корректируем импорт для зацикливания аудио
from moviepy.audio.fx.all import audio_loop

from config import VIDEO_WIDTH, VIDEO_HEIGHT, DEFAULT_IMAGE_DURATION, OUTPUT_FPS


def resize_and_pad_image(image_path, output_size=(VIDEO_WIDTH, VIDEO_HEIGHT), bg_color='black'):
    """
    Изменяет размер изображения с сохранением пропорций и добавляет фон.
    (Код этой функции остается без изменений)
    """
    try:
        img = Image.open(image_path).convert("RGBA")
        img_copy = img.copy()
        img_copy.thumbnail(output_size, Image.Resampling.LANCZOS)
        background = Image.new('RGBA', output_size, bg_color)
        paste_position = (
            (output_size[0] - img_copy.width) // 2,
            (output_size[1] - img_copy.height) // 2
        )
        background.paste(img_copy, paste_position, img_copy)
        return background.convert("RGB")
    except FileNotFoundError:
        print(f"Ошибка: Изображение не найдено по пути: {image_path}")
        return None
    except Exception as e:
        print(f"Ошибка при обработке изображения {image_path}: {e}")
        return None


def create_video(image_folder, audio_path, output_path):
    """
    Создает видео из набора изображений и добавляет аудио.
    """
    print("--- Начинаем создание видео ---")

    image_files = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg'))])

    if not image_files:
        print("Ошибка: В папке с обработанными изображениями пусто.")
        return

    clips = [ImageClip(m).set_duration(DEFAULT_IMAGE_DURATION) for m in image_files]
    video_clip = concatenate_videoclips(clips, method="compose")

    if audio_path:
        print(f"Добавляем аудио: {audio_path}")
        try:
            audio_clip = AudioFileClip(audio_path)

            # ИСПРАВЛЕНА ЛОГИКА ЗАЦИКЛИВАНИЯ
            if video_clip.duration > audio_clip.duration:
                print("Аудио короче видео. Зацикливаем...")
                audio_clip = audio_clip.fx(audio_loop, duration=video_clip.duration)
            else:
                print("Аудио длиннее видео. Обрезаем...")
                audio_clip = audio_clip.subclip(0, video_clip.duration)

            final_clip = video_clip.set_audio(audio_clip)
        except Exception as e:
            print(f"Ошибка при обработке аудио: {e}. Видео будет создано без звука.")
            final_clip = video_clip
    else:
        print("Аудиофайл не найден, видео будет без звука.")
        final_clip = video_clip

    print(f"Экспортируем видео в файл: {output_path}")
    final_clip.write_videofile(output_path, fps=OUTPUT_FPS, codec="libx264", audio_codec="aac")
    print("--- Видео успешно создано! ---")