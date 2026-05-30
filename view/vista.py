class Vista:
    def mostrar_menu(self) -> int:
        print("\n=== GESTIÓN RPG EN PYTHON (MVC + SQLITE) ===")
        print("1. Crear Personaje e Insertar en BD")
        print("2. Listar todos los Personajes")
        print("3. Buscar Personaje por Nombre")
        print("4. Actualizar Nivel (Update)")
        print("5. Eliminar Personaje (Delete)")
        print("6. Ejecutar Habilidades Especiales (Polimorfismo)")
        print("7. Salir")
        try:
            return int(input("Seleccione una opción (1-7): "))
        except ValueError:
            return -1

    def pedir_texto(self, mensaje: str) -> str:
        return input(mensaje)

    def pedir_entero(self, mensaje: str) -> int:
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print("[!] Entrada inválida. Por favor, ingrese un número entero.")

    def mostrar_mensaje(self, mensaje: str):
        print(mensaje)

    def mostrar_error(self, mensaje: str):
        print(f"\033[91m{mensaje}\033[0m")
