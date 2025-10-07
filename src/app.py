from interface_grafica import InterfaceGrafica

def app():
    interface = InterfaceGrafica(1280, 720)
    interface.menu()
    interface.iniciar()

if __name__ == '__main__':
    app()