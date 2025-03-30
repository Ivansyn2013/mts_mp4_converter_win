import os
import subprocess

import ffmpeg
from loguru import logger
from tqdm import tqdm
import sys


def convert_mts_mp4(base_dir, file, options=None):
    """
    Function for convet file from MTS to mp4
    :param file: path to mts file
    :return:
    """
    OUTPUT_DIR = os.path.join(base_dir, 'converted')
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_file_name = os.path.basename(file).split('.')[0] + ".mp4"
    output_file = os.path.join(OUTPUT_DIR, output_file_name)
    i = 1
    while os.path.exists(output_file):
        output_file_name = (os.path.basename(file).split('.')[0] +
                            f"({str(i)})" +
                            ".mp4")
        output_file = os.path.join(OUTPUT_DIR, output_file_name)
        i += 1

    if get_os() == 'windows':
        ffmpeg_path = os.path.join(os.path.dirname(sys.executable),
                                   '',
                                   "ffmpeg.exe")

        # Если ffmpeg.exe не рядом с EXE, ищем в папке скрипта
        if not os.path.exists(ffmpeg_path):
            ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")

    try:

        (
            ffmpeg
            .input(file)
            .output(output_file,
                    **{"c:v": "copy", "c:a": "copy"})  # Копируем видео и аудио
            .run()
        )
        logger.info(f"Фаил {output_file_name} перекодирован")
    except ffmpeg.Error as e:
        logger.error(e)
        logger.error(f"Возникла ошибка при перекодированнии файла {output_file_name}")
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
    mts_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.mts'):
                mts_files.append(os.path.join(root, file))
    if not mts_files:
        raise FileNotFoundError("Ни однин фаил MTS не был найден в каталоге")
    return mts_files


def main():
    START_DIR = os.getcwd()
    if not get_os():
        raise SystemError("Программ предназначена для запуска в Windows")

    mts_files = find_MTS_files(START_DIR)
    logger.info(f"Обнаружено {len(mts_files)} файлов нужного формата")

    for file in tqdm(mts_files, desc="Конвертация файлов MTS в mp4"):
        convert_mts_mp4(START_DIR, file)

    logger.info("Конверация закончена")


if __name__ == '__main__':
    main()
