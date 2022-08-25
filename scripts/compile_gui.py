import subprocess

# TODO: Not working for some dumb reason
ui_file = "..\\src\\gui\\ui\\mainWindow.ui"
ui_python = "..\\src\\gui\\compiled\\main_window.py"

subprocess.call(['pyside6-uic', ui_file, ">", ui_python], shell=True)