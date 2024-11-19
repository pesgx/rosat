import flet as ft
from db.conexion import ConexionBD

def pantalla_aparatos(page):
    """Pantalla para la gestión de aparatos"""

    # Método para cerrar la aplicación (temporalmente en lugar de volver a menú principal)
    def cerrar_aplicacion(e):
        page.window_close()  # Cierra la ventana de Flet

    txt_nombre_aparato = ft.TextField(label="Nombre del Aparato", width=300)
    mensaje = ft.Text("", size=14, color=ft.colors.GREEN)

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre del Aparato")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[],
    )

    def cargar_datos():
        """Carga los datos de la tabla de la base de datos en la interfaz"""
        conexion = ConexionBD()
        conexion.conectar()
        consulta = "SELECT id_aparato, nombre_aparato FROM tabla_aparatos"
        resultados = conexion.ejecutar_consulta(consulta)
        conexion.cerrar()

        tabla_datos.rows.clear()
        if resultados:
            for fila in resultados:
                tabla_datos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(fila[0]))),
                            ft.DataCell(ft.Text(fila[1])),
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
        """Selecciona una fila y autocompleta los campos"""
        txt_nombre_aparato.value = nombre
        txt_nombre_aparato.data = id
        mensaje.value = ""
        page.update()

    def registrar_aparato(e):
        """Registra un nuevo aparato en la base de datos"""
        nombre = txt_nombre_aparato.value.strip()
        if not nombre:
            mensaje.value = "El campo 'Nombre del Aparato' está vacío."
            mensaje.color = ft.colors.RED
            page.update()
            return

        conexion = ConexionBD()
        conexion.conectar()
        consulta = "INSERT INTO tabla_aparatos (nombre_aparato) VALUES (%s)"
        parametros = (nombre,)
        conexion.ejecutar_consulta(consulta, parametros)
        conexion.cerrar()

        mensaje.value = "¡Aparato registrado con éxito!"
        mensaje.color = ft.colors.GREEN
        txt_nombre_aparato.value = ""
        cargar_datos()

    def actualizar_aparato(e):
        """Actualiza el nombre del aparato seleccionado"""
        id_aparato = txt_nombre_aparato.data
        nombre = txt_nombre_aparato.value.strip()
        if not id_aparato or not nombre:
            mensaje.value = "Seleccione un aparato para actualizar."
            mensaje.color = ft.colors.RED
            page.update()
            return

        # Diálogo de confirmación para actualizar
        def confirmar_actualizacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "UPDATE tabla_aparatos SET nombre_aparato = %s WHERE id_aparato = %s"
            parametros = (nombre, id_aparato)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Aparato actualizado con éxito!"
            mensaje.color = ft.colors.GREEN
            txt_nombre_aparato.value = ""
            txt_nombre_aparato.data = None
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        def cancelar_actualizacion(e):
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de actualizar el aparato con ID {id_aparato}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_actualizacion),
                ft.TextButton("Confirmar", on_click=confirmar_actualizacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def eliminar_aparato(e):
        """Elimina el aparato seleccionado"""
        id_aparato = txt_nombre_aparato.data
        if not id_aparato:
            mensaje.value = "Seleccione un aparato para eliminar."
            mensaje.color = ft.colors.RED
            page.update()
            return

        # Diálogo de confirmación para eliminar
        def confirmar_eliminacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "DELETE FROM tabla_aparatos WHERE id_aparato = %s"
            parametros = (id_aparato,)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Aparato eliminado con éxito!"
            mensaje.color = ft.colors.GREEN
            txt_nombre_aparato.value = ""
            txt_nombre_aparato.data = None
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        def cancelar_eliminacion(e):
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de eliminar el aparato con ID {id_aparato}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_eliminacion),
                ft.TextButton("Confirmar", on_click=confirmar_eliminacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def limpiar_campos(e):
        """Limpia los campos del formulario"""
        txt_nombre_aparato.value = ""
        txt_nombre_aparato.data = None
        mensaje.value = ""
        page.update()

    # Diseño de la pantalla
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Gestión de Aparatos", size=20, weight=ft.FontWeight.BOLD)]),
                ft.Row([txt_nombre_aparato]),
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar", on_click=registrar_aparato, bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Actualizar", on_click=actualizar_aparato, bgcolor=ft.colors.BLUE),
                        ft.ElevatedButton("Eliminar", on_click=eliminar_aparato, bgcolor=ft.colors.RED),
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
