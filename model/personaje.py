class Personaje:
    def __init__(self, nombre: str, nivel: int, puntos_vida: int):
        self.nombre = nombre
        self.nivel = nivel
        self.puntos_vida = puntos_vida

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        if valor and valor.strip():
            self._nombre = valor
        else:
            print("[ERROR] Nombre vacío o inválido. Asignando 'Heroe_Anonimo'.")
            self._nombre = "Heroe_Anonimo"

    @property
    def nivel(self):
        return self._nivel
    
    @nivel.setter
    def nivel(self, valor):
        if 1 <= valor <= 100:
            self._nivel = valor
        else:
            print("[ERROR] Nivel fuera de rango (1-100). Asignando 1.")
            self._nivel = 1

    @property
    def puntos_vida(self):
        return self._puntos_vida
    
    @puntos_vida.setter
    def puntos_vida(self, valor):
        if valor >= 0:
            self._puntos_vida = valor
        else:
            print("[ERROR] Puntos de vida negativos. Asignando 0.")
            self._puntos_vida = 0

    def habilidad_especial(self):
        print(f"{self.nombre} realiza un ataque básico.")
