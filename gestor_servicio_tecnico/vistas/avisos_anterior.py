from db.conexion import ConexionBD
import base64
import flet as ft
import psycopg2



'''  ################################################################################################################

                                                    INTERFAZ GRAFICA

################################################################################################################   '''
def pantalla_avisos(page):
    """
    Pantalla principal para la gestión de avisos.
    Incluye contenedores, tablas y botones para CRUD.
    """

    # Definir los campos de cliente como globales para accesibilidad
    global txt_codigo, txt_nombre, txt_nombre_comercial, txt_nif, txt_domicilio
    global txt_telefono_1, txt_telefono_2, txt_nota
    global txt_archivos_adjuntos  # Asegurar que sea accesible globalmente
    # Variable global para almacenar temporalmente los datos del archivo
    archivo_binario = None
    # Definir `lineas_avisos` fuera de las funciones para que esté accesible
    lineas_avisos = []  #''' lista para almarcenar los datos de linea avisos del contenedor_lineas_aviso en la función manejar_añadir_linea'''
    

    # Campos y objetos de la interfaz
    # Dropdown para seleccionar un aviso existente o añadir uno nuevo
    dropdown_numero_aviso = ft.Dropdown(
        label="Número de Aviso",
        width=200, 
    )
    txt_numero_aviso = ft.TextField(label="Número de Aviso", width=150)
    txt_numero_expediente = ft.TextField(label="Número de Expediente", width=150)
    txt_fecha_recepcion = ft.TextField(label="Fecha de Recepción (dd/mm/aaaa)", width=150)
    txt_fecha_reparacion = ft.TextField(label="Fecha de Reparación (dd/mm/aaaa)", width=150)
    txt_hora_agenda = ft.TextField(label="Hora Agenda (00:00)", width=150)
    combo_cliente = ft.Dropdown(label="Cliente", width=200, options=cargar_clientes(), on_change=manejar_seleccion_cliente)
    combo_aparato = ft.Dropdown(label="Aparato", width=150, options=cargar_aparatos())
    combo_marca = ft.Dropdown(label="Marca", width=150, options=cargar_marcas())
    txt_modelo = ft.TextField(label="Modelo", width=150)
    txt_numero_serie = ft.TextField(label="Número de Serie", width=150)
    txt_codigo = ft.TextField(label="Código", width=150)
    txt_descripcion_averia = ft.TextField(label="Descripción de Avería", multiline=True, width=150)
    txt_descripcion_reparacion = ft.TextField(label="Descripción de Reparación", multiline=True, width=150)
    txt_nota = ft.TextField(label="Nota", multiline=True, width=150)
    combo_empleado = ft.Dropdown(label="Empleado", width=150, options=cargar_empleados())
    combo_compañia = ft.Dropdown(label="Compañía", width=150, options=cargar_compañias())
    combo_grupo = ft.Dropdown(label="Grupo", width=150, options=cargar_grupos())
    combo_estado_aviso = ft.Dropdown(label="Estado del Aviso", width=150, options=cargar_estados())
    txt_archivos_adjuntos = ft.TextField(label="Archivos Adjuntos", width=200, read_only=True)
    txt_base_importe = ft.TextField(label="Base Importe (€)", width=150)
    txt_porcentaje_importe = ft.TextField(label="Porcentaje Importe (%)", width=150)
    txt_impuesto_importe = ft.TextField(label="Impuesto Importe (€)", width=150, read_only=True)
    txt_importe_aviso = ft.TextField(label="Importe Total (€)", width=150, read_only=True)
    # Campos de cliente
    txt_codigo = ft.TextField(label="Código del Cliente", width=200, read_only=True)
    txt_nombre = ft.TextField(label="Nombre del Cliente", width=200, read_only=True)
    txt_nombre_comercial = ft.TextField(label="Nombre Comercial", width=200, read_only=True)
    txt_nif = ft.TextField(label="NIF", width=200, read_only=True)
    txt_domicilio = ft.TextField(label="Domicilio", width=200, read_only=True)
    txt_telefono_1 = ft.TextField(label="Teléfono 1", width=200, read_only=True)
    txt_telefono_2 = ft.TextField(label="Teléfono 2", width=200, read_only=True)
    txt_nota = ft.TextField(label="Nota", multiline=True, width=200, read_only=True)

    # Campos para agregar una línea de aviso
    dropdown_articulo = ft.Dropdown(
        label="Artículo", 
        width=200)
    txt_cantidad = ft.TextField(label="Cantidad", width=200)
    txt_precio_unitario = ft.TextField(label="Precio Unitario", width=200)
    txt_total_linea = ft.TextField(label="Total Línea", width=200, read_only=True)


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
    '''BOTONES   ######################################################################################'''
    # Botones
    boton_registrar = ft.ElevatedButton(
        "Registrar",
        on_click=lambda e: registrar_aviso(),
        bgcolor=ft.colors.GREEN,
    )

    boton_actualizar = ft.ElevatedButton(
        "Actualizar",
        on_click=lambda e: actualizar_aviso(),
        bgcolor=ft.colors.BLUE,
    )

    boton_eliminar = ft.ElevatedButton(
        "Eliminar",
        on_click=lambda e: eliminar_aviso(),
        bgcolor=ft.colors.RED,
    )
    # Botón para subir archivo
    boton_subir_archivo1 = ft.ElevatedButton(
        "Subir Archivo",
        bgcolor=ft.colors.BLUE,
        on_click=lambda e: manejar_subir_archivo1(e, file_picker),
    )
    # Botón para subir archivo
    boton_subir_archivo2 = ft.ElevatedButton(
        "Subir Archivo",
        bgcolor=ft.colors.BLUE,
        on_click=lambda e: manejar_subir_archivo2(e, file_picker),
    )
    # Botón para subir archivo
    boton_subir_archivo3 = ft.ElevatedButton(
        "Subir Archivo",
        bgcolor=ft.colors.BLUE,
        on_click=lambda e: manejar_subir_archivo3(e, file_picker),
    )
    # Botón para subir archivo
    boton_subir_archivo_firma = ft.ElevatedButton(
        "Subir Archivo",
        bgcolor=ft.colors.BLUE,
        on_click=lambda e: manejar_subir_firma(e, file_picker),
    )



    '''CONTENEDORES   ######################################################################################'''
    
    
    # Diseño de la pantalla
    contenedor_datos_aviso = ft.Container(
        content=ft.Row(
            [
                dropdown_numero_aviso,
                ft.TextField(label="Número de Aviso", width=200),
                ft.TextField(label="Número de Expediente", width=200),
                ft.TextField(label="Fecha de Recepción (dd/mm/aaaa)", width=200),
                ft.TextField(label="Fecha de Reparación (dd/mm/aaaa)", width=200),
                ft.TextField(label="Hora Agenda (00:00)", width=200),
            ],
            spacing=5,
        ),
        padding=5,
        border=ft.border.all(1, ft.colors.GREY),
    )

    # Contenedor 2: Datos del Cliente
