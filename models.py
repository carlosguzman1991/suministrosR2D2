import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
import datetime

class Cliente(db.Base):
    __tablename__ = "cliente"
    __table_args__= {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True) # Identificador único de cada cliente
    nombre = Column(String(200), nullable=False) # Nombre cliente, máximo 200 caracteres
    contraseña = Column(String(20), nullable=False) # Contraseña del cliente
    direccion = Column(String, nullable=False) # Direccion cliente


    def __init__(self, nombre, contraseña, direccion):
        self.nombre = nombre
        self.contraseña = contraseña
        self.direccion = direccion

    def __str__(self):
        return "{} {} {} {}".format(self.id, self.nombre, self.contraseña, self.direccion)

    @staticmethod
    def buscar_por_nombre(nombre):
        return db.session.query(Cliente).filter_by(nombre=nombre).first()

class Admin(db.Base):
    __tablename__ = "administradores"
    __table_args__= {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True) # Identificador único de cada administrador
    nombre = Column(String(200), nullable=False) # Nombre administrador, máximo 200 caracteres
    contraseña = Column(String(20), nullable=False) # Contraseña del administrador

    def __init__(self, nombre, contraseña):
        self.nombre = nombre
        self.contraseña = contraseña

    def __str__(self):
        return "{} {} {}".format(self.id, self.nombre, self.contraseña)

    @staticmethod
    def buscar_por_nombre(nombre):
        return db.session.query(Admin).filter_by(nombre=nombre).first()

class Proveedor(db.Base):
    __tablename__ = "proveedor"
    __table_args__ = {'sqlite_autoincrement': True}
    id_proveedor = Column(Integer, primary_key=True) # id del proveedor
    nombre_proveedor = Column(String, nullable=False) # nombre del proveedor
    direccion_proveedor = Column(String, nullable=False) # Direccion de empresa
    telefono = Column(Integer, nullable=False) # Telefono del proveedor
    cif = Column(String, nullable=False) # CIF de la empresa
    descuentos = Column(Integer, nullable=False) # Numero de porcentaje de descuento

    def __init__(self, nombre_proveedor, direccion_proveedor, telefono, cif, descuentos):
        self.nombre_proveedor = nombre_proveedor
        self.direccion_proveedor = direccion_proveedor
        self.telefono = telefono
        self.cif = cif
        self.descuentos = descuentos

    def __str__(self):
        return "{} {} {} {} {} {} ".format(self.id_proveedor,
                                           self.nombre_proveedor,
                                           self.direccion_proveedor,
                                           self.telefono,
                                           self.cif,
                                           self.descuentos)


class Producto(db.Base):
    __tablename__ = "productos"
    __table_args__ = {'sqlite_autoincrement': True}
    id_producto = Column(Integer, primary_key=True)  # Identificador único de cada producto
    nombre_producto = Column(String, nullable=False)  # Nombre producto
    proveedor = Column(String, ForeignKey('proveedor.nombre_proveedor'))  # Proveedor desde clase proveedor
    precio_compra = Column(Integer, nullable=False)  # Precio de compra del producto
    precio_venta = Column(Integer, nullable=False)  # Precio de venta al cliente
    stock = Column(Integer, nullable=False)  # stock de producto
    stock_Maximo = Column(Integer, nullable=False)  # stock maximo del producto
    alerta_Compra = Column(String)  # alerta stock inferior al 90%
    descripcion = Column(String, nullable=False)  # descripcion del producto
    imagen = Column(String)  # imagen del pruducto

    def __init__(self, nombre_producto, proveedor, precio_compra, precio_venta, stock, stock_Maximo, alerta_Compra,
                 descripcion, imagen):
        self.nombre_producto = nombre_producto
        self.proveedor = proveedor
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.stock = stock
        self.stock_Maximo = stock_Maximo
        self.alerta_Compra = alerta_Compra
        self.descripcion = descripcion
        self.imagen = imagen

    def __str__(self):
        return "{} {} {} {} {} {} {} {} {} {}".format(self.id_producto,
                                                   self.nombre_producto,
                                                   self.proveedor,
                                                   self.precio_compra,
                                                   self.precio_venta,
                                                   self.stock,
                                                   self.stock_Maximo,
                                                   self.alerta_Compra,
                                                   self.descripcion,
                                                   self.imagen)

class Compra(db.Base):
    __tablename__ = "compras"
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)  # Identificador único de cada compra
    cliente_id = Column(Integer, ForeignKey('cliente.id'))  # ID del cliente que realizó la compra
    fecha = Column(Integer, default=datetime.datetime.utcnow)  # Fecha de la compra
    direccion_envio = Column(String, ForeignKey('cliente.direccion'))  # Dirección de envío
    total = Column(Float, nullable=False)  # Precio total de la compra
    productos = Column(String, nullable=False)  # Lista de productos y cantidades en formato JSON

    def __init__(self, cliente_id, direccion_envio, total, productos):
        self.cliente_id = cliente_id
        self.direccion_envio = direccion_envio
        self.total = total
        self.productos = productos
