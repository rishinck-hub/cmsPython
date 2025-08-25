import configparser 
import mysql.connector
from mysql.connector import Error

class DBConnection:
    'Establish a singleton connection with db'
    '''This class will create only one instance'''
    __instance = None       #To store the singleton instance

    def __new__(cls):
        """
        Override to implement singleton
        Ensures only one instance of DBConnection is ever created
        """
        if cls.__instance is None:          #If no instance created 
            cls.__instance = super(DBConnection, cls).__new__(cls)
            cls.__instance.__initialize()   #Initialize the connection
        return cls.__instance               #Return the same instance
    
    def __initialize(self):
        """
        Initialize the database connection using properties
        from the db_config.ini
        """
        try:
            #Load the configuration file
            config = configparser.ConfigParser()
            config.read("db_config.ini")
            #Establish the MySQL connection
            self.connection = mysql.connector.connect(
                host = config.get("mysql", "host"),
                user = config.get("mysql", "user"),
                password = config.get("mysql", "password"),
                database = config.get("mysql", "database")
            )
            if self.connection.is_connected():
                print("Connected to MYSQL database..")
        except Error as e:
            print(f"Error while connecting to MYSQL: {e}")
            self.connection = None

    def get_connection(self):
        return self.connection
    