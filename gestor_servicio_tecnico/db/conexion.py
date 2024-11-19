import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

class ConexionBD:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.nombre = os.getenv("DB_NAME")
        self.usuario = os.getenv("DB_USER")
        self.contrasena = os.getenv("DB_PASSWORD")
        self.puerto = os.getenv("DB_PORT")
        self.conexion = None

    def conectar(self):
        """Establece la conexión con la base de datos"""
        try:
            self.conexion = psycopg2.connect(
                host=self.host,
                database=self.nombre,
                user=self.usuario,
                password=self.contrasena,
                port=self.puerto,
            )
            print("Conexión a la base de datos exitosa.")
        except psycopg2.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            self.conexion = None

    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")

    def ejecutar_consulta(self, consulta, parametros=None):
        """Ejecuta una consulta SQL"""
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(consulta, parametros)
                self.conexion.commit()
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
