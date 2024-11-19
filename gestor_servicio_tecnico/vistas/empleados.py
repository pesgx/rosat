import flet as ft
from db.conexion import ConexionBD

def pantalla_empleados(page):
    """
    Pantalla para la gestión de empleados.
    Permite registrar, actualizar, eliminar y listar empleados.
    """
    # Método para cerrar la aplicación (temporalmente en lugar de volver a menú principal)
    def cerrar_aplicacion(e):
        page.window_close()  # Cierra la ventana de Flet

    txt_nombre_empleado = ft.TextField(label="Nombre del Empleado", width=300)
    mensaje = ft.Text("", size=14, color=ft.colors.GREEN)  # Mensaje para notificaciones

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre del Empleado")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[],
    )

    def cargar_datos():
        """Carga los datos de la tabla de empleados desde la base de datos en la interfaz."""
        conexion = ConexionBD()
        conexion.conectar()
        consulta = "SELECT id_empleado, nombre_empleado FROM tabla_empleados"
        resultados = conexion.ejecutar_consulta(consulta)
        conexion.cerrar()

        tabla_datos.rows.clear()
        if resultados:
            for fila in resultados:
                tabla_datos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(fila[0]))),  # ID
                            ft.DataCell(ft.Text(fila[1])),  # Nombre del Empleado
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
        txt_nombre_empleado.value = nombre
        txt_nombre_empleado.data = id  # Guardar el ID del empleado para futuras acciones
        mensaje.value = ""  # Limpia el mensaje previo
        page.update()

    def registrar_empleado(e):
        """Registra un nuevo empleado en la base de datos."""
        nombre = txt_nombre_empleado.value.strip()

        if not nombre:
            mensaje.value = "El campo 'Nombre del Empleado' está vacío."
            mensaje.color = ft.colors.RED
            page.update()
            return

        conexion = ConexionBD()
        conexion.conectar()
        consulta = "INSERT INTO tabla_empleados (nombre_empleado) VALUES (%s)"
        parametros = (nombre,)
        conexion.ejecutar_consulta(consulta, parametros)
        conexion.cerrar()

        mensaje.value = "¡Empleado registrado con éxito!"
        mensaje.color = ft.colors.GREEN
        limpiar_campos(None)
        cargar_datos()

    def actualizar_empleado(e):
        """Actualiza los datos del empleado seleccionado."""
        id_empleado = txt_nombre_empleado.data
        nombre = txt_nombre_empleado.value.strip()

        if not id_empleado or not nombre:
            mensaje.value = "Seleccione un empleado para actualizar y complete el campo."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_actualizacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "UPDATE tabla_empleados SET nombre_empleado = %s WHERE id_empleado = %s"
            parametros = (nombre, id_empleado)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Empleado actualizado con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de actualizar el empleado con ID {id_empleado}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_actualizacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def eliminar_empleado(e):
        """Elimina el empleado seleccionado."""
        id_empleado = txt_nombre_empleado.data
        if not id_empleado:
            mensaje.value = "Seleccione un empleado para eliminar."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_eliminacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "DELETE FROM tabla_empleados WHERE id_empleado = %s"
            parametros = (id_empleado,)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Empleado eliminado con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de eliminar el empleado con ID {id_empleado}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_eliminacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def limpiar_campos(e):
        """Limpia los campos del formulario."""
        txt_nombre_empleado.value = ""
        txt_nombre_empleado.data = None
        mensaje.value = ""
        page.update()

    # Diseño de la pantalla
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Gestión de Empleados", size=20, weight=ft.FontWeight.BOLD)]),
                ft.Row([txt_nombre_empleado]),
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar", on_click=registrar_empleado, bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Actualizar", on_click=actualizar_empleado, bgcolor=ft.colors.BLUE),
                        ft.ElevatedButton("Eliminar", on_click=eliminar_empleado, bgcolor=ft.colors.RED),
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
