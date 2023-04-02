import mysql.connector
import sys

connection = None

try:

    def getConnection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="UIP2023Root_",
            database="inventorySys"
        )

    def createTables():
        tables = ["CREATE TABLE IF NOT EXISTS inventory (id INT AUTO_INCREMENT PRIMARY KEY, product_name VARCHAR(255) NOT NULL, quantity INT NOT NULL, price DECIMAL(10,2) NOT NULL)"]
        connection = getConnection()
        cursor = connection.cursor()
        for table in tables:
            cursor.execute(table)


    def principal():
        createTables()
        menu = """
    \n__________________________________________
            SISTEMA DE INVENTARIO
    a) Agregar nuevo producto
    b) Editar producto existente
    c) Eliminar producto existente
    d) Ver lista de productos
    e) Buscar producto por nombre
    f) Salir
    __________________________________________
    Selecciona una opción: """

        option = ""
        while option != "f":
            option = input(menu).lower()
            if option == "a":
                name = input("Ingresa el nombre del producto: ")
                # Comprobar si el producto ya existe
                product = getProduct(name)
                if product is not None:
                    print(f"El producto '{name}' ya existe")
                # Si no existe:
                else:
                    quantity = int(input("Ingresa la cantidad: "))
                    price = float(input("Ingresa el precio: "))
                    addProduct(name, quantity, price)
                    print(f"Producto agregado: {name}")
            if option == "b":
                name = input("Ingresa el nombre del producto que quieres editar: ")
                quantity = int(input("Ingresa la nueva cantidad: "))
                price = float(input("Ingresa el nuevo precio: "))
                editProduct(name, quantity, price)
                print(f"Producto actualizado: {name}")
            if option == "c":
                name = input("Ingresa el nombre del producto a eliminar: ")
                removeProduct(name)
                print(f"Producto eliminado: {name}")
            if option == "d":
                products = getProducts()
                print("=== Lista de productos ===")
                print("Nombre Producto                         -    Precio      -      Stock       ")
                for product in products:
                    print(f"{product[0]}                        -    {product[2]}       -      {product[1]}")
            if option == "e":
                name = input("Ingresa el nombre del producto que deseas buscar: ")
                product = getProduct(name)
                if product is not None:
                    print(f"El producto '{name}' tiene una cantidad de {product[0]} y un precio de {product[1]}")
                else:
                    print(f"Producto '{name}' no encontrado")
        else:
            print("\nEl programa ha finalizado")
            sys.exit()


    #MÉTODO PARA AGREGAR PRODUCTO
    def addProduct(name, quantity, price):
        connection = getConnection()
        cursor = connection.cursor()
        statement = "INSERT INTO inventory (product_name, quantity, price) VALUES (%s, %s, %s)"
        cursor.execute(statement, (name, quantity, price))
        connection.commit()

    #MÉTODO PARA EDITAR PRODUCTO
    def editProduct(name, quantity, price):
        connection = getConnection()
        cursor = connection.cursor()
        statement = "UPDATE inventory SET quantity = %s, price = %s WHERE product_name = %s"
        cursor.execute(statement, (quantity, price, name))
        connection.commit()


    #MÉTODO PARA ELIMINAR PRODUCTO
    def removeProduct(name):
        connection = getConnection()
        cursor = connection.cursor()
        statement = "DELETE FROM inventory WHERE product_name = %s"
        cursor.execute(statement, (name,))
        connection.commit()

    #MÉTODO PARA OBTENER PRODUCTOS
    def getProducts():
        connection = getConnection()
        cursor = connection.cursor()
        query = "SELECT product_name, quantity, price FROM inventory"
        cursor.execute(query)
        return cursor.fetchall()

    #MÉTODO PARA OBTENER PRODUCTO POR NOMBRE
    def getProduct(name):
        connection = getConnection()
        cursor = connection.cursor()
        query = "SELECT quantity, price FROM inventory WHERE product_name = %s"
        cursor.execute(query, (name,))
        return cursor.fetchone()


    #GARANTIZAR QUE LA FUNCIÓN 'principal' SOLO SE EJECUTE CUANDO EL ARCHIVO SE EJECUTA COMO PROGRAMA PRINCIPAL Y NO CUANDO SE IMPORTA COMO MÓDULO
    if __name__ == '__main__':
        principal()

#MANEJO DE EXCEPCIONES
except ValueError:
    print("ExceptionError - ValueError: Database not connected")

except TypeError:
    print("ExceptionError - TypeError: Database not connected")

except TimeoutError:
    print("ExceptionError - Timeout: Database not connected")

finally:
    # CIERRE DE CONEXION A BASE DE DATOS MYSQL
    if connection is not None:
        getConnection().close