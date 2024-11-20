from db.conexion import ConexionBD
import flet as ft

def pantalla_avisos(page):
    """
    Pantalla principal para la gestión de avisos.
    Incluye contenedores, tablas y botones para CRUD.
    """

    # Campos y objetos de la interfaz
    txt_id_aviso = ft.TextField(label="ID Aviso", width=150, read_only=True)
    txt_numero_aviso = ft.TextField(label="Número de Aviso", width=150)
    txt_numero_expediente = ft.TextField(label="Número de Expediente", width=150)
    txt_fecha_recepcion = ft.TextField(label="Fecha de Recepción (dd/mm/aaaa)", width=150)
    txt_fecha_reparacion = ft.TextField(label="Fecha de Reparación (dd/mm/aaaa)", width=150)
    txt_hora_agenda = ft.TextField(label="Hora Agenda (00:00)", width=150)
    combo_cliente = ft.Dropdown(label="Cliente", width=150, options=[])
    combo_aparato = ft.Dropdown(label="Aparato", width=150, options=[])
    combo_marca = ft.Dropdown(label="Marca", width=150, options=[])
    txt_modelo = ft.TextField(label="Modelo", width=150)
    txt_numero_serie = ft.TextField(label="Número de Serie", width=150)
    txt_codigo = ft.TextField(label="Código", width=150)
    txt_descripcion_averia = ft.TextField(label="Descripción de Avería", multiline=True, width=150)
    txt_descripcion_reparacion = ft.TextField(label="Descripción de Reparación", multiline=True, width=150)
    txt_nota = ft.TextField(label="Nota", multiline=True, width=150)
    combo_empleado = ft.Dropdown(label="Empleado", width=150, options=[])
    combo_compañia = ft.Dropdown(label="Compañía", width=150, options=[])
    combo_grupo = ft.Dropdown(label="Grupo", width=150, options=[])
    combo_estado_aviso = ft.Dropdown(label="Estado del Aviso", width=150, options=[])
    mensaje = ft.Text("", size=14, color=ft.colors.GREEN)

    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Número de Aviso")),
            ft.DataColumn(ft.Text("Número de Expediente")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[],
    )

    # Botones
    boton_registrar = ft.ElevatedButton(
        "Registrar",
        on_click=lambda e: registrar_aviso(
            txt_numero_aviso.value.strip(), txt_numero_expediente.value.strip(),
            txt_fecha_recepcion.value.strip(), txt_fecha_reparacion.value.strip(),
            txt_hora_agenda.value.strip(), combo_cliente.value, combo_aparato.value,
            combo_marca.value, txt_modelo.value.strip(), txt_numero_serie.value.strip(),
            txt_codigo.value.strip(), txt_descripcion_averia.value.strip(),
            txt_descripcion_reparacion.value.strip(), txt_nota.value.strip(),
            combo_empleado.value, combo_compañia.value, combo_grupo.value,
            combo_estado_aviso.value, mensaje
        ),
        bgcolor=ft.colors.GREEN,
    )

    boton_actualizar = ft.ElevatedButton(
        "Actualizar",
        on_click=lambda e: actualizar_aviso(
            txt_id_aviso.data, txt_numero_aviso.value.strip(), txt_numero_expediente.value.strip(),
            txt_fecha_recepcion.value.strip(), txt_fecha_reparacion.value.strip(),
            txt_hora_agenda.value.strip(), combo_cliente.value, combo_aparato.value,
            combo_marca.value, txt_modelo.value.strip(), txt_numero_serie.value.strip(),
            txt_codigo.value.strip(), txt_descripcion_averia.value.strip(),
            txt_descripcion_reparacion.value.strip(), txt_nota.value.strip(),
            combo_empleado.value, combo_compañia.value, combo_grupo.value,
            combo_estado_aviso.value, mensaje
        ),
        bgcolor=ft.colors.BLUE,
    )

    boton_eliminar = ft.ElevatedButton(
        "Eliminar",
        on_click=lambda e: eliminar_aviso(txt_id_aviso.data, mensaje),
        bgcolor=ft.colors.RED,
    )

    boton_cargar = ft.ElevatedButton(
        "Cargar Datos",
        on_click=lambda e: cargar_datos(tabla_datos, mensaje),
        bgcolor=ft.colors.ORANGE,
    )

    # Diseño de la pantalla
    contenedor_datos_aviso = ft.Container(
        content=ft.Row(
            [
                ft.TextField(label="Número de Aviso", width=150),
                ft.TextField(label="Número de Expediente", width=150),
                ft.TextField(label="Fecha de Recepción (dd/mm/aaaa)", width=150),
                ft.TextField(label="Fecha de Reparación (dd/mm/aaaa)", width=150),
                ft.TextField(label="Hora Agenda (00:00)", width=150),
            ],
            spacing=5,
        ),
        padding=5,
        border=ft.border.all(1, ft.colors.GREY),
    )

    # Contenedor 2: Datos del Cliente
    contenedor_datos_cliente = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Dropdown(label="Cliente", width=100, options=[]),
                        ft.TextField(label="Código del Cliente", width=100),
                        ft.TextField(label="Nombre del Cliente", width=100),
                        ft.TextField(label="Nombre Comercial", width=100),
                    ],
                    spacing=5,
                ),
                ft.Row(
                    [
                        ft.TextField(label="NIF", width=100),
                        ft.TextField(label="Domicilio", width=100),
                        ft.TextField(label="Teléfono 1", width=100),
                        ft.TextField(label="Teléfono 2", width=100),
                        ft.TextField(label="Nota", multiline=True, width=100),
                    ],
                    spacing=5,
                ),
            ],
            spacing=5,
        ),
        padding=5,
        border=ft.border.all(1, ft.colors.GREY),
    )

    # Contenedor 3: Datos del Aparato
    contenedor_aparato = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Dropdown(label="Aparato", width=100, options=[]),
                        ft.Dropdown(label="Marca", width=100, options=[]),
                        ft.TextField(label="Modelo", width=100),
                        ft.TextField(label="Número de Serie", width=100),
                        ft.TextField(label="Código", width=100),
                    ],
                    spacing=5,
                ),
                ft.Row(
                    [
                        ft.TextField(label="Descripción de Avería", multiline=True, width=100),
                        ft.TextField(label="Descripción de Reparación", multiline=True, width=100),
                        ft.TextField(label="Nota", multiline=True, width=100),
                    ],
                    spacing=5,
                ),
            ],
            spacing=5,
        ),
        padding=5,
        border=ft.border.all(1, ft.colors.GREY),
    )

    # Contenedor 4: Adjuntos
    contenedor_adjuntos = ft.Container(
        content=ft.Row(
            [
                ft.Dropdown(label="Empleado", width=100, options=[]),
                ft.Dropdown(label="Compañía", width=100, options=[]),
                ft.Dropdown(label="Grupo", width=100, options=[]),
                ft.Dropdown(label="Estado del Aviso", width=100, options=[]),
                ft.TextField(label="Archivos Adjuntos", width=100),
                ft.ElevatedButton("Subir Archivo", bgcolor=ft.colors.BLUE),
            ],
            spacing=5,
        ),
        padding=5,
        border=ft.border.all(1, ft.colors.GREY),
    )

    # Contenedor 5: Líneas del Aviso
    contenedor_lineas_aviso = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.ElevatedButton("Añadir", bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Actualizar", bgcolor=ft.colors.BLUE),
                        ft.ElevatedButton("Eliminar", bgcolor=ft.colors.RED),
                    ],
                    spacing=5,
                ),
                ft.Row(
                    [
                        ft.Dropdown(label="Artículo", width=100, options=[]),
                        ft.TextField(label="Cantidad", width=100),
                        ft.TextField(label="Precio Unitario", width=100),
                        ft.TextField(label="Total Línea", width=100, read_only=True),
                    ],
                    spacing=5,
                ),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Artículo")),
                        ft.DataColumn(ft.Text("Cantidad")),
                        ft.DataColumn(ft.Text("Precio")),
                        ft.DataColumn(ft.Text("Total")),
                    ],
                    rows=[],
                ),
            ],
            spacing=5,
        ),
        padding=5,
        border=ft.border.all(1, ft.colors.GREY),
    )

    # Contenedor 6: Totales del Aviso
    contenedor_total_aviso = ft.Container(
        content=ft.Row(
            [
                ft.TextField(label="Base Importe", width=100, read_only=True),
                ft.TextField(label="Porcentaje Importe", width=100),
                ft.TextField(label="Impuesto Importe", width=100, read_only=True),
                ft.TextField(label="Importe Total", width=100, read_only=True),
            ],
            spacing=5,
        ),
        padding=5,
        border=ft.border.all(1, ft.colors.GREY),
    )

    # Contenedor 7: Tabla de Datos
    contenedor_tabla_datos = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Dropdown(label="Filtrar por Campo", width=100, options=[]),
                        ft.TextField(label="Buscar", width=100),
                        ft.ElevatedButton("Buscar", bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Mostrar Todos", bgcolor=ft.colors.BLUE),
                    ],
                    spacing=5,
                ),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Número de Aviso")),
                        ft.DataColumn(ft.Text("Número de Expediente")),
                        ft.DataColumn(ft.Text("Cliente")),
                        ft.DataColumn(ft.Text("Estado")),
                    ],
                    rows=[],
                ),
            ],
            spacing=5,
        ),
        padding=5,
        border=ft.border.all(1, ft.colors.GREY),
    )




    # Añadir todos los contenedores a la página
    page.add(
        ft.Column(
            [
                contenedor_datos_aviso,
                contenedor_datos_cliente,
                contenedor_aparato,
                contenedor_adjuntos,
                contenedor_lineas_aviso,
                contenedor_total_aviso,
                contenedor_tabla_datos,
            ],
            spacing=5,
        )
    )

