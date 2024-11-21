from db.conexion import ConexionBD

conexion = ConexionBD()
try:
    conexion.conectar()
    consulta = """
        SELECT codigo_cliente, nombre_cliente, nombre_cliente_comercial, nif_cliente,
               domicilio, telefono_1, telefono_2, nota_cliente
        FROM tabla_clientes
        WHERE id_cliente = %s
    """
    id_prueba = 6  # Cambia este ID por uno existente en tu base de datos
    resultado = conexion.ejecutar_consulta(consulta, (id_prueba,))
    print(resultado)
finally:
    conexion.cerrar()
