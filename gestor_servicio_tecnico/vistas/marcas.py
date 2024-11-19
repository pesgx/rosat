import flet as ft
from db.conexion import ConexionBD

def pantalla_marcas(page):
    """
    Pantalla para la gestión de marcas.
    Permite registrar, actualizar, eliminar y listar marcas.
    Incluye un combo para seleccionar el grupo asociado desde la tabla_grupos.
    """
    # Método para cerrar la aplicación (temporalmente en lugar de volver a menú principal)
    def cerrar_aplicacion(e):
        page.window_close()  # Cierra la ventana de Flet

    txt_nombre_marca = ft.TextField(label="Nombre de la Marca", width=300)
    combo_grupo = ft.Dropdown(label="Grupo", width=300, options=[])  # Combo para seleccionar grupo
    mensaje = ft.Text("", size=14, color=ft.colors.GREEN)  # Mensaje para notificaciones

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre de la Marca")),
            ft.DataColumn(ft.Text("Grupo Asociado")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[],
    )

    def cargar_datos():
        """Carga los datos de la tabla de marcas desde la base de datos en la interfaz."""
        conexion = ConexionBD()
        conexion.conectar()
        consulta = """
            SELECT m.id_marca, m.nombre_marca, g.nombre_grupo
            FROM tabla_marcas m
            LEFT JOIN tabla_grupos g ON m.grupo_id = g.id_grupo
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
                            ft.DataCell(ft.Text(fila[1])),  # Nombre de la Marca
                            ft.DataCell(ft.Text(fila[2])),  # Grupo Asociado
                            ft.DataCell(
                                ft.ElevatedButton(
                                    "Seleccionar",
                                    on_click=lambda e, id=fila[0], nombre=fila[1], grupo=fila[2]: seleccionar_fila(id, nombre, grupo),
                                )
                            ),
                        ]
                    )
                )
        page.update()

    def cargar_grupos():
        """Carga los grupos desde la tabla_grupos en el combo."""
        conexion = ConexionBD()
        conexion.conectar()
        consulta = "SELECT id_grupo, nombre_grupo FROM tabla_grupos"
        resultados = conexion.ejecutar_consulta(consulta)
        conexion.cerrar()

        combo_grupo.options.clear()
        if resultados:
            for fila in resultados:
                combo_grupo.options.append(ft.dropdown.Option(key=fila[0], text=fila[1]))  # ID como key, nombre como texto
        page.update()

    def seleccionar_fila(id, nombre, grupo):
        """Selecciona una fila y autocompleta los campos."""
        txt_nombre_marca.value = nombre
        txt_nombre_marca.data = id  # Guardar el ID de la marca para futuras acciones
        for opcion in combo_grupo.options:
            if opcion.text == grupo:  # Busca y selecciona el grupo en el combo
                combo_grupo.value = opcion.key
                break
        mensaje.value = ""  # Limpia el mensaje previo
        page.update()

    def registrar_marca(e):
        """Registra una nueva marca en la base de datos."""
        nombre = txt_nombre_marca.value.strip()
        grupo_id = combo_grupo.value

        if not nombre or not grupo_id:
            mensaje.value = "Todos los campos son obligatorios."
            mensaje.color = ft.colors.RED
            page.update()
            return

        conexion = ConexionBD()
        conexion.conectar()
        consulta = "INSERT INTO tabla_marcas (nombre_marca, grupo_id) VALUES (%s, %s)"
        parametros = (nombre, grupo_id)
        conexion.ejecutar_consulta(consulta, parametros)
        conexion.cerrar()

        mensaje.value = "¡Marca registrada con éxito!"
        mensaje.color = ft.colors.GREEN
        limpiar_campos(None)
        cargar_datos()

    def actualizar_marca(e):
        """Actualiza los datos de la marca seleccionada."""
        id_marca = txt_nombre_marca.data
        nombre = txt_nombre_marca.value.strip()
        grupo_id = combo_grupo.value

        if not id_marca or not nombre or not grupo_id:
            mensaje.value = "Seleccione una marca para actualizar y complete todos los campos."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_actualizacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "UPDATE tabla_marcas SET nombre_marca = %s, grupo_id = %s WHERE id_marca = %s"
            parametros = (nombre, grupo_id, id_marca)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Marca actualizada con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de actualizar la marca con ID {id_marca}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_actualizacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def eliminar_marca(e):
        """Elimina la marca seleccionada."""
        id_marca = txt_nombre_marca.data
        if not id_marca:
            mensaje.value = "Seleccione una marca para eliminar."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_eliminacion(e):
            conexion = ConexionBD()
            conexion.conectar()
            consulta = "DELETE FROM tabla_marcas WHERE id_marca = %s"
            parametros = (id_marca,)
            conexion.ejecutar_consulta(consulta, parametros)
            conexion.cerrar()

            mensaje.value = "¡Marca eliminada con éxito!"
            mensaje.color = ft.colors.GREEN
            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de eliminar la marca con ID {id_marca}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_eliminacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def limpiar_campos(e):
        """Limpia los campos del formulario."""
        txt_nombre_marca.value = ""
        combo_grupo.value = None
        txt_nombre_marca.data = None
        mensaje.value = ""
        page.update()

    # Diseño de la pantalla
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Gestión de Marcas", size=20, weight=ft.FontWeight.BOLD)]),
                ft.Row([txt_nombre_marca]),
                ft.Row([combo_grupo]),
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar", on_click=registrar_marca, bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Actualizar", on_click=actualizar_marca, bgcolor=ft.colors.BLUE),
                        ft.ElevatedButton("Eliminar", on_click=eliminar_marca, bgcolor=ft.colors.RED),
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
    cargar_grupos()  # Carga los valores del combo al inicio
    cargar_datos()
