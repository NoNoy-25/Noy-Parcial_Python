from model.personaje import Personaje

class Arquero(Personaje):
    def __init__(self, nombre: str, nivel: int, puntos_vida: int, destreza: int):
        super().__init__(nombre, nivel, puntos_vida)
        self.destreza = destreza

    def habilidad_especial(self):
        print(f"[HABILIDAD ARQUERO] ¡Ráfaga Silvante! Precisión crítica basada en destreza: {self.destreza}")
