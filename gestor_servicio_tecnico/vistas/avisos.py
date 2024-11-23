from db.conexion import ConexionBD
import base64
import flet as ft
import psycopg2

def pantalla_avisos(page: ft.Page):
    """
    Interfaz gráfica para la gestión de avisos, diseñada con Flet.
    Organiza los campos en filas, proporciona un diseño web responsive
    y botones para las acciones principales.
    """
    page.title = "Gestión de Avisos"
    page.scroll = "adaptive"

    # Contenedor principal
    contenedor_principal = ft.Column(
        expand=True,
        spacing=10,
        controls=[]
    )

    # Campos de entrada organizados por secciones
    campos_seccion_1 = ft.Row(
        controls=[
            ft.TextField(label="ID Aviso", read_only=True),
            ft.TextField(label="Número Aviso"),
            ft.TextField(label="Número Expediente"),
            ft.DatePicker(label="Fecha Recepción", format="dd/MM/yyyy"),
            ft.DatePicker(label="Fecha Reparación", format="dd/MM/yyyy"),
            ft.TextField(label="Hora Agenda", hint_text="hh:mm"),
        ]
    )

    campos_seccion_2 = ft.Row(
        controls=[
            ft.Dropdown(label="Nombre Cliente", options=[]),
            ft.TextField(label="Nombre Comercial Cliente"),
            ft.TextField(label="NIF Cliente"),
            ft.TextField(label="Domicilio"),
            ft.TextField(label="ID Población"),
            ft.TextField(label="Teléfono 1"),
            ft.TextField(label="Teléfono 2"),
        ]
    )

    campos_seccion_3 = ft.Row(
        controls=[
            ft.Dropdown(label="ID Aparato", options=[]),
            ft.Dropdown(label="Marca", options=[]),
            ft.TextField(label="Modelo"),
            ft.TextField(label="Número de Serie"),
            ft.TextField(label="Código"),
        ]
    )

    campos_seccion_4 = ft.Row(
        controls=[
            ft.TextField(label="Descripción Avería"),
            ft.TextField(label="Descripción Reparación"),
            ft.TextField(label="Nota"),
            ft.Dropdown(label="Empleado", options=[]),
            ft.Dropdown(label="Compañía", options=[]),
            ft.Dropdown(label="Grupo", options=[]),
        ]
    )

    campos_seccion_5 = ft.Row(
        controls=[
            ft.Dropdown(label="Estado Aviso", options=[]),
            ft.TextField(label="Archivo Adjunto 1"),
            ft.TextField(label="Archivo Adjunto 2"),
            ft.TextField(label="Archivo Adjunto 3"),
            ft.TextField(label="Archivo Firma"),
        ]
    )

    campos_seccion_6 = ft.Row(
        controls=[
            ft.TextField(label="Base Importe"),
            ft.TextField(label="Porcentaje Importe"),
            ft.TextField(label="Impuesto Importe"),
            ft.TextField(label="Importe Aviso"),
        ]
    )

    # Tabla para mostrar los datos
    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("ID Aviso")),
            ft.DataColumn(label=ft.Text("Número Aviso")),
            ft.DataColumn(label=ft.Text("Número Expediente")),
            ft.DataColumn(label=ft.Text("Fecha Recepción")),
            ft.DataColumn(label=ft.Text("Nombre Cliente")),
            ft.DataColumn(label=ft.Text("Nombre Comercial Cliente")),
            ft.DataColumn(label=ft.Text("ID Población")),
            ft.DataColumn(label=ft.Text("ID Aparato")),
            ft.DataColumn(label=ft.Text("Marca")),
            ft.DataColumn(label=ft.Text("Empleado")),
            ft.DataColumn(label=ft.Text("Compañía")),
            ft.DataColumn(label=ft.Text("Grupo")),
            ft.DataColumn(label=ft.Text("Estado Aviso")),
        ],
        rows=[],
    )

    # Contenedor de botones
    contenedor_botones = ft.Row(
        controls=[
            ft.ElevatedButton("Guardar"),
            ft.ElevatedButton("Modificar"),
            ft.ElevatedButton("Eliminar"),
            ft.ElevatedButton("Limpiar"),
            ft.ElevatedButton("Volver"),
            ft.ElevatedButton("Insertar Línea"),
        ]
    )

    contenedor_botones_archivos = ft.Row(
        controls=[
            ft.ElevatedButton("Generar PDF"),
            ft.ElevatedButton("Adjuntar Archivo 1"),
            ft.ElevatedButton("Adjuntar Archivo 2"),
            ft.ElevatedButton("Adjuntar Archivo 3"),
            ft.ElevatedButton("Adjuntar Firma"),
        ]
    )

    # Añadir los componentes al contenedor principal
    contenedor_principal.controls.extend([
        campos_seccion_1,
        campos_seccion_2,
        campos_seccion_3,
        campos_seccion_4,
        campos_seccion_5,
        campos_seccion_6,
        tabla_datos,
        contenedor_botones,
        contenedor_botones_archivos,
    ])

    # Añadir el contenedor principal a la página
    page.add(contenedor_principal)