# Funciones CRUD

def actualizar_aviso(
    id_aviso, numero_aviso, numero_expediente, fecha_recepcion, fecha_reparacion,
    hora_agenda, cliente_id, aparato_id, marca_id, modelo, numero_serie,
    codigo, descripcion_averia, descripcion_reparacion, nota, empleado_id,
    compañia_id, grupo_id, estado_aviso_id, mensaje_obj
):
    """Actualiza los datos de un aviso existente."""
    if not id_aviso:
        mensaje_obj.value = "Seleccione un aviso para actualizar."
        mensaje_obj.color = ft.colors.RED
        return

    conexion = ConexionBD()
    try:
        conexion.conectar()
        consulta = """
            UPDATE tabla_avisos
            SET numero_aviso = %s, numero_expediente = %s, fecha_recepcion = %s,
                fecha_reparacion = %s, hora_agenda = %s, cliente_id = %s,
                aparato_id = %s, marca_id = %s, modelo = %s, numero_serie = %s,
                codigo = %s, descripcion_averia = %s, descripcion_reparacion = %s,
                nota = %s, empleado_id = %s, compañia_id = %s, grupo_id = %s,
                estado_aviso_id = %s
            WHERE id_aviso = %s
        """
        parametros = (
            numero_aviso, numero_expediente, fecha_recepcion, fecha_reparacion, hora_agenda,
            cliente_id, aparato_id, marca_id, modelo, numero_serie, codigo,
            descripcion_averia, descripcion_reparacion, nota, empleado_id,
            compañia_id, grupo_id, estado_aviso_id, id_aviso
        )
        conexion.ejecutar_consulta(consulta, parametros)
        mensaje_obj.value = "¡Aviso actualizado con éxito!"
        mensaje_obj.color = ft.colors.GREEN
    except Exception as e:
        mensaje_obj.value = f"Error al actualizar aviso: {str(e)}"
        mensaje_obj.color = ft.colors.RED
    finally:
        conexion.cerrar()