# Contenedor de datos del cliente
    contenedor_datos_cliente = ft.Container(
        content=ft.Column(
            [
                ft.Row([combo_cliente, txt_codigo, txt_nombre, txt_nombre_comercial], spacing=5),
                ft.Row([txt_nif, txt_domicilio, txt_telefono_1, txt_telefono_2, txt_nota], spacing=5)
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
                        ft.Dropdown(label="Aparato", width=200, options=cargar_aparatos()),
                        ft.Dropdown(label="Marca", width=200, options=cargar_marcas()),
                        ft.TextField(label="Modelo", width=200),
                        ft.TextField(label="Número de Serie", width=200),
                        ft.TextField(label="Código", width=200),
                    ],
                    spacing=5,
                ),
                ft.Row(
                    [
                        ft.TextField(label="Descripción de Avería", multiline=True, width=200),
                        ft.TextField(label="Descripción de Reparación", multiline=True, width=200),
                        ft.TextField(label="Nota", multiline=True, width=200),
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
                ft.Dropdown(label="Empleado", width=200, options=cargar_empleados()),
                ft.Dropdown(label="Compañía", width=200, options=cargar_compañias()),
                ft.Dropdown(label="Grupo", width=200, options=cargar_grupos()),
                ft.Dropdown(label="Estado del Aviso", width=200, options=cargar_estados()),
                ft.TextField(label="Archivos Adjuntos", width=200),
                txt_archivos_adjuntos,  # Campo de texto para mostrar el archivo
                boton_subir_archivo,   # Botón para seleccionar el archivo
                #ft.ElevatedButton("Subir Archivo", bgcolor=ft.colors.BLUE),
            ],
            spacing=5,
        ),
        padding=5,
        border=ft.border.all(1, ft.colors.GREY),
    )

    '''CONTENEDOR LINEAS AVISO   ######################################################################################'''

    # Ajuste de la función calcular_total para asegurarse de que se ejecute bien

    # Tabla visual para mostrar las líneas añadidas
    tabla_lineas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Artículo")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Precio Unitario")),
            ft.DataColumn(ft.Text("Total Línea")),
        ],
        rows=[],
    )

    # Contenedor para la interfaz de líneas de aviso
    contenedor_lineas_aviso = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        dropdown_articulo,
                        txt_cantidad,
                        txt_precio_unitario,
                        txt_total_linea,
                        boton_añadir_linea,
                    ],
                    spacing=5,
                ),
                tabla_lineas,
            ],
            spacing=10,
        ),
        padding=10,
        border=ft.border.all(1, ft.colors.GREY),
    )


    boton_añadir = ft.ElevatedButton(
        "Añadir",
        bgcolor=ft.colors.GREEN,
        on_click=manejar_añadir_linea,
    )

    # Contenedor 5: Líneas del Aviso
    contenedor_lineas_aviso = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        boton_añadir,
                        ft.ElevatedButton("Actualizar", bgcolor=ft.colors.BLUE),
                        ft.ElevatedButton("Eliminar", bgcolor=ft.colors.RED),
                    ],
                    spacing=5,
                ),
                ft.Row(
                    [
                        ft.Dropdown(label="Artículo", width=200, options=cargar_articulos()),
                        ft.TextField(label="Cantidad", width=200,on_change = calcular_total),
                        ft.TextField(label="Precio Unitario", width=200,on_change = calcular_total),
                        ft.TextField(label="Total Línea", width=200, read_only=True),
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
                ft.TextField(label="Base Importe", width=200, read_only=True),
                ft.TextField(label="Porcentaje Importe", width=200),
                ft.TextField(label="Impuesto Importe", width=200, read_only=True),
                ft.TextField(label="Importe Total", width=200, read_only=True),
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
                        ft.Dropdown(label="Filtrar por Campo", width=200, options=[]),
                        ft.TextField(label="Buscar", width=200),
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

    # Contenedor de botones CRUD
    contenedor_botones_crud = ft.Container(
        content=ft.Row(
            [
                boton_registrar,
                boton_actualizar,
                boton_eliminar,

            ],
            spacing=10,
        ),
        padding=5,
    )


    '''PAGE ADD          #########################################################################################################
    '''
    # Añadir todos los contenedores a la página
    page.add(
        ft.Column(
            [
                contenedor_datos_aviso,
                contenedor_datos_cliente,
                contenedor_aparato,
                contenedor_adjuntos,
                contenedor_lineas_aviso,
                dropdown_numero_aviso,
                contenedor_total_aviso,
                contenedor_tabla_datos,
                contenedor_botones_crud,
            ],
            spacing=5,
        )
    )

'''################################################################################################################

                                                    FUNCIONES

################################################################################################################   '''