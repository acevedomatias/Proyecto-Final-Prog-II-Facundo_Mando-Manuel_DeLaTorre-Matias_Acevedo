from app import app
from models import db, Producto

with app.app_context():
    db.create_all()
    if not Producto.query.first():
        productos = [
            Producto(nombre="Producto 1", descripcion="Descripción del producto 1", precio=100.0, imagen_url="ruta_a_imagen1.jpg"),
            Producto(nombre="Producto 2", descripcion="Descripción del producto 2", precio=200.0, imagen_url="ruta_a_imagen2.jpg"),
            Producto(nombre="Producto 3", descripcion="Descripción del producto 3", precio=300.0, imagen_url="ruta_a_imagen3.jpg"),
        ]
        db.session.bulk_save_objects(productos)
        db.session.commit()
    print("Base de datos inicializada con productos.")

