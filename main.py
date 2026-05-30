from view.vista import Vista
from controller.controlador import Control

if __name__ == "__main__":
    vista = Vista()
    controlador = Control(vista)
    controlador.iniciar()
