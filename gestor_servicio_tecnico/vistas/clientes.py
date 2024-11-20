import flet as ft
from db.conexion import ConexionBD

def pantalla_clientes(page):
    """
    Pantalla para la gestión de clientes.
    Permite registrar, actualizar, eliminar y listar clientes.
    Valida el NIF y los teléfonos para que contengan exactamente 9 dígitos.
    Incluye un combo para seleccionar la población desde la tabla_poblacion.
    """

    # Método para cerrar la aplicación (temporalmente en lugar de volver a menú principal)
    def cerrar_aplicacion(e):
        page.window_close()  # Cierra la ventana de Flet

    # Campos de entrada
    txt_codigo_cliente = ft.TextField(label="Código del Cliente", width=300)
    txt_nombre_cliente = ft.TextField(label="Nombre del Cliente", width=300)
    txt_nombre_comercial = ft.TextField(label="Nombre Comercial", width=300)
    txt_nif_cliente = ft.TextField(label="NIF del Cliente", width=300)
    txt_domicilio = ft.TextField(label="Domicilio", width=300)
    combo_poblacion = ft.Dropdown(label="Población", width=300, options=[])
    txt_telefono_1 = ft.TextField(label="Teléfono 1", width=300)
    txt_telefono_2 = ft.TextField(label="Teléfono 2", width=300)
    txt_nota_cliente = ft.TextField(label="Nota del Cliente", multiline=True, width=300)
    mensaje = ft.Text("", size=14, color=ft.colors.GREEN)

    # Tabla de datos
    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("NIF")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Población")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[],
    )

    def cargar_datos():
        """Carga los datos de la tabla de clientes desde la base de datos en la interfaz."""
        conexion = ConexionBD()
        try:
            conexion.conectar()
            consulta = """
                SELECT c.id_cliente, c.codigo_cliente, c.nombre_cliente, c.nombre_cliente_comercial, 
                       c.nif_cliente, c.domicilio, c.telefono_1, c.telefono_2, c.nota_cliente, 
                       p.nombre_poblacion
                FROM tabla_clientes c
                LEFT JOIN tabla_poblacion p ON c.poblacion_id = p.id_poblacion
            """
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
                            ft.DataCell(ft.Text(fila[4])),  # NIF
                            ft.DataCell(ft.Text(str(fila[6]))),  # Teléfono 1
                            ft.DataCell(ft.Text(fila[9])),  # Población
                            ft.DataCell(
                                ft.ElevatedButton(
                                    "Seleccionar",
                                    on_click=lambda e, id=fila[0], codigo=fila[1], nombre=fila[2],
                                    comercial=fila[3], nif=fila[4], domicilio=fila[5],
                                    telefono_1=fila[6], telefono_2=fila[7], nota=fila[8],
                                    poblacion=fila[9]: seleccionar_fila(id, codigo, nombre, comercial, nif,
                                                                        domicilio, telefono_1, telefono_2, nota, poblacion),
                                )
                            ),
                        ]
                    )
                )
        page.update()

    def cargar_poblaciones():
        """Carga las poblaciones desde la tabla_poblacion en el combo."""
        conexion = ConexionBD()
        try:
            conexion.conectar()
            consulta = "SELECT id_poblacion, nombre_poblacion FROM tabla_poblacion"
            resultados = conexion.ejecutar_consulta(consulta)
        except Exception as e:
            mensaje.value = f"Error al cargar poblaciones: {str(e)}"
            mensaje.color = ft.colors.RED
        finally:
            conexion.cerrar()

        combo_poblacion.options.clear()
        if resultados:
            for fila in resultados:
                combo_poblacion.options.append(ft.dropdown.Option(key=fila[0], text=fila[1]))  # ID como key, nombre como texto
        page.update()

    def seleccionar_fila(id, codigo, nombre, comercial, nif, domicilio, telefono_1, telefono_2, nota, poblacion):
        """Selecciona una fila y autocompleta los campos."""
        txt_codigo_cliente.value = codigo
        txt_nombre_cliente.value = nombre
        txt_nombre_comercial.value = comercial
        txt_nif_cliente.value = nif
        txt_domicilio.value = domicilio
        txt_telefono_1.value = str(telefono_1)
        txt_telefono_2.value = str(telefono_2)
        txt_nota_cliente.value = nota

        # Selecciona la población en el combo
        for opcion in combo_poblacion.options:
            if opcion.text == poblacion:
                combo_poblacion.value = opcion.key
                break

        txt_codigo_cliente.data = id  # Guardar el ID del cliente para futuras acciones
        mensaje.value = ""  # Limpia el mensaje previo
        page.update()

    def validar_numerico(campo, nombre_campo):
        """Valida que el campo sea numérico y tenga 9 dígitos."""
        if not campo.isdigit() or len(campo) != 9:
            raise ValueError(f"{nombre_campo} debe contener exactamente 9 dígitos.")
        return campo

    def registrar_cliente(e):
        """Registra un nuevo cliente en la base de datos."""
        codigo = txt_codigo_cliente.value.strip()
        nombre = txt_nombre_cliente.value.strip()
        comercial = txt_nombre_comercial.value.strip()
        nif = txt_nif_cliente.value.strip()
        domicilio = txt_domicilio.value.strip()
        poblacion_id = combo_poblacion.value
        telefono_1 = txt_telefono_1.value.strip()
        telefono_2 = txt_telefono_2.value.strip()
        nota = txt_nota_cliente.value.strip()

        if not codigo or not nombre or not nif or not poblacion_id:
            mensaje.value = "Todos los campos obligatorios deben completarse."
            mensaje.color = ft.colors.RED
            page.update()
            return

        try:
            validar_numerico(telefono_1, "Teléfono 1")
            validar_numerico(telefono_2, "Teléfono 2")
        except ValueError as ve:
            mensaje.value = str(ve)
            mensaje.color = ft.colors.RED
            page.update()
            return

        conexion = ConexionBD()
        try:
            conexion.conectar()
            consulta = """
                INSERT INTO tabla_clientes (codigo_cliente, nombre_cliente, nombre_cliente_comercial, nif_cliente, 
                                             domicilio, poblacion_id, telefono_1, telefono_2, nota_cliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            parametros = (codigo, nombre, comercial, nif, domicilio, poblacion_id, telefono_1, telefono_2, nota)
            conexion.ejecutar_consulta(consulta, parametros)
            mensaje.value = "¡Cliente registrado con éxito!"
            mensaje.color = ft.colors.GREEN
        except Exception as e:
            mensaje.value = f"Error al registrar cliente: {str(e)}"
            mensaje.color = ft.colors.RED
        finally:
            conexion.cerrar()

        limpiar_campos(None)
        cargar_datos()

    def actualizar_cliente(e):
        """Actualiza los datos del cliente seleccionado."""
        id_cliente = txt_codigo_cliente.data
        codigo = txt_codigo_cliente.value.strip()
        nombre = txt_nombre_cliente.value.strip()
        comercial = txt_nombre_comercial.value.strip()
        nif = txt_nif_cliente.value.strip()
        domicilio = txt_domicilio.value.strip()
        poblacion_id = combo_poblacion.value
        telefono_1 = txt_telefono_1.value.strip()
        telefono_2 = txt_telefono_2.value.strip()
        nota = txt_nota_cliente.value.strip()

        if not id_cliente:
            mensaje.value = "Seleccione un cliente para actualizar."
            mensaje.color = ft.colors.RED
            page.update()
            return

        if not codigo or not nombre or not nif or not poblacion_id:
            mensaje.value = "Todos los campos obligatorios deben completarse."
            mensaje.color = ft.colors.RED
            page.update()
            return

        try:
            validar_numerico(telefono_1, "Teléfono 1")
            validar_numerico(telefono_2, "Teléfono 2")
        except ValueError as ve:
            mensaje.value = str(ve)
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_actualizacion(e):
            conexion = ConexionBD()
            try:
                conexion.conectar()
                consulta = """
                    UPDATE tabla_clientes 
                    SET codigo_cliente = %s, nombre_cliente = %s, nombre_cliente_comercial = %s, nif_cliente = %s, 
                        domicilio = %s, poblacion_id = %s, telefono_1 = %s, telefono_2 = %s, nota_cliente = %s
                    WHERE id_cliente = %s
                """
                parametros = (codigo, nombre, comercial, nif, domicilio, poblacion_id, telefono_1, telefono_2, nota, id_cliente)
                conexion.ejecutar_consulta(consulta, parametros)
                mensaje.value = "¡Cliente actualizado con éxito!"
                mensaje.color = ft.colors.GREEN
            except Exception as e:
                mensaje.value = f"Error al actualizar cliente: {str(e)}"
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
            content=ft.Text(f"¿Estás seguro de actualizar el cliente con ID {id_cliente}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_actualizacion),
            ],
        )
        page.dialog.open = True
        page.update()

        # Completar con métodos actualizar_cliente y eliminar_cliente siguiendo la estructura de marcas.py

    def eliminar_cliente(e):
        """Elimina el cliente seleccionado."""
        id_cliente = txt_codigo_cliente.data

        if not id_cliente:
            mensaje.value = "Seleccione un cliente para eliminar."
            mensaje.color = ft.colors.RED
            page.update()
            return

        def confirmar_eliminacion(e):
            conexion = ConexionBD()
            try:
                conexion.conectar()
                consulta = "DELETE FROM tabla_clientes WHERE id_cliente = %s"
                parametros = (id_cliente,)
                conexion.ejecutar_consulta(consulta, parametros)
                mensaje.value = "¡Cliente eliminado con éxito!"
                mensaje.color = ft.colors.GREEN
            except Exception as e:
                mensaje.value = f"Error al eliminar cliente: {str(e)}"
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
            content=ft.Text(f"¿Estás seguro de eliminar el cliente con ID {id_cliente}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: [setattr(page.dialog, "open", False), page.update()]),
                ft.TextButton("Confirmar", on_click=confirmar_eliminacion),
            ],
        )
        page.dialog.open = True
        page.update()


    def limpiar_campos(e):
        """Limpia los campos del formulario."""
        txt_codigo_cliente.value = ""
        txt_nombre_cliente.value = ""
        txt_nombre_comercial.value = ""
        txt_nif_cliente.value = ""
        txt_domicilio.value = ""
        txt_telefono_1.value = ""
        txt_telefono_2.value = ""
        txt_nota_cliente.value = ""
        combo_poblacion.value = None
        txt_codigo_cliente.data = None
        mensaje.value = ""
        page.update()

    # Diseño de la pantalla
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Gestión de Clientes", size=20, weight=ft.FontWeight.BOLD)]),
                ft.Row([txt_codigo_cliente, txt_nombre_cliente, txt_nombre_comercial]),
                ft.Row([txt_nif_cliente, txt_domicilio]),
                ft.Row([combo_poblacion, txt_telefono_1, txt_telefono_2]),
                ft.Row([txt_nota_cliente]),
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar", on_click=registrar_cliente, bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Actualizar", on_click=actualizar_cliente, bgcolor=ft.colors.BLUE),  # Actualizar
                        ft.ElevatedButton("Eliminar", on_click=eliminar_cliente, bgcolor=ft.colors.RED),  # Eliminar
                        ft.ElevatedButton("Limpiar", on_click=limpiar_campos, bgcolor=ft.colors.GREY),
                        ft.ElevatedButton("Volver", on_click=cerrar_aplicacion, bgcolor=ft.colors.ORANGE),
                    ]
                ),
                mensaje,  # Mensaje para notificaciones
                tabla_datos,
            ],
            spacing=20,
        )
    )
    cargar_poblaciones()
    cargar_datos()
