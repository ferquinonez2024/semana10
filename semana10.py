import os


class Producto:
    def _init_(self, id_producto, nombre, cantidad, precio):
        # Atributos del producto
        self._id_producto = id_producto  # ID único del producto
        self._nombre = nombre  # Nombre del producto
        self._cantidad = cantidad  # Cantidad en inventario
        self._precio = precio  # Precio del producto

    # Métodos para leer y escribir cada atributo
    def get_id_producto(self):
        return self._id_producto

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        self._nombre = nombre

    def get_cantidad(self):
        return self._cantidad

    def set_cantidad(self, cantidad):
        self._cantidad = cantidad

    def get_precio(self):
        return self._precio

    def set_precio(self, precio):
        self._precio = precio

    # Método para mostrar la información del producto
    def mostrar_info(self):
        return f"ID: {self._id_producto}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, Precio: {self._precio}"

    # Método para convertir el producto a una línea de texto
    def to_line(self):
        return f"{self._id_producto};{self._nombre};{self._cantidad};{self._precio}"


class Inventario:
    def _init_(self, archivo='inventario.txt'):
        self.productos = []  # Lista para almacenar los productos
        self.archivo = archivo  # Nombre del archivo donde se almacenará el inventario
        self.cargar_inventario()  # Cargar los productos desde el archivo al iniciar

    def cargar_inventario(self):
        # Cargar productos desde el archivo
        if os.path.exists(self.archivo):  # Verificar si el archivo existe
            try:
                with open(self.archivo, 'r') as f:  # Abrir el archivo en modo lectura
                    for linea in f:  # Leer cada línea del archivo
                        # Descomponer la línea en sus componentes
                        id_producto, nombre, cantidad, precio = linea.strip().split(';')
                        # Crear un objeto Producto y añadirlo a la lista
                        producto = Producto(id_producto, nombre, int(cantidad), float(precio))
                        self.productos.append(producto)
            except (FileNotFoundError, PermissionError) as e:
                # Manejo de excepciones si hay problemas al abrir el archivo
                print(f"Error al cargar el inventario: {e}")
        else:
            # Si el archivo no existe, se informa al usuario
            print(f"El archivo {self.archivo} no existe. Se creará uno nuevo.")

    def guardar_inventario(self):
        # Guardar productos en el archivo
        try:
            with open(self.archivo, 'w') as f:  # Abrir el archivo en modo escritura
                for producto in self.productos:  # Iterar sobre los productos
                    f.write(producto.to_line() + '\n')  # Escribir cada producto en el archivo
            print("Inventario guardado exitosamente.")  # Mensaje de éxito
        except (PermissionError, IOError) as e:
            # Manejo de excepciones si hay problemas al guardar el archivo
            print(f"Error al guardar el inventario: {e}")

    def añadir_producto(self, producto):
        # Verificar que el ID del producto sea único antes de añadirlo
        for p in self.productos:
            if p.get_id_producto() == producto.get_id_producto():
                print("Error: Ya existe un producto con ese ID.")  # Mensaje de error
                return
        self.productos.append(producto)  # Añadir el producto a la lista
        self.guardar_inventario()  # Guardar cambios en el archivo
        print("Producto añadido con éxito.")  # Mensaje de éxito

    def eliminar_producto(self, id_producto):
        # Eliminar producto por ID
        for p in self.productos:
            if p.get_id_producto() == id_producto:
                self.productos.remove(p)  # Eliminar el producto de la lista
                self.guardar_inventario()  # Guardar cambios en el archivo
                print("Producto eliminado con éxito.")  # Mensaje de éxito
                return
        print("Error: Producto no encontrado.")  # Mensaje de error

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        # Actualizar cantidad o precio de un producto por ID
        for p in self.productos:
            if p.get_id_producto() == id_producto:
                if cantidad is not None:
                    p.set_cantidad(cantidad)  # Actualizar cantidad si se proporciona
                if precio is not None:
                    p.set_precio(precio)  # Actualizar precio si se proporciona
                self.guardar_inventario()  # Guardar cambios en el archivo
                print("Producto actualizado con éxito.")  # Mensaje de éxito
                return
        print("Error: Producto no encontrado.")  # Mensaje de error

    def buscar_producto(self, nombre):
        # Buscar productos por nombre
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            for p in resultados:
                print(p.mostrar_info())  # Mostrar información de los productos encontrados
        else:
            print("No se encontraron productos con ese nombre.")  # Mensaje de error

    def mostrar_todos(self):
        # Mostrar todos los productos en el inventario
        if self.productos:
            for p in self.productos:
                print(p.mostrar_info())  # Mostrar información de cada producto
        else:
            print("El inventario está vacío.")  # Mensaje si no hay productos


# Impresión en pantalla
def menu():
    inventario = Inventario()  # Crear una instancia de Inventario

    while True:
        # Mostrar menú de opciones al usuario
        print("\nSistema de Gestión de Inventarios")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad o precio de un producto")
        print("4. Buscar producto(s) por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")  # Solicitar opción al usuario

        if opcion == '1':  # Opción para añadir un nuevo producto
            id_producto = input("Ingrese el ID del producto: ")
            nombre = input("Ingrese el nombre del producto: ")
            cantidad = int(input("Ingrese la cantidad: "))
            precio = float(input("Ingrese el precio: "))
            producto = Producto(id_producto, nombre, cantidad, precio)  # Crear un nuevo producto
            inventario.añadir_producto(producto)  # Añadir el producto al inventario

        elif opcion == '2':  # Opción para eliminar un producto
            id_producto = input("Ingrese el ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)  # Eliminar el producto del inventario

        elif opcion == '3':  # Opción para actualizar un producto
            id_producto = input("Ingrese el ID del producto a actualizar: ")
            cantidad = input("Ingrese la nueva cantidad (o presione Enter para no cambiarla): ")
            precio = input("Ingrese el nuevo precio (o presione Enter para no cambiarlo): ")
            cantidad = int(cantidad) if cantidad else None  # Convertir a int o None
            precio = float(precio) if precio else None  # Convertir a float o None
            inventario.actualizar_producto(id_producto, cantidad, precio)  # Actualizar el producto

        elif opcion == '4':  # Opción para buscar productos
            nombre = input("Ingrese el nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)  # Buscar el producto en el inventario

        elif opcion == '5':  # Opción para mostrar todos los productos
            inventario.mostrar_todos()  # Mostrar todos los productos en el inventario

        elif opcion == '6':  # Opción para salir
            print("Saliendo del sistema...")  # Mensaje de salida
            break  # Romper el bucle y salir

        else:
            print("Opción no válida. Intente de nuevo.")  # Mensaje de error para opción no válida


if _name_ == "_main_":
    menu()  # Ejecutar el menú al iniciar el programa