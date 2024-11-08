import mysql.connector

def obtener_conexion():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='mydb'
        )
        print("Conexión exitosa a la base de datos.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

if __name__ == "__main__":
    conexion = obtener_conexion()
    if conexion:
        conexion.close()