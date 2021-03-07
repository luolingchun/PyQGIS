:: -w 窗口程序 -c 控制台程序
"C:\Program Files\QGIS 3.16\bin\python-qgis-ltr.bat" -m PyInstaller -c ^
--add-data="C:\Program Files\QGIS 3.16\apps\Python37\Lib\site-packages\PyQt5\*.pyd;PyQt5" ^
--add-data="C:\Program Files\QGIS 3.16\share;share" ^
--add-data="data;data" ^
--add-data="images;images" ^
--icon=images\pyqgis.ico ^
PyQGIS.py