# Скрипт для конвертирования файлов из MTS в mp4
* Программа ищет файлы .MTS в папке запуска, при нахождении запускает скрипт использующий библиотеку ffmpeg. Конвертированные файлы отправляются в папку "converted"
* Исполняемый фаил .exe
* Использует библиотеку ffmpeg.exe, требует его отдельного скачивания и размещения в `./libres/`
 

## Вызов сборки для Windows
* `pyi-makespec --onefile --add-data "./libres/ffmpeg.exe;ffmpeg.exe" --icon=icon.ico main.py`

* `pyinstaller --onefile --add-data "./libres/ffmpeg.exe;ffmpeg.exe"  main.py
`
* исполняемый фаил будет доступен в папке `./dist/main.exe`