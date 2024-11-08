from mysql.connector import MySQLConnection, Error
import configparser
import bcrypt

class Database:
    def __init__(self, config_file, section='biblioteca'):
        self.connection = None
        self.cursor = None
        self.config_file = config_file  # Guardamos el nombre del archivo
        self.section = section          # Guardamos la sección a leer (por defecto 'mysql')

    def load_config(self):
        """Carga y devuelve la configuración de la base de datos desde el archivo .ini."""
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        if self.section in config:
            return dict(config[self.section])
        else:
            raise Exception(f"La sección {self.section} no se encontró en {self.config_file}")

    def connect(self):
        """Establece la conexión y el cursor usando la configuración cargada."""
        try:
            config_db = self.load_config()#cargar el config_db recibido del config.ini
            self.connection = MySQLConnection(**config_db)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Conexión exitosa")#comprobacion de la conexion
        except Error as error:
            print("Error en la conexión:", error)

    def get_column_names(self, table_name):
        """Obtiene los nombres de las columnas de una tabla específica."""
        query = f"SHOW COLUMNS FROM {table_name}"
        columns = []
        if self.cursor:
            try:
                self.cursor.execute(query)
                for column in self.cursor.fetchall():
                    columns.append(column[0])  # Devuelve los nombres de las columnas
                return columns
            except Error as error:
                print("Error al obtener los nombres de las columnas:", error)
                return columns
            
    def execute_query(self, query, params=None):
        """Ejecuta una consulta con parámetros opcionales y devuelve los resultados."""
        if self.cursor:
            try:
                self.cursor.execute(query, params)
                # Comprueba si la consulta es de tipo SELECT o SHOW para usar fetchall()
                if query.strip().upper().startswith("SELECT") or "SHOW" in query.upper():
                    result = self.cursor.fetchall()  # Lee todos los resultados para evitar el error
                    return result
                else:
                    self.connection.commit()  # Para consultas de escritura
                    return None
            except Error as error:
                print("Error al ejecutar la consulta:", error)
                return None
        else:
            print("La conexión no está establecida.")
            return None
        
    def check_user(self, usuario: str, contra: str) -> bool:
        '''
        Obtiene el usuario recibido y revisa la contraseña recibida comparándola con la almacenada en la DB.
        Devuelve True si las contraseñas coinciden, de lo contrario devuelve False.
        '''
        flag = False
        try:
            # Realizar la consulta para obtener el ID del usuario por nombre
            resultado = self.execute_query("SELECT id FROM usuarios WHERE nombre = %s", (usuario,))

            # Verificar si el usuario existe
            if resultado:
                id_usuario = resultado[0][0]  # Obtener el ID del usuario

                # Realizar la consulta para obtener la contraseña hasheada del usuario
                resultado = self.execute_query("SELECT password FROM usuarios WHERE id = %s", (id_usuario,))
                
                # Verificar si la contraseña existe
                if resultado:
                    passw_hasheada = resultado[0][0]  # Obtener la contraseña hasheada de la DB
                    
                    # Comparar la contraseña proporcionada con la hasheada en la DB
                    if bcrypt.checkpw(contra.encode('utf-8'), passw_hasheada.encode('utf-8')):
                        flag = True  # Las contraseñas coinciden
                    else:
                        print("Contraseña incorrecta")
                else:
                    print("Contraseña no encontrada")
            else:
                print("Usuario no encontrado")
        except Error as err:
            print(f"Error: {err}")
        finally:
            return flag
    
    @staticmethod
    def hashear(contra:str)->str:
        return bcrypt.hashpw(contra.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    def close(self):
        """Cierra el cursor y la conexión."""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")


# Uso de la clase con un archivo de configuración de cualquier nombre
db = Database('config.ini','biblioteca')  # Puede ser cualquier archivo .ini con la estructura adecuada
db.connect()

# # Realizar una consulta
# resultados = db.execute_query("SELECT * FROM categoria_producto")#INSERTAR CONSULTA
# if resultados:
#     for fila in resultados:
#         print(fila)

print(db.check_user("admin","admin"))


# # try:
#     db.execute_query("INSERT INTO producto(nombre,descripcion,precio_unitario,precio_mayorista,alerta_stock,stock_actual,idcategoria) VALUES (%s,%s,%s,%s,%s,%s,%s)",('terere', 'tremendo refrescante natural', 10, 5, 10, 900, 2)) #Esto funciona para insertar un valor a la DB
# except:
#     print("eror")
# print(db.execute_query("SELECT * FROM clientes"))
# Cerrar la conexión
db.close()
