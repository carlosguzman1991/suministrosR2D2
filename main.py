from flask import Flask, render_template, request, redirect, url_for
from flask import session
import db
from models import Cliente, Admin, Proveedor, Producto, Compra
from sqlalchemy import MetaData, create_engine, table
from datetime import datetime
import json
import os

app = Flask(__name__)
# Configuración de la clave secreta
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://localhost/suministros_R2D2'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/registro/cliente', methods=['GET', 'POST'])
def registro_cliente():
    if request.method == 'POST':
        # datos del formulario de registro
        nombre = request.form.get('nombre')
        contraseña = request.form.get('contraseña')
        direccion = request.form.get('direccion')

        # Crear una nueva instancia de Cliente y guardar en la base de datos
        cliente = Cliente(nombre=nombre, contraseña=contraseña, direccion=direccion)
        db.session.add(cliente)
        db.session.commit()

        # Redirigir a inicio
        return redirect(url_for('home'))

    # Renderiza el formulario de registro de cliente
    return render_template('index.html')

@app.route('/registro/admin', methods=['GET', 'POST'])
def registro_admin():
    if request.method == 'POST':
        # datos de formulario de registro
        nombre_admin = request.form.get('nombre')
        contraseña_admin = request.form.get('contraseña')

        # nueva instancia de Admin y guardar en la base de datos
        admin = Admin(nombre=nombre_admin, contraseña=contraseña_admin)
        db.session.add(admin)
        db.session.commit()

        # Redirigir a inicio
        return redirect(url_for('login_admin'))

    # Renderizar el formulario de registro de administrador
    return render_template('registro_admin.html')



@app.route('/login/cliente', methods=['GET', 'POST'])
def login_cliente():
    if request.method == 'POST':
        # Obtén los datos del formulario de inicio de sesión
        usuario = request.form.get('usuario')
        contraseña = request.form.get('contraseña')

        # Realiza la comprobación en la base de datos de clientes
        cliente = db.session.query(Cliente).filter_by(nombre=usuario, contraseña=contraseña).first()
        if cliente:
            # Usuario válido, guarda el cliente_id en la sesión
            session['cliente_id'] = cliente.id
            # Recuperar el ID del cliente de la sesión
            cliente_id = session.get('cliente_id')
            # Obtén la dirección del cliente desde la base de datos
            direccion_cliente = cliente.direccion
            # Usuario válido, redirige a la página del cliente pasando la direccion
            return redirect(url_for('pagina_cliente'))
        else:
            # Usuario inválido, muestra un mensaje de error o redirige a la página de registro de cliente
            # Usuario inválido, muestra un mensaje de error
            error = 'Usuario o contraseña incorrectos'
            return render_template('index.html', error=error)

    # Renderizar la página de inicio de sesión del cliente
    return render_template('pagina_cliente.html', tipo='cliente')


@app.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        # Obtén los datos del formulario de inicio de sesión
        usuario = request.form.get('usuario')
        contraseña = request.form.get('contraseña')

        # Realiza la comprobación en la base de datos de administradores
        admin = db.session.query(Admin).filter_by(nombre=usuario, contraseña=contraseña).first()
        print(admin)
        proveedores = db.session.query(Proveedor).all()
        productos = db.session.query(Producto).all()
        print(proveedores)
        if admin:
        # Usuario válido, redirige a la página del administrador
            print("Inicio de sesión exitoso como administrador")
            #return redirect(url_for('pagina_admin'))
            return render_template('pagina_admin.html', proveedores=proveedores, productos=productos)

        else:
        # Usuario inválido, muestra un mensaje de error
            error = 'Usuario o contraseña incorrectos'
            return render_template('index.html', error=error, tipo='admin')

        # Renderiza la página de inicio de sesión del administrador
    return render_template('pagina_admin.html', tipo='admin')


@app.route('/cliente')
def pagina_cliente():
    # Obtener todos los productos de base de datos
    productos = db.session.query(Producto).all()

    #imprimir productos en el terminar
    for producto in productos:
        print(producto)

    return render_template('pagina_cliente.html', producto=productos)


@app.route('/admin')
def pagina_admin():
    print("hola")
    # Obtener todos los productos de la base de datos
    productos = Producto.query.all()
    # Imprimir productos en el terminal
    for producto in productos:
        print(producto)
    return render_template('pagina_admin.html', productos=productos)


def obtener_proveedores():
    proveedores = Proveedor.query.all()
    return proveedores


