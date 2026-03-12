from models.menu import MenuModel

model = MenuModel()


class MenuController:

    def get_products(self):
        return model.get_all()

    def create_product(self, nombre, descripcion, precio, stock, ruta_imagen=None):
        return model.create(nombre, descripcion, float(precio), int(stock), ruta_imagen)

    def update_product(self, id, nombre, descripcion, precio, stock, ruta_imagen=None):
        return model.update(id, nombre, descripcion, float(precio), int(stock), ruta_imagen)

    def delete_product(self, id):
        return model.delete(id)

    def toggle_disponible(self, id, disponible: bool):
        return model.toggle_disponible(id, disponible)