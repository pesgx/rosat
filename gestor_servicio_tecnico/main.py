import flet as ft
from vistas.login import pantalla_login
from vistas.menu_principal import mostrar_menu_principal

def main(page: ft.Page):
    page.title = "Gestor de Servicio Técnico"

    def ir_login(p):
        pantalla_login(p, ir_menu_principal)

    def ir_menu_principal(p, usuario):
        mostrar_menu_principal(p, usuario, ir_login)

    # Inicia en la pantalla de login
    ir_login(page)

if __name__ == "__main__":
    ft.app(target=main)
