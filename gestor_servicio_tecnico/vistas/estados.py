import flet as ft
from db.conexion import ConexionBD

def pantalla_estados(page):
    """
    Pantalla para la gestión de estados.
    Permite registrar, actualizar, eliminar y listar estados.
    """
    # Método para cerrar la aplicación (temporalmente en lugar de volver a menú principal)
    def cerrar_aplicacion(e):
        page.window_close()  # Cierra la ventana de Flet

    txt_nombre_estado = ft.TextField(label="Nombre del Estado", width=300)
    mensaje = ft.Text("", size=14, color=ft.colors.GREEN)  # Mensaje para notificaciones

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre del Estado")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[],
    )

    def cargar_datos():
        """Carga los datos de la tabla de estados desde la base de datos en la interfaz."""
        conexion = ConexionBD()
        conexion.conectar()
        consulta = "SELECT id_estado, nombre_estado FROM tabla_estados"
        resultados = conexion.ejecutar_consulta(consulta)
        conexion.cerrar()

        tabla_datos.rows.clear()
        if resultados:
            for fila in resultados:
                tabla_datos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(fila[0]))),  # ID
                            ft.DataCell(ft.Text(fila[1])),  # Nombre del Estado
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
        txt_nombre_estado.value = nombre
        txt_nombre_estado.data = id  # Guardar el ID del estado para futuras acciones
        mensaje.value = ""  # Limpia el mensaje previo
        page.update()

    def registrar_estado(e):
        """Registra un nuevo estado en la base de datos."""
        nombre = txt_nombre_estado.value.strip()

        if not nombre:
            mensaje.value = "El campo 'Nombre del Estado' está vacío."
            mensaje.color = ft.colors.RED
            page.update()
            return

        conexion = ConexionBD()
        conexion.conectar()
        consulta = "INSERT INTO tabla_estados (nombre_estado) VALUES (%s)"
        parametros = (nombre,)
        conexion.ejecutar_consulta(consulta, parametros)
        conexion.cerrar()

        mensaje.value = "¡Estado registrado con éxito!"
        mensaje.color = ft.colors.GREEN
        limpiar_campos(None)
        cargar_datos()

    def actualizar_estado(e):
        """Actualiza los datos del estado seleccionado."""
        id_estado = txt_nombre_estado.data
        nombre = txt_nombre_estado.value.strip()

        if not id_estado or not nombre:
            mensaje.value = "Seleccione un estado para actualizar y complete el campo."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_actualizacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "UPDATE tabla_estados SET nombre_estado = %s WHERE id_estado = %s"
            parametros = (nombre, id_estado)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Estado actualizado con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de actualizar el estado con ID {id_estado}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_actualizacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def eliminar_estado(e):
        """Elimina el estado seleccionado."""
        id_estado = txt_nombre_estado.data
        if not id_estado:
            mensaje.value = "Seleccione un estado para eliminar."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_eliminacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "DELETE FROM tabla_estados WHERE id_estado = %s"
            parametros = (id_estado,)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Estado eliminado con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de eliminar el estado con ID {id_estado}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_eliminacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def limpiar_campos(e):
        """Limpia los campos del formulario."""
        txt_nombre_estado.value = ""
        txt_nombre_estado.data = None
        mensaje.value = ""
        page.update()

    # Diseño de la pantalla
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Gestión de Estados", size=20, weight=ft.FontWeight.BOLD)]),
                ft.Row([txt_nombre_estado]),
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar", on_click=registrar_estado, bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Actualizar", on_click=actualizar_estado, bgcolor=ft.colors.BLUE),
                        ft.ElevatedButton("Eliminar", on_click=eliminar_estado, bgcolor=ft.colors.RED),
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
