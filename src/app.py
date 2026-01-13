# import sys
# import os
from interface_grafica import InterfaceGrafica

# def resource_path(relative_path):
#     """ Retorna o caminho absoluto para o recurso, funcionando em dev e no PyInstaller """
#     try:
#         # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)

def app():
    interface = InterfaceGrafica()
    interface.iniciar()

if __name__ == '__main__':
    app()