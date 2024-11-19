import flet as ft
from db.conexion import ConexionBD

def pantalla_articulos(page):
    """
    Pantalla para la gestión de artículos.
    Permite registrar, actualizar, eliminar y listar artículos.
    Valida el precio para que el separador de decimales sea un punto (.) y maneja errores con try-except-finally.
    """
    # Método para cerrar la aplicación (temporalmente en lugar de volver a menú principal)
    def cerrar_aplicacion(e):
        page.window_close()  # Cierra la ventana de Flet

    txt_codigo_articulo = ft.TextField(label="Código del Artículo", width=300)
    txt_nombre_articulo = ft.TextField(label="Nombre del Artículo", width=300)
    txt_precio_articulo = ft.TextField(label="Precio del Artículo (€)", width=300)
    mensaje = ft.Text("", size=14, color=ft.colors.GREEN)  # Mensaje para notificaciones

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Precio (€)")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[],
    )

    def cargar_datos():
        """Carga los datos de la tabla de artículos desde la base de datos en la interfaz."""
        conexion = ConexionBD()
        try:
            conexion.conectar()
            consulta = "SELECT id_articulo, codigo_articulo, nombre_articulo, precio_articulo FROM tabla_articulo"
            resultados = conexion.ejecutar_consulta(consulta)
        except Exception as e:
            mensaje.value = f"Error al cargar datos: {str(e)}"
            mensaje.color = ft.colors.RED
        finally:
            conexion.cerrar()

        tabla_datos.rows.clear()
        if resultados:
            for fila in resultados:
                tabla_datos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(fila[0]))),  # ID
                            ft.DataCell(ft.Text(fila[1])),  # Código
                            ft.DataCell(ft.Text(fila[2])),  # Nombre
                            ft.DataCell(ft.Text(f"{fila[3]:.2f}")),  # Precio
                            ft.DataCell(
                                ft.ElevatedButton(
                                    "Seleccionar",
                                    on_click=lambda e, id=fila[0], codigo=fila[1], nombre=fila[2], precio=fila[3]: seleccionar_fila(id, codigo, nombre, precio),
                                )
                            ),
                        ]
                    )
                )
        page.update()

    def seleccionar_fila(id, codigo, nombre, precio):
        """Selecciona una fila y autocompleta los campos."""
        txt_codigo_articulo.value = codigo
        txt_nombre_articulo.value = nombre
        txt_precio_articulo.value = f"{precio:.2f}"  # Mostrar con formato decimal
        txt_codigo_articulo.data = id  # Guardar el ID del artículo para futuras acciones
        mensaje.value = ""  # Limpia el mensaje previo
        page.update()

    def validar_precio(precio):
        """Valida que el precio sea un número con decimales usando punto como separador."""
        if ',' in precio:
            raise ValueError("El precio debe usar el punto (.) como separador de decimales.")
        return float(precio)

    def registrar_articulo(e):
        """Registra un nuevo artículo en la base de datos."""
        codigo = txt_codigo_articulo.value.strip()
        nombre = txt_nombre_articulo.value.strip()
        precio = txt_precio_articulo.value.strip()

        if not codigo or not nombre or not precio:
            mensaje.value = "Todos los campos son obligatorios."
            mensaje.color = ft.colors.RED
            page.update()
            return

        try:
            precio = validar_precio(precio)
        except ValueError as ve:
            mensaje.value = str(ve)
            mensaje.color = ft.colors.RED
            page.update()
            return

        conexion = ConexionBD()
        try:
            conexion.conectar()
            consulta = "INSERT INTO tabla_articulo (codigo_articulo, nombre_articulo, precio_articulo) VALUES (%s, %s, %s)"
            parametros = (codigo, nombre, precio)
            conexion.ejecutar_consulta(consulta, parametros)
            mensaje.value = "¡Artículo registrado con éxito!"
            mensaje.color = ft.colors.GREEN
        except Exception as e:
            mensaje.value = f"Error al registrar artículo: {str(e)}"
            mensaje.color = ft.colors.RED
        finally:
            conexion.cerrar()

        limpiar_campos(None)
        cargar_datos()

    def actualizar_articulo(e):
        """Actualiza los datos del artículo seleccionado."""
        id_articulo = txt_codigo_articulo.data
        codigo = txt_codigo_articulo.value.strip()
        nombre = txt_nombre_articulo.value.strip()
        precio = txt_precio_articulo.value.strip()

        if not id_articulo or not codigo or not nombre or not precio:
            mensaje.value = "Seleccione un artículo para actualizar y complete todos los campos."
            mensaje.color = ft.colors.RED
            page.update()
            return

        try:
            precio = validar_precio(precio)
        except ValueError as ve:
            mensaje.value = str(ve)
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_actualizacion(e):
            conexion = ConexionBD()
            try:
                conexion.conectar()
                consulta = "UPDATE tabla_articulo SET codigo_articulo = %s, nombre_articulo = %s, precio_articulo = %s WHERE id_articulo = %s"
                parametros = (codigo, nombre, precio, id_articulo)
                conexion.ejecutar_consulta(consulta, parametros)
                mensaje.value = "¡Artículo actualizado con éxito!"
                mensaje.color = ft.colors.GREEN
            except Exception as e:
                mensaje.value = f"Error al actualizar artículo: {str(e)}"
                mensaje.color = ft.colors.RED
            finally:
                conexion.cerrar()

            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de actualizar el artículo con ID {id_articulo}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_actualizacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def eliminar_articulo(e):
        """Elimina el artículo seleccionado."""
        id_articulo = txt_codigo_articulo.data
        if not id_articulo:
            mensaje.value = "Seleccione un artículo para eliminar."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_eliminacion(e):
            conexion = ConexionBD()
            try:
                conexion.conectar()
                consulta = "DELETE FROM tabla_articulo WHERE id_articulo = %s"
                parametros = (id_articulo,)
                conexion.ejecutar_consulta(consulta, parametros)
                mensaje.value = "¡Artículo eliminado con éxito!"
                mensaje.color = ft.colors.GREEN
            except Exception as e:
                mensaje.value = f"Error al eliminar artículo: {str(e)}"
                mensaje.color = ft.colors.RED
            finally:
                conexion.cerrar()

            limpiar_campos(None)
            cargar_datos()

            # Cierra el diálogo
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text(f"¿Estás seguro de eliminar el artículo con ID {id_articulo}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_eliminacion),
            ],
        )
        page.dialog.open = True
        page.update()

    def limpiar_campos(e):
        """Limpia los campos del formulario."""
        txt_codigo_articulo.value = ""
        txt_nombre_articulo.value = ""
        txt_precio_articulo.value = ""
        txt_codigo_articulo.data = None
        mensaje.value = ""
        page.update()

    # Diseño de la pantalla
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Gestión de Artículos", size=20, weight=ft.FontWeight.BOLD)]),
                ft.Row([txt_codigo_articulo, txt_nombre_articulo]),
                ft.Row([txt_precio_articulo]),
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar", on_click=registrar_articulo, bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Actualizar", on_click=actualizar_articulo, bgcolor=ft.colors.BLUE),
                        ft.ElevatedButton("Eliminar", on_click=eliminar_articulo, bgcolor=ft.colors.RED),
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
