import flet as ft
from db.conexion import ConexionBD

def pantalla_login(page, ir_menu_principal):
    """Pantalla de inicio de sesión"""

    def validar_credenciales(e):
        usuario = txt_usuario.value
        contrasena = txt_contrasena.value

        # Validación en la base de datos
        conexion = ConexionBD()
        conexion.conectar()
        consulta = "SELECT * FROM tabla_usuarios WHERE nombre_usuario = %s AND contrasena = %s"
        parametros = (usuario, contrasena)
        resultado = conexion.ejecutar_consulta(consulta, parametros)
        conexion.cerrar()

        if resultado:
            page.clean()
            ir_menu_principal(page, usuario)  # Redirige al menú principal
        else:
            mensaje_error.value = "Credenciales inválidas"
            page.update()

    # Componentes del formulario
    txt_usuario = ft.TextField(label="Usuario", autofocus=True, width=300)
    txt_contrasena = ft.TextField(label="Contraseña", password=True, width=300)
    btn_ingresar = ft.ElevatedButton("Iniciar sesión", on_click=validar_credenciales)
    mensaje_error = ft.Text("", color=ft.colors.RED)

    # Diseño de la pantalla
    page.add(
        ft.Column(
            [
                ft.Text("Iniciar sesión", size=24, weight=ft.FontWeight.BOLD),
                txt_usuario,
                txt_contrasena,
                btn_ingresar,
                mensaje_error,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    page.update()
