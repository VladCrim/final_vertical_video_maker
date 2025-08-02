import os
from video_processing import resize_and_pad_image, create_video
from config import SUPPORTED_IMAGE_FORMATS

SUPPORTED_AUDIO_FORMATS = ('.mp3', '.wav')


def find_audio_file(folder):
    """Находит первый попавшийся аудиофайл в папке."""
    for file in os.listdir(folder):
        if file.lower().endswith(SUPPORTED_AUDIO_FORMATS):
            return os.path.join(folder, file)
    return None


def process_images(image_folder, output_folder):
    """
    Находит все изображения в папке, обрабатывает их и сохраняет результат.
    """
    print("Начинаем обработку изображений...")
    if not os.path.exists(output_folder):
        print(f"Создаем папку для обработанных изображений: {output_folder}")
        os.makedirs(output_folder)

    files = os.listdir(image_folder)
    image_files = [f for f in files if f.lower().endswith(SUPPORTED_IMAGE_FORMATS)]

    if not image_files:
        print(f"Внимание: В папке '{image_folder}' не найдено изображений в форматах {SUPPORTED_IMAGE_FORMATS}.")
        return 0

    print(f"Найдено {len(image_files)} изображений. Начинаем обработку...")
    for filename in image_files:
        input_path = os.path.join(image_folder, filename)
        processed_image = resize_and_pad_image(input_path)
        if processed_image:
            output_filename = f"processed_{filename}"
            output_path = os.path.join(output_folder, output_filename)
            processed_image.save(output_path)
            print(f"Сохранено: {output_path}")

    return len(image_files)


def main():
    """
    Главная функция приложения.
    """
    print("--- Vertical Video Maker ---")

    # --- ИСПРАВЛЕННАЯ ЛОГИКА ОПРЕДЕЛЕНИЯ ПУТЕЙ ---
    # Получаем абсолютный путь к папке, где лежит наш скрипт (т.е. к папке 'src')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Поднимаемся на один уровень выше, чтобы получить корень проекта
    project_root = os.path.dirname(script_dir)

    # Теперь все пути будут правильными
    input_folder = os.path.join(project_root, 'input')
    output_folder = os.path.join(project_root, 'output')
    processed_images_folder = os.path.join(output_folder, 'processed_images')

    final_video_path = os.path.join(output_folder, 'final_video.mp4')

    if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
        os.makedirs(input_folder, exist_ok=True)
        print(f"Создана папка '{input_folder}'. Пожалуйста, поместите в нее ваши изображения и аудиофайл.")
        return

    processed_count = process_images(input_folder, processed_images_folder)
    print("--- Обработка изображений завершена ---")

    if processed_count == 0:
        print("Нет изображений для создания видео. Завершение работы.")
        return

    audio_file = find_audio_file(input_folder)
    if not audio_file:
        print(
            f"Внимание: в папке '{input_folder}' не найден аудиофайл ({SUPPORTED_AUDIO_FORMATS}). Видео будет без музыки.")

    create_video(
        image_folder=processed_images_folder,
        audio_path=audio_file,
        output_path=final_video_path
    )


if __name__ == "__main__":
    main()