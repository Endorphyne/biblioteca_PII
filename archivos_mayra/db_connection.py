import mysql.connector
from configparser import ConfigParser

def get_db_connection():
    config = ConfigParser()
    config.read('Proyecto_Biblioteca/config.ini')
    
    try:
        connection = mysql.connector.connect(
            host=config['mysql']['host'],
            port=config['mysql']['port'],
            database=config['mysql']['database'],
            user=config['mysql']['user'],
            password=config['mysql']['password']
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
    return None
