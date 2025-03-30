import subprocess

from loguru import logger
from tqdm import tqdm
import sys
from pathlib import Path


def get_ffmpeg_path():
    """Определяет правильный путь к ffmpeg"""
    # 1. Проверяем рядом с EXE (для PyInstaller)
    ffmpeg_path = Path(sys.executable).parent / "ffmpeg.exe"
    if ffmpeg_path.exists():
        return str(ffmpeg_path)

    # 2. Проверяем в папке скрипта
    ffmpeg_path = Path(__file__).parent / "ffmpeg.exe"
    if ffmpeg_path.exists():
        return str(ffmpeg_path)

    # 3. Проверяем в PATH системы
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return "ffmpeg"
    except:
        logger.error("FFmpeg не найден! Положите ffmpeg.exe рядом с программой")
        sys.exit(1)


def convert_mts_mp4(base_dir, file, options=None):
    """
    Function for convet file from MTS to mp4
    :param file: path to mts file
    :return:
    """
    output_dir = base_dir / 'converted'
    output_dir.mkdir(parents=True, exist_ok=True)  # Создаем папку, если не существует

    stem = file.stem
    suffix = '.mp4'
    output_file = output_dir / f"{stem}{suffix}"

    # Обработка случая, когда файл уже существует
    counter = 1
    while output_file.exists():
        output_file = output_dir / f"{stem}({counter}){suffix}"
        counter += 1


    ffmpeg_path = get_ffmpeg_path()


    try:
        subprocess.run([
            ffmpeg_path,
            '-i', str(file),
            '-c:v', 'copy',
            '-c:a', 'copy',
            '-y',  # Разрешить перезапись
            str(output_file)
        ], check=True, capture_output=True)



        logger.success(f"Фаил {output_file.name} перекодирован")
    except subprocess.CalledProcessError as e:
        logger.error(e)
        logger.error(f"Возникла ошибка при перекодированнии файла {output_file.name}")
        sys.exit(1)



def get_os():
    system = sys.platform.lower()
    if system.startswith('linux'):
        return 'linux'
    if system.startswith('win'):
        return 'windows'
    return False

def find_MTS_files(path):
    """
    Function for find MTS files in directory
    :param path: str
    :return: list
    """
    mts_files = list(path.rglob('*.mts')) + list(path.rglob('*.MTS'))
    if not mts_files:
        raise FileNotFoundError("Не найдено ни одного MTS файла в каталоге")
    return mts_files


def main():
    START_DIR = Path.cwd()
    if not get_os():
        raise SystemError("Программ предназначена для запуска в Windows")

    mts_files = find_MTS_files(START_DIR)
    logger.info(f"Обнаружено {len(mts_files)} файлов нужного формата")

    for file in tqdm(mts_files, desc="Конвертация файлов MTS в mp4"):
        convert_mts_mp4(START_DIR, file)

    logger.info("Конверация закончена")
    print("Нажми любую кнопку для завершения")


if __name__ == '__main__':
    main()