def registrar_aviso(
    numero_aviso, numero_expediente, fecha_recepcion, fecha_reparacion,
    hora_agenda, cliente_id, aparato_id, marca_id, modelo, numero_serie,
    codigo, descripcion_averia, descripcion_reparacion, nota, empleado_id,
    compañia_id, grupo_id, estado_aviso_id, mensaje_obj
):
    """Registra un nuevo aviso en la base de datos."""
    if not numero_aviso or not cliente_id or not aparato_id or not empleado_id:
        mensaje_obj.value = "Todos los campos obligatorios deben completarse."
        mensaje_obj.color = ft.colors.RED
        return

    conexion = ConexionBD()
    try:
        conexion.conectar()
        consulta = """
            INSERT INTO tabla_avisos (
                numero_aviso, numero_expediente, fecha_recepcion, fecha_reparacion, hora_agenda,
                cliente_id, aparato_id, marca_id, modelo, numero_serie, codigo,
                descripcion_averia, descripcion_reparacion, nota, empleado_id,
                compañia_id, grupo_id, estado_aviso_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        parametros = (
            numero_aviso, numero_expediente, fecha_recepcion, fecha_reparacion, hora_agenda,
            cliente_id, aparato_id, marca_id, modelo, numero_serie, codigo,
            descripcion_averia, descripcion_reparacion, nota, empleado_id,
            compañia_id, grupo_id, estado_aviso_id
        )
        conexion.ejecutar_consulta(consulta, parametros)
        mensaje_obj.value = "¡Aviso registrado con éxito!"
        mensaje_obj.color = ft.colors.GREEN
    except Exception as e:
        mensaje_obj.value = f"Error al registrar aviso: {str(e)}"
        mensaje_obj.color = ft.colors.RED
    finally:
        conexion.cerrar()



def eliminar_aviso(id_aviso, mensaje_obj):
    """Elimina un aviso de la base de datos."""
    if not id_aviso:
        mensaje_obj.value = "Seleccione un aviso para eliminar."
        mensaje_obj.color = ft.colors.RED
        return

    conexion = ConexionBD()
    try:
        conexion.conectar()
        consulta = "DELETE FROM tabla_avisos WHERE id_aviso = %s"
        conexion.ejecutar_consulta(consulta, (id_aviso,))
        mensaje_obj.value = "¡Aviso eliminado con éxito!"
        mensaje_obj.color = ft.colors.GREEN
    except Exception as e:
        mensaje_obj.value = f"Error al eliminar aviso: {str(e)}"
        mensaje_obj.color = ft.colors.RED
    finally:
        conexion.cerrar()


def cargar_datos(tabla_datos, mensaje_obj):
    """Carga los avisos en la tabla principal."""
    conexion = ConexionBD()
    try:
        conexion.conectar()
        consulta = """
            SELECT id_aviso, numero_aviso, numero_expediente, cliente_id, estado_aviso_id
            FROM tabla_avisos
            ORDER BY id_aviso DESC
            LIMIT 30
        """
        resultados = conexion.ejecutar_consulta(consulta)
    except Exception as e:
        mensaje_obj.value = f"Error al cargar datos: {str(e)}"
        mensaje_obj.color = ft.colors.RED
        return
    finally:
        conexion.cerrar()

    tabla_datos.rows.clear()
    if resultados:
        for fila in resultados:
            tabla_datos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(fila[1]))),  # Número de Aviso
                        ft.DataCell(ft.Text(fila[2])),  # Número de Expediente
                        ft.DataCell(ft.Text(str(fila[3]))),  # Cliente
                        ft.DataCell(ft.Text(str(fila[4]))),  # Estado
                        ft.DataCell(
                            ft.ElevatedButton(
                                "Seleccionar",
                                on_click=lambda e, id=fila[0]: seleccionar_aviso(id),
                            )
                        ),
                    ]
                )
            )
