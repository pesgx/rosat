import flet as ft
from db.conexion import ConexionBD

def pantalla_grupos(page):
    """
    Pantalla para la gestión de grupos.
    Permite registrar, actualizar, eliminar y listar grupos.
    """
    # Método para cerrar la aplicación (temporalmente en lugar de volver a menú principal)
    def cerrar_aplicacion(e):
        page.window_close()  # Cierra la ventana de Flet

    txt_nombre_grupo = ft.TextField(label="Nombre del Grupo", width=300)
    mensaje = ft.Text("", size=14, color=ft.colors.GREEN)  # Mensaje para notificaciones

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre del Grupo")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[],
    )

    def cargar_datos():
        """Carga los datos de la tabla de grupos desde la base de datos en la interfaz."""
        conexion = ConexionBD()
        conexion.conectar()
        consulta = "SELECT id_grupo, nombre_grupo FROM tabla_grupos"
        resultados = conexion.ejecutar_consulta(consulta)
        conexion.cerrar()

        tabla_datos.rows.clear()
        if resultados:
            for fila in resultados:
                tabla_datos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(fila[0]))),  # ID
                            ft.DataCell(ft.Text(fila[1])),  # Nombre del Grupo
                            ft.DataCell(
                                ft.ElevatedButton(
                                    "Seleccionar",
                                    on_click=lambda e, id=fila[0], nombre=fila[1]: seleccionar_fila(id, nombre),
                                )
                            ),
                        ]
                    )
                )
        page.update()

    def seleccionar_fila(id, nombre):
        """Selecciona una fila y autocompleta los campos."""
        txt_nombre_grupo.value = nombre
        txt_nombre_grupo.data = id  # Guardar el ID del grupo para futuras acciones
        mensaje.value = ""  # Limpia el mensaje previo
        page.update()

    def registrar_grupo(e):
        """Registra un nuevo grupo en la base de datos."""
        nombre = txt_nombre_grupo.value.strip()

        if not nombre:
            mensaje.value = "El campo 'Nombre del Grupo' está vacío."
            mensaje.color = ft.colors.RED
            page.update()
            return

        conexion = ConexionBD()
        conexion.conectar()
        consulta = "INSERT INTO tabla_grupos (nombre_grupo) VALUES (%s)"
        parametros = (nombre,)
        conexion.ejecutar_consulta(consulta, parametros)
        conexion.cerrar()

        mensaje.value = "¡Grupo registrado con éxito!"
        mensaje.color = ft.colors.GREEN
        limpiar_campos(None)
        cargar_datos()

    def actualizar_grupo(e):
        """Actualiza los datos del grupo seleccionado."""
        id_grupo = txt_nombre_grupo.data
        nombre = txt_nombre_grupo.value.strip()

        if not id_grupo or not nombre:
            mensaje.value = "Seleccione un grupo para actualizar y complete el campo."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_actualizacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "UPDATE tabla_grupos SET nombre_grupo = %s WHERE id_grupo = %s"
            parametros = (nombre, id_grupo)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Grupo actualizado con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de actualizar el grupo con ID {id_grupo}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_actualizacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def eliminar_grupo(e):
        """Elimina el grupo seleccionado."""
        id_grupo = txt_nombre_grupo.data
        if not id_grupo:
            mensaje.value = "Seleccione un grupo para eliminar."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_eliminacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "DELETE FROM tabla_grupos WHERE id_grupo = %s"
            parametros = (id_grupo,)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Grupo eliminado con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de eliminar el grupo con ID {id_grupo}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_eliminacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def limpiar_campos(e):
        """Limpia los campos del formulario."""
        txt_nombre_grupo.value = ""
        txt_nombre_grupo.data = None
        mensaje.value = ""
        page.update()

    # Diseño de la pantalla
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Gestión de Grupos", size=20, weight=ft.FontWeight.BOLD)]),
                ft.Row([txt_nombre_grupo]),
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar", on_click=registrar_grupo, bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Actualizar", on_click=actualizar_grupo, bgcolor=ft.colors.BLUE),
                        ft.ElevatedButton("Eliminar", on_click=eliminar_grupo, bgcolor=ft.colors.RED),
                        ft.ElevatedButton("Limpiar", on_click=limpiar_campos, bgcolor=ft.colors.GREY),
                        ft.ElevatedButton("Volver", on_click=cerrar_aplicacion, bgcolor=ft.colors.ORANGE),
                    ]
                ),
                mensaje,  # Agregamos el mensaje al diseño para que sea visible
                tabla_datos,
            ],
            spacing=20,
        )
    )
    cargar_datos()
