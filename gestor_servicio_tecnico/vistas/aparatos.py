import flet as ft
from db.conexion import ConexionBD

def pantalla_aparatos(page, volver_menu_principal):
    """Pantalla para la gestión de aparatos"""

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
        txt_nombre_aparato.value = nombre
        txt_nombre_aparato.data = id
        mensaje.value = ""
        page.update()

    def registrar_aparato(e):
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

    def limpiar_campos(e):
        txt_nombre_aparato.value = ""
        txt_nombre_aparato.data = None
        mensaje.value = ""
        page.update()

    def volver_al_menu(e):
        page.clean()
        volver_menu_principal(page)

    # Diseño de la pantalla
    page.add(
        ft.Column(
            [
                ft.Row([ft.Text("Gestión de Aparatos", size=20, weight=ft.FontWeight.BOLD)]),
                ft.Row([txt_nombre_aparato]),
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar", on_click=registrar_aparato, bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Limpiar", on_click=limpiar_campos, bgcolor=ft.colors.GREY),
                        ft.ElevatedButton("Volver al Menú", on_click=volver_al_menu, bgcolor=ft.colors.BLUE),
                    ]
                ),
                mensaje,
                tabla_datos,
            ],
            spacing=20,
        )
    )
    cargar_datos()
