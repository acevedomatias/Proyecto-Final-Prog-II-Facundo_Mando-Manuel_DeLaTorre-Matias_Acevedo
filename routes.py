from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Producto, CarritoItem

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/quienes_somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@main.route('/contacto')
def contacto():
    return render_template('contacto.html')

@main.route('/preguntas_frecuentes')
def preguntas_frecuentes():
    return render_template('preguntasfrecuentes.html')

@main.route('/catalogo')
def catalogo():
    productos = Producto.query.all()
    return render_template('catalogo.html', productos=productos)

@main.route('/add_to_cart/<int:producto_id>')
def add_to_cart(producto_id):
    cart = session.get('cart', {})
    producto_id = str(producto_id)
    if producto_id in cart:
        cart[producto_id] += 1
    else:
        cart[producto_id] = 1
    session['cart'] = cart
    return redirect(url_for('main.catalogo'))

@main.route('/carrito')
def carrito():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for producto_id, cantidad in cart.items():
        producto = Producto.query.get(int(producto_id))
        if producto:
            total += producto.precio * cantidad
            cart_items.append({'producto': producto, 'cantidad': cantidad, 'total_price': producto.precio * cantidad})
    return render_template('carrito.html', cart_items=cart_items, total=total)

@main.route('/remove_from_cart/<int:producto_id>')
def remove_from_cart(producto_id):
    cart = session.get('cart', {})
    producto_id = str(producto_id)
    if producto_id in cart:
        cart[producto_id] -= 1
        if cart[producto_id] <= 0:
            del cart[producto_id]
        session['cart'] = cart
    return redirect(url_for('main.carrito'))

#  agregar productos
@main.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        imagen_url = request.form['imagen_url']
        nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, imagen_url=imagen_url)
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('main.catalogo'))
    return render_template('agregar_producto.html')

# editar productos
@main.route('/editar_producto/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.precio = request.form['precio']
        producto.imagen_url = request.form['imagen_url']
        db.session.commit()
        return redirect(url_for('main.catalogo'))
    return render_template('editar_producto.html', producto=producto)

@main.route('/eliminar_producto/<int:producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('main.catalogo'))
