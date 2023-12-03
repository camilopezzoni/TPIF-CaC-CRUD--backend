
from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root_22@localhost/catalogo_productos'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino la tabla
class Producto(db.Model):   # la clase Producto hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    foto=db.Column(db.String(400))
    tipo=db.Column(db.String(100))
    descripcion=db.Column(db.String(100))            
    precio=db.Column(db.Integer)
    recomendado=db.Column(db.Boolean)
    
    
    def __init__(self,nombre,foto,tipo,descripcion,precio,recomendado):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.foto=foto 
        self.tipo=tipo
        self.descripcion=descripcion
        self.precio=precio      
        self.recomendado=recomendado
        


with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','foto', 'tipo', 'descripcion', 'precio', 'recomendado')




producto_schema=ProductoSchema()            # El objeto producto_schema es para traer un producto
productos_schema=ProductoSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto




# crea los endpoint o rutas (json)
@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all()         # el metodo query.all() lo hereda de db.Model
    result=productos_schema.dump(all_productos)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla




@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)   # retorna el JSON de un producto recibido como parametro




@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)   # me devuelve un json con el registro eliminado


@app.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    foto=request.json['foto']
    tipo=request.json['tipo']
    descripcion=request.json['descripcion']
    precio=request.json['precio']
    recomendado=request.json['recomendado']
    
    new_producto=Producto(nombre,foto,tipo,descripcion,precio,recomendado)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto)


@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    producto=Producto.query.get(id)
    #'nombre','foto', 'tipo', 'descripcion', 'precio', 'recomendado', 'stock'
 
    nombre=request.json['nombre']
    foto=request.json['foto']
    tipo=request.json['tipo']
    descripcion=request.json['descripcion']
    precio=request.json['precio']
    recomendado=request.json['recomendado']
    

    producto.nombre=nombre
    producto.fot=foto
    producto.tipo=tipo
    producto.descripcion=descripcion
    producto.precio=precio
    producto.recomendado=recomendado
        

    db.session.commit()
    return producto_schema.jsonify(producto)
 


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000