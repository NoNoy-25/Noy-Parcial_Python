import sqlite3
from model.personaje import Personaje
from model.guerrero import Guerrero
from model.mago import Mago
from model.arquero import Arquero
from view.vista import Vista

class Control:
    def __init__(self, vista: Vista):
        self.vista = vista
        self.db_name = "base_multi.db"
        self.inicializar_bd()

    def conectar(self):
        con = sqlite3.connect(self.db_name)
        con.execute("PRAGMA foreign_keys = ON;")
        return con

    def inicializar_bd(self):
        with self.conectar() as con:
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS personajes (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL UNIQUE, nivel INTEGER NOT NULL DEFAULT 1, puntos_vida INTEGER NOT NULL DEFAULT 100);")
            cursor.execute("CREATE TABLE IF NOT EXISTS guerreros (personaje_id INTEGER PRIMARY KEY, fuerza INTEGER NOT NULL DEFAULT 0, FOREIGN KEY (personaje_id) REFERENCES personajes(id) ON DELETE CASCADE);")
            cursor.execute("CREATE TABLE IF NOT EXISTS magos (personaje_id INTEGER PRIMARY KEY, mana INTEGER NOT NULL DEFAULT 0, FOREIGN KEY (personaje_id) REFERENCES personajes(id) ON DELETE CASCADE);")
            cursor.execute("CREATE TABLE IF NOT EXISTS arqueros (personaje_id INTEGER PRIMARY KEY, destreza INTEGER NOT NULL DEFAULT 0, FOREIGN KEY (personaje_id) REFERENCES personajes(id) ON DELETE CASCADE);")
            cursor.execute("CREATE TABLE IF NOT EXISTS inventario (id INTEGER PRIMARY KEY AUTOINCREMENT, personaje_id INTEGER NOT NULL, item_nombre TEXT NOT NULL, cantidad INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (personaje_id) REFERENCES personajes(id) ON DELETE CASCADE);")
            con.commit()

    def iniciar(self):
        opcion = 0
        while opcion != 7:
            opcion = self.vista.mostrar_menu()
            if opcion == 1: self.crear_personaje()
            elif opcion == 2: self.listar_personajes()
            elif opcion == 3: self.buscar_personaje()
            elif opcion == 4: self.actualizar_personaje()
            elif opcion == 5: self.eliminar_personaje()
            elif opcion == 6: self.usar_habilidades()
            elif opcion == 7: self.vista.mostrar_mensaje("Finalizando el programa del parcial.")
            else: self.vista.mostrar_error("[ERROR] Opcion invalida.")

    def crear_personaje(self):
        self.vista.mostrar_mensaje("\n--- CREAR PERSONAJE ---")
        print("1. Guerrero | 2. Mago | 3. Arquero")
        tipo = self.vista.pedir_entero("Seleccione el rol: ")
        nombre = self.vista.pedir_texto("Ingrese nombre: ")
        nivel = self.vista.pedir_entero("Ingrese nivel: ")
        vida = self.vista.pedir_entero("Ingrese puntos de vida: ")
        p_temp = Personaje(nombre, nivel, vida)
        con = self.conectar()
        try:
            cursor = con.cursor()
            cursor.execute("INSERT INTO personajes (nombre, nivel, puntos_vida) VALUES (?, ?, ?)", (p_temp.nombre, p_temp.nivel, p_temp.puntos_vida))
            id_generado = cursor.lastrowid
            if tipo == 1:
                fuerza = self.vista.pedir_entero("Ingrese fuerza del Guerrero: ")
                cursor.execute("INSERT INTO guerreros (personaje_id, fuerza) VALUES (?, ?)", (id_generado, fuerza))
            elif tipo == 2:
                mana = self.vista.pedir_entero("Ingrese mana del Mago: ")
                cursor.execute("INSERT INTO magos (personaje_id, mana) VALUES (?, ?)", (id_generado, mana))
            elif tipo == 3:
                destreza = self.vista.pedir_entero("Ingrese destreza del Arquero: ")
                cursor.execute("INSERT INTO arqueros (personaje_id, destreza) VALUES (?, ?)", (id_generado, destreza))
            con.commit()
            self.vista.mostrar_mensaje("[EXITO] Personaje guardado de forma persistente.")
        except sqlite3.IntegrityError:
            self.vista.mostrar_error("[ERROR] El nombre ya esta registrado.")
        finally:
            con.close()

    def listar_personajes(self):
        self.vista.mostrar_mensaje("\n--- LISTADO DE PERSONAJES ---")
        with self.conectar() as con:
            cursor = con.cursor()
            cursor.execute("SELECT id, nombre, nivel, puntos_vida FROM personajes")
            filas = cursor.fetchall()
            if not filas:
                self.vista.mostrar_mensaje("La base de datos esta vacia.")
                return
            for f in filas:
                self.vista.mostrar_mensaje(f"ID: {f[0]} | Nombre: {f[1]} | Nivel: {f[2]} | Vida: {f[3]}")

    def buscar_personaje(self):
        nombre_buscar = self.vista.pedir_texto("Ingrese el nombre exacto a buscar: ")
        with self.conectar() as con:
            cursor = con.cursor()
            cursor.execute("SELECT id, nombre, nivel FROM personajes WHERE nombre = ?", (nombre_buscar,))
            fila = cursor.fetchone()
            if fila:
                self.vista.mostrar_mensaje(f"[ENCONTRADO] ID: {fila[0]} | Nombre: {fila[1]} | Nivel: {fila[2]}")
            else:
                self.vista.mostrar_error(f"El personaje '{nombre_buscar}' no existe.")

    def actualizar_personaje(self):
        idx = self.vista.pedir_entero("Ingrese el ID del personaje a modificar: ")
        nuevo_nv = self.vista.pedir_entero("Ingrese el nuevo nivel: ")
        with self.conectar() as con:
            cursor = con.cursor()
            cursor.execute("UPDATE personajes SET nivel = ? WHERE id = ?", (nuevo_nv, idx))
            if cursor.rowcount > 0:
                con.commit()
                self.vista.mostrar_mensaje("[EXITO] Nivel modificado correctamente.")
            else:
                self.vista.mostrar_error(f"[ERROR] El ID {idx} no fue hallado.")

    def eliminar_personaje(self):
        idx = self.vista.pedir_entero("Ingrese el ID del personaje a eliminar: ")
        with self.conectar() as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM personajes WHERE id = ?", (idx,))
            if cursor.rowcount > 0:
                con.commit()
                self.vista.mostrar_mensaje("[EXITO] Registro eliminado (ON DELETE CASCADE aplicado).")
            else:
                self.vista.mostrar_error(f"[ERROR] El ID {idx} no existe.")

    def usar_habilidades(self):
        self.vista.mostrar_mensaje("\n--- POLIMORFISMO: EJECUTANDO ACCIONES DESDE BD ---")
        with self.conectar() as con:
            cursor = con.cursor()
            cursor.execute("SELECT p.nombre, p.nivel, p.puntos_vida, g.fuerza FROM personajes p JOIN guerreros g ON p.id = g.personaje_id")
            for f in cursor.fetchall(): Guerrero(f[0], f[1], f[2], f[3]).habilidad_especial()
            cursor.execute("SELECT p.nombre, p.nivel, p.puntos_vida, m.mana FROM personajes p JOIN magos m ON p.id = m.personaje_id")
            for f in cursor.fetchall(): Mago(f[0], f[1], f[2], f[3]).habilidad_especial()
            cursor.execute("SELECT p.nombre, p.nivel, p.puntos_vida, a.destreza FROM personajes p JOIN arqueros a ON p.id = a.personaje_id")
            for f in cursor.fetchall(): Arquero(f[0], f[1], f[2], f[3]).habilidad_especial()
