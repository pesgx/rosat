import flet as ft
from db.conexion import ConexionBD

def pantalla_companias(page):
    """
    Pantalla para la gestión de compañías.
    Permite registrar, actualizar, eliminar y listar compañías.
    """
    # Método para cerrar la aplicación (temporalmente en lugar de volver a menú principal)
    def cerrar_aplicacion(e):
        page.window_close()  # Cierra la ventana de Flet

    txt_nombre_compania = ft.TextField(label="Nombre de la Compañía", width=300)
    mensaje = ft.Text("", size=14, color=ft.colors.GREEN)  # Mensaje para notificaciones

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre de la Compañía")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[],
    )

    def cargar_datos():
        """Carga los datos de la tabla de compañías desde la base de datos en la interfaz."""
        conexion = ConexionBD()
        conexion.conectar()
        consulta = "SELECT id_compañia, nombre_compañia FROM tabla_compañias"
        resultados = conexion.ejecutar_consulta(consulta)
        conexion.cerrar()

        tabla_datos.rows.clear()
        if resultados:
            for fila in resultados:
                tabla_datos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(fila[0]))),  # ID
                            ft.DataCell(ft.Text(fila[1])),  # Nombre de la Compañía
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
        txt_nombre_compania.value = nombre
        txt_nombre_compania.data = id  # Guardar el ID de la compañía para futuras acciones
        mensaje.value = ""  # Limpia el mensaje previo
        page.update()

    def registrar_compania(e):
        """Registra una nueva compañía en la base de datos."""
        nombre = txt_nombre_compania.value.strip()

        if not nombre:
            mensaje.value = "El campo 'Nombre de la Compañía' está vacío."
            mensaje.color = ft.colors.RED
            page.update()
            return

        conexion = ConexionBD()
        conexion.conectar()
        consulta = "INSERT INTO tabla_compañias (nombre_compañia) VALUES (%s)"
        parametros = (nombre,)
        conexion.ejecutar_consulta(consulta, parametros)
        conexion.cerrar()

        mensaje.value = "¡Compañía registrada con éxito!"
        mensaje.color = ft.colors.GREEN
        limpiar_campos(None)
        cargar_datos()

    def actualizar_compania(e):
        """Actualiza los datos de la compañía seleccionada."""
        id_compania = txt_nombre_compania.data
        nombre = txt_nombre_compania.value.strip()

        if not id_compania or not nombre:
            mensaje.value = "Seleccione una compañía para actualizar y complete el campo."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_actualizacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "UPDATE tabla_compañias SET nombre_compañia = %s WHERE id_compañia = %s"
            parametros = (nombre, id_compania)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Compañía actualizada con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de actualizar la compañía con ID {id_compania}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_actualizacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def eliminar_compania(e):
        """Elimina la compañía seleccionada."""
        id_compania = txt_nombre_compania.data
        if not id_compania:
            mensaje.value = "Seleccione una compañía para eliminar."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_eliminacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "DELETE FROM tabla_compañias WHERE id_compañia = %s"
            parametros = (id_compania,)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Compañía eliminada con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de eliminar la compañía con ID {id_compania}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_eliminacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def limpiar_campos(e):
        """Limpia los campos del formulario."""
        txt_nombre_compania.value = ""
        txt_nombre_compania.data = None
        mensaje.value = ""
        page.update()

    # Diseño de la pantalla
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Gestión de Compañías", size=20, weight=ft.FontWeight.BOLD)]),
                ft.Row([txt_nombre_compania]),
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar", on_click=registrar_compania, bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Actualizar", on_click=actualizar_compania, bgcolor=ft.colors.BLUE),
                        ft.ElevatedButton("Eliminar", on_click=eliminar_compania, bgcolor=ft.colors.RED),
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
