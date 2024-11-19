import flet as ft
from db.conexion import ConexionBD

def pantalla_usuarios(page):
    """
    Pantalla para la gestión de usuarios.
    Permite registrar, actualizar, eliminar y listar usuarios.
    """
    # Método para cerrar la aplicación (temporalmente en lugar de volver a menú principal)
    def cerrar_aplicacion(e):
        page.window_close()  # Cierra la ventana de Flet

    txt_nombre_usuario = ft.TextField(label="Nombre de Usuario", width=300)
    txt_email = ft.TextField(label="Correo Electrónico", width=300)
    txt_contrasena = ft.TextField(label="Contraseña", password=True, width=300)
    txt_rol = ft.TextField(label="Rol", width=300)
    mensaje = ft.Text("", size=14, color=ft.colors.GREEN)

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre de Usuario")),
            ft.DataColumn(ft.Text("Correo Electrónico")),
            ft.DataColumn(ft.Text("Rol")),
            ft.DataColumn(ft.Text("Fecha de Creación")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[],
    )

    def cargar_datos():
        """Carga los datos de la tabla de usuarios desde la base de datos en la interfaz."""
        conexion = ConexionBD()
        conexion.conectar()
        consulta = """
            SELECT id_usuario, nombre_usuario, email, rol, fecha_creacion
            FROM tabla_usuarios
        """
        resultados = conexion.ejecutar_consulta(consulta)
        conexion.cerrar()

        tabla_datos.rows.clear()
        if resultados:
            for fila in resultados:
                tabla_datos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(fila[0]))),  # ID
                            ft.DataCell(ft.Text(fila[1])),  # Nombre de Usuario
                            ft.DataCell(ft.Text(fila[2])),  # Email
                            ft.DataCell(ft.Text(fila[3])),  # Rol
                            ft.DataCell(ft.Text(str(fila[4]))),  # Fecha de Creación
                            ft.DataCell(
                                ft.ElevatedButton(
                                    "Seleccionar",
                                    on_click=lambda e, id=fila[0], nombre=fila[1], email=fila[2], rol=fila[3]: seleccionar_fila(id, nombre, email, rol),
                                )
                            ),
                        ]
                    )
                )
        page.update()

    def seleccionar_fila(id, nombre, email, rol):
        """Selecciona una fila y autocompleta los campos."""
        txt_nombre_usuario.value = nombre
        txt_email.value = email
        txt_contrasena.value = ""  # No mostramos la contraseña por seguridad
        txt_rol.value = rol
        txt_nombre_usuario.data = id  # Guardar el ID del usuario para futuras acciones
        mensaje.value = ""
        page.update()

    def registrar_usuario(e):
        """Registra un nuevo usuario en la base de datos."""
        nombre = txt_nombre_usuario.value.strip()
        email = txt_email.value.strip()
        contrasena = txt_contrasena.value.strip()
        rol = txt_rol.value.strip()

        if not nombre or not email or not contrasena or not rol:
            mensaje.value = "Todos los campos son obligatorios."
            mensaje.color = ft.colors.RED
            page.update()
            return

        conexion = ConexionBD()
        conexion.conectar()
        consulta = """
            INSERT INTO tabla_usuarios (nombre_usuario, email, contrasena, rol)
            VALUES (%s, %s, %s, %s)
        """
        parametros = (nombre, email, contrasena, rol)
        conexion.ejecutar_consulta(consulta, parametros)
        conexion.cerrar()

        mensaje.value = "¡Usuario registrado con éxito!"
        mensaje.color = ft.colors.GREEN
        limpiar_campos(None)
        cargar_datos()

    def actualizar_usuario(e):
        """Actualiza los datos del usuario seleccionado."""
        id_usuario = txt_nombre_usuario.data
        nombre = txt_nombre_usuario.value.strip()
        email = txt_email.value.strip()
        contrasena = txt_contrasena.value.strip()
        rol = txt_rol.value.strip()

        if not id_usuario or not nombre or not email or not rol:
            mensaje.value = "Seleccione un usuario para actualizar y complete todos los campos."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_actualizacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = """
                UPDATE tabla_usuarios
                SET nombre_usuario = %s, email = %s, contrasena = %s, rol = %s
                WHERE id_usuario = %s
            """
            parametros = (nombre, email, contrasena, rol, id_usuario)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Usuario actualizado con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de actualizar el usuario con ID {id_usuario}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_actualizacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def eliminar_usuario(e):
        """Elimina el usuario seleccionado."""
        id_usuario = txt_nombre_usuario.data
        if not id_usuario:
            mensaje.value = "Seleccione un usuario para eliminar."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_eliminacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "DELETE FROM tabla_usuarios WHERE id_usuario = %s"
            parametros = (id_usuario,)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Usuario eliminado con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de eliminar el usuario con ID {id_usuario}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_eliminacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def limpiar_campos(e):
        """Limpia los campos del formulario."""
        txt_nombre_usuario.value = ""
        txt_email.value = ""
        txt_contrasena.value = ""
        txt_rol.value = ""
        txt_nombre_usuario.data = None
        mensaje.value = ""
        page.update()

    # Diseño de la pantalla
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Gestión de Usuarios", size=20, weight=ft.FontWeight.BOLD)]),
                ft.Row([txt_nombre_usuario, txt_email]),
                ft.Row([txt_contrasena, txt_rol]),
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar", on_click=registrar_usuario, bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Actualizar", on_click=actualizar_usuario, bgcolor=ft.colors.BLUE),
                        ft.ElevatedButton("Eliminar", on_click=eliminar_usuario, bgcolor=ft.colors.RED),
                        ft.ElevatedButton("Limpiar", on_click=limpiar_campos, bgcolor=ft.colors.GREY),
                        ft.ElevatedButton("Volver", on_click=cerrar_aplicacion, bgcolor=ft.colors.ORANGE),
                    ]
                ),
                mensaje,
                tabla_datos,
            ],
            spacing=20,
        )
    )
    cargar_datos()
