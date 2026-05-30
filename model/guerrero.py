from model.personaje import Personaje

class Guerrero(Personaje):
    def __init__(self, nombre: str, nivel: int, puntos_vida: int, fuerza: int):
        super().__init__(nombre, nivel, puntos_vida)
        self.fuerza = fuerza

    def habilidad_especial(self):
        print(f"[HABILIDAD GUERRERO] ¡Furia Estruendosa! Daño físico escalado en fuerza: {self.fuerza}")
