import flet as ft

def mostrar_menu_principal(page, usuario, ir_login):
    """Muestra el menú principal tras el inicio de sesión"""

    def abrir_aparatos(e):
        page.clean()
        pantalla_aparatos(page, lambda p: mostrar_menu_principal(p, usuario, ir_login))

    # Diseño del menú
    page.add(
        ft.Column(
            [
                ft.Text(f"Bienvenido, {usuario}!", size=20, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    "Gestión de Aparatos",
                    on_click=abrir_aparatos,
                    bgcolor=ft.colors.PURPLE,
                ),
                ft.ElevatedButton(
                    "Salir",
                    on_click=lambda e: ir_login(page),  # Redirige al login
                    bgcolor=ft.colors.RED,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )
    page.update()
