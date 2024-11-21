from db.conexion import ConexionBD
import base64
import flet as ft



'''  ################################################################################################################

                                                    INTERFAZ GRAFICA

################################################################################################################   '''
def pantalla_avisos(page):
    """
    Pantalla principal para la gestión de avisos.
    Incluye contenedores, tablas y botones para CRUD.
    """
    # Inicializar FilePicker y agregarlo a la página
    file_picker = inicializar_file_picker(page)
    # Definir los campos de cliente como globales para accesibilidad
    global txt_codigo, txt_nombre, txt_nombre_comercial, txt_nif, txt_domicilio
    global txt_telefono_1, txt_telefono_2, txt_nota
    global txt_archivos_adjuntos  # Asegurar que sea accesible globalmente
    # Variable global para almacenar temporalmente los datos del archivo
    archivo_binario = None
    

    # Campos y objetos de la interfaz
    txt_id_aviso = ft.TextField(label="ID Aviso", width=150, read_only=True)
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

    # Mostrar el nombre del archivo en el campo de texto


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
    boton_subir_archivo = ft.ElevatedButton(
        "Subir Archivo",
        bgcolor=ft.colors.BLUE,
        on_click=lambda e: manejar_subir_archivo(e, file_picker),
    )
    # Diseño de la pantalla
    contenedor_datos_aviso = ft.Container(
        content=ft.Row(
            [
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
                        ft.Dropdown(label="Artículo", width=200, options=cargar_articulos()),
                        ft.TextField(label="Cantidad", width=200),
                        ft.TextField(label="Precio Unitario", width=200),
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
                contenedor_botones_crud,
            ],
            spacing=5,
        )
    )

'''################################################################################################################

                                                    FUNCIONES

################################################################################################################   '''
def cargar_clientes():
    """Carga los clientes desde la base de datos y los devuelve como opciones del Dropdown."""
    conexion = ConexionBD()
    opciones = []
    try:
        conexion.conectar()
        consulta = "SELECT id_cliente, nombre_cliente FROM tabla_clientes"
        resultados = conexion.ejecutar_consulta(consulta)
        for fila in resultados:
            opciones.append(ft.dropdown.Option(key=fila[0], text=fila[1]))
    except Exception as e:
        print(f"Error al cargar clientes: {str(e)}")
    finally:
        conexion.cerrar()
    return opciones

def cargar_aparatos():
    """Carga los aparatos desde la base de datos y los devuelve como opciones del Dropdown."""
    conexion = ConexionBD()
    opciones = []
    try:
        conexion.conectar()
        consulta = "SELECT id_aparato, nombre_aparato FROM tabla_aparatos"
        resultados = conexion.ejecutar_consulta(consulta)
        for fila in resultados:
            opciones.append(ft.dropdown.Option(key=fila[0], text=fila[1]))
    except Exception as e:
        print(f"Error al cargar aparatos: {str(e)}")
    finally:
        conexion.cerrar()
    return opciones

def cargar_empleados():
    """Carga los empleados desde la base de datos y los devuelve como opciones del Dropdown."""
    conexion = ConexionBD()
    opciones = []
    try:
        conexion.conectar()
        consulta = "SELECT id_empleado, nombre_empleado FROM tabla_empleados"
        resultados = conexion.ejecutar_consulta(consulta)
        for fila in resultados:
            opciones.append(ft.dropdown.Option(key=fila[0], text=fila[1]))
    except Exception as e:
        print(f"Error al cargar empleados: {str(e)}")
    finally:
        conexion.cerrar()
    return opciones

def cargar_marcas():
    """Carga las marcas desde la base de datos y las devuelve como opciones del Dropdown."""
    conexion = ConexionBD()
    opciones = []
    try:
        conexion.conectar()
        consulta = "SELECT id_marca, nombre_marca FROM tabla_marcas"
        resultados = conexion.ejecutar_consulta(consulta)
        for fila in resultados:
            opciones.append(ft.dropdown.Option(key=fila[0], text=fila[1]))
    except Exception as e:
        print(f"Error al cargar marcas: {str(e)}")
    finally:
        conexion.cerrar()
    return opciones

def cargar_estados():
    """Carga los estados desde la base de datos y los devuelve como opciones del Dropdown."""
    conexion = ConexionBD()
    opciones = []
    try:
        conexion.conectar()
        consulta = "SELECT id_estado, nombre_estado FROM tabla_estados"
        resultados = conexion.ejecutar_consulta(consulta)
        for fila in resultados:
            opciones.append(ft.dropdown.Option(key=fila[0], text=fila[1]))
    except Exception as e:
        print(f"Error al cargar estados: {str(e)}")
    finally:
        conexion.cerrar()
    return opciones

def cargar_articulos():
    """Carga los artículos desde la base de datos y los devuelve como opciones del Dropdown."""
    conexion = ConexionBD()
    opciones = []
    try:
        conexion.conectar()
        consulta = "SELECT id_articulo, nombre_articulo FROM tabla_articulo"
        resultados = conexion.ejecutar_consulta(consulta)
        for fila in resultados:
            opciones.append(ft.dropdown.Option(key=fila[0], text=fila[1]))
    except Exception as e:
        print(f"Error al cargar artículos: {str(e)}")
    finally:
        conexion.cerrar()
    return opciones

