# Скрипт для конвертирования файлов из MTS в mp4
* Исполняемый фаил .exe
* Использует библиотеку ffmpeg.exe, требует его отдельного скачивания и размещения в `./libres/`
 
`pyi-makespec --onefile --add-data "./libres/ffmpeg.exe:ffmpeg.exe" --icon=icon.ico main.py`

`pyinstaller --onefile --add-data "./libres/ffmpeg.exe:ffmpeg.exe"  main.py
`