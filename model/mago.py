from model.personaje import Personaje

class Mago(Personaje):
    def __init__(self, nombre: str, nivel: int, puntos_vida: int, mana: int):
        super().__init__(nombre, nivel, puntos_vida)
        self.mana = mana

    def habilidad_especial(self):
        print(f"[HABILIDAD MAGO] ¡Tormenta Arcana! Poder destructivo usando sus {self.mana} de maná.")