@app.route('/agregar_proveedor', methods=['POST'])
def agregar_proveedor():
    if request.method == 'POST':
        nombre_proveedor = request.form['nuevo_proveedor_nombre']
        cif = request.form['nuevo_proveedor_cif']
        telefono = request.form['nuevo_proveedor_telefono']
        direccion = request.form['nuevo_proveedor_direccion']
        descuento = request.form['nuevo_proveedor_descuento']

        nuevo_proveedor = Proveedor(nombre_proveedor=nombre_proveedor, cif=cif, telefono=telefono, direccion_proveedor=direccion, descuentos=descuento)

        try:
            db.session.add(nuevo_proveedor)
            db.session.commit()
            return redirect(url_for('pagina_admin'))
        except:
            return 'Hubo un problema al agregar el proveedor'


@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        # Obtén los datos del formulario de agregar producto
        nombre_producto = request.form.get('nombre_producto')
        proveedor = request.form.get('proveedor')
        precio_compra = int(request.form.get('precio_compra'))
        precio_venta = int(request.form.get('precio_venta'))
        stock = int(request.form.get('stock'))
        stock_maximo = int(request.form.get('stock_maximo'))
        alerta_compra = request.form.get('alerta_compra')
        descripcion = request.form.get('descripcion')

        # Verificar si el proveedor ya existe en la base de datos
        proveedor_existente = Proveedor.query.filter_by(nombre=proveedor).first()

        if not proveedor_existente and proveedor != "Otro":
            # Si el proveedor no existe y no seleccionó "Otro", redirigir a la página de agregar producto con el proveedor seleccionado
            return redirect(url_for('agregar_producto'))

        if proveedor == "Otro":
            # Si el proveedor seleccionado es "Otro", obtener el nombre del nuevo proveedor del formulario
            nuevo_proveedor = request.form.get('otro_proveedor')
            if nuevo_proveedor:
                # Crear una nueva instancia de Proveedor y guardar en la base de datos
                proveedor_existente = Proveedor(nombre_proveedor=nuevo_proveedor)
                db.session.add(proveedor_existente)
                db.session.commit()
                proveedor = nuevo_proveedor  # Establecer el nombre del proveedor como el nuevo proveedor creado

        # Crear nueva instancia de Producto y guardar en la base de datos
        producto = Producto(nombre_producto=nombre_producto, proveedor=proveedor, precio_compra=precio_compra, precio_venta=precio_venta,
                            stock=stock, stock_Maximo=stock_maximo, alerta_Compra=alerta_compra, descripcion=descripcion)
        db.session.add(producto)
        db.session.commit()

        # Redirigir a la página_admin
        return redirect(url_for('pagina_admin'))

    # Obtener la lista de proveedores para mostrar en el formulario
    proveedores = Proveedor.query.all()

    # Renderizar el formulario para agregar producto
    return render_template('agregar_producto.html', proveedores=proveedores)

# Lista que representa el carrito de compras
carrito = []

@app.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    producto_id = request.form.get('producto_id')
    cantidad = int(request.form.get('cantidad'))

    if cantidad > 0:
        # Agregar el producto al carrito
        carrito.append({'producto_id': producto_id, 'cantidad': cantidad})

    return {'message': 'Producto agregado al carrito'}


@app.route('/registrar_compra', methods=['POST'])
def registrar_compra():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')  # Asegúrate de obtener el ID del cliente
        direccion_envio = request.form.get('direccion_envio')  # Asegúrate de obtener la dirección de envío
        total = request.form.get('total')  # Asegúrate de obtener el precio total

        # Formatear el carrito como una cadena JSON
        carrito_json = json.dumps(carrito)

        # Crear una nueva instancia de Compra y guardar en la base de datos
        compra = Compra(cliente_id=cliente_id, direccion_envio=direccion_envio, total=total, productos=carrito_json)
        db.session.add(compra)
        db.session.commit()

        # Limpiar el carrito después de completar la compra
        carrito.clear()

        # Redirigir a la página de inicio o a donde desees después de la compra
        return redirect(url_for('pagina_cliente'))

    # En caso de que no se haya realizado una solicitud POST
    return 'Método no permitido', 405


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine) #modelo de datos
    Cliente.__table__ = db.Base.metadata.tables['cliente']
    Admin.__table__ = db.Base.metadata.tables['administradores']
    Proveedor.__table__ = db.Base.metadata.tables['proveedor']
    Producto.__table__ = db.Base.metadata.tables['productos']
    app.run(debug=True)