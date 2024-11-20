'''
    Archivo principal de la aplicación.
    Inicia la pantalla principal de la aplicación.'''

import flet as ft
from vistas.aparatos import pantalla_aparatos
from vistas.usuarios import pantalla_usuarios
from vistas.companias import pantalla_companias
from vistas.empleados import pantalla_empleados
from vistas.estados import pantalla_estados
from vistas.grupos import pantalla_grupos
from vistas.marcas import pantalla_marcas
from vistas.articulos import pantalla_articulos
from vistas.clientes import pantalla_clientes
from vistas.avisos import pantalla_avisos

def main(page: ft.Page):
    page.title = "Gestión de Avisos"
    pantalla_avisos(page)

if __name__ == "__main__":
    ft.app(target=main)