def cargar_compañias():
    """Carga las compañías desde la base de datos y las devuelve como opciones del Dropdown."""
    conexion = ConexionBD()
    opciones = []
    try:
        conexion.conectar()
        consulta = "SELECT id_compañia, nombre_compañia FROM tabla_compañias"
        resultados = conexion.ejecutar_consulta(consulta)
        for fila in resultados:
            opciones.append(ft.dropdown.Option(key=fila[0], text=fila[1]))
    except Exception as e:
        print(f"Error al cargar compañías: {str(e)}")
    finally:
        conexion.cerrar()
    return opciones

def cargar_grupos():
    """Carga los grupos desde la base de datos y los devuelve como opciones del Dropdown."""
    conexion = ConexionBD()
    opciones = []
    try:
        conexion.conectar()
        consulta = "SELECT id_grupo, nombre_grupo FROM tabla_grupos"
        resultados = conexion.ejecutar_consulta(consulta)
        for fila in resultados:
            opciones.append(ft.dropdown.Option(key=fila[0], text=fila[1]))
    except Exception as e:
        print(f"Error al cargar grupos: {str(e)}")
    finally:
        conexion.cerrar()
    return opciones

# Función para manejar la selección de un cliente
def manejar_seleccion_cliente(e):
    """
    Maneja la selección de un cliente y autocompleta los campos.
    """
    cliente_id = e.control.value
    if cliente_id:
        datos_cliente = obtener_datos_cliente(cliente_id)
        if datos_cliente:
            txt_codigo.value = datos_cliente.get("codigo_cliente", "")
            txt_nombre.value = datos_cliente.get("nombre_cliente", "")
            txt_nombre_comercial.value = datos_cliente.get("nombre_comercial", "")
            txt_nif.value = datos_cliente.get("nif", "")
            txt_domicilio.value = datos_cliente.get("domicilio", "")
            txt_telefono_1.value = str(datos_cliente.get("telefono_1", ""))
            txt_telefono_2.value = str(datos_cliente.get("telefono_2", ""))
            txt_nota.value = datos_cliente.get("nota", "")
            e.page.update()  # Actualizar la página para reflejar cambios

# Función para cargar clientes en el Dropdown
def cargar_clientes():
    """
    Carga los clientes desde la base de datos y devuelve una lista de opciones.
    """
    conexion = ConexionBD()
    opciones = []
    try:
        conexion.conectar()
        consulta = "SELECT id_cliente, nombre_cliente FROM tabla_clientes"
        resultados = conexion.ejecutar_consulta(consulta)
        for fila in resultados:
            opciones.append(ft.dropdown.Option(key=fila[0], text=fila[1]))
    except Exception as e:
        print(f"Error al cargar clientes: {str(e)}")
    finally:
        conexion.cerrar()
    return opciones

# Función para obtener datos de un cliente específico
def obtener_datos_cliente(cliente_id):
    """
    Recupera los datos de un cliente específico desde la base de datos.
    """
    conexion = ConexionBD()
    datos_cliente = {}
    try:
        conexion.conectar()
        consulta = """
            SELECT codigo_cliente, nombre_cliente, nombre_cliente_comercial, nif_cliente,
                   domicilio, telefono_1, telefono_2, nota_cliente
            FROM tabla_clientes
            WHERE id_cliente = %s
        """
        resultado = conexion.ejecutar_consulta(consulta, (cliente_id,))
        if resultado:
            fila = resultado[0]
            datos_cliente = {
                "codigo_cliente": fila[0],
                "nombre_cliente": fila[1],
                "nombre_comercial": fila[2],
                "nif": fila[3],
                "domicilio": fila[4],
                "telefono_1": fila[5],
                "telefono_2": fila[6],
                "nota": fila[7],
            }
    except Exception as e:
        print(f"Error al obtener datos del cliente: {str(e)}")
    finally:
        conexion.cerrar()
    return datos_cliente

# Función para inicializar el FilePicker
def inicializar_file_picker(page):
    """
    Inicializa el FilePicker y lo agrega al overlay de la página.
    """
    archivo = ft.FilePicker(on_result=lambda result: procesar_archivo(result, page))
    page.overlay.append(archivo)
    page.update()  # Asegurarse de que el FilePicker esté disponible en la página
    return archivo

# Función para manejar la selección del archivo
def manejar_subir_archivo(e, archivo):
    """
    Maneja el evento del botón 'Subir Archivo'.
    Abre el selector de archivos del sistema operativo.
    """
    archivo.pick_files(allow_multiple=False)  # Permite seleccionar un solo archivo


# Función para procesar el archivo seleccionado
# Función para procesar el archivo seleccionado
# Función para procesar el archivo seleccionado
def procesar_archivo(result, page):
    """
    Procesa el archivo seleccionado por el usuario.
    Guarda su nombre en el campo 'txt_archivos_adjuntos' y su contenido binario en memoria.
    """
    global archivo_binario

    if result.files:
        archivo_seleccionado = result.files[0]
        ruta_archivo = archivo_seleccionado.path

        # Leer archivo en formato binario
        with open(ruta_archivo, "rb") as f:
            archivo_binario = f.read()

        # Mostrar el nombre del archivo en el campo de texto
        txt_archivos_adjuntos.value = archivo_seleccionado.name
        page.update()  # Refrescar la página para reflejar los cambios
    print(f"Archivos seleccionados: {result.files}")
    print(f"Nombre del archivo: {archivo_seleccionado.name}")    

# txt_archivos_adjuntos.value = archivo_seleccionado.name
# txt_archivos_adjuntos.page.update()