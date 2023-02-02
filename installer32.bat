@echo Click any key to start Python download (Python 3.11.1 32-bit) 
@pause>nul
@start https://www.python.org/ftp/python/3.10.9/python-3.10.9.exe
@cls
@echo Click any key to continue downloading (if Python is installed)
@pause>nul
@cls
@echo Installing required libs
python.exe -m pip install --upgrade pip
pip3 install wheel
pip3 install pygame
pip3 install PyQt5
@echo Instalation complete!
@echo Click any key to close this window
@pause>nul