from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# para poder crear nuestra app con flask
app = Flask(__name__)
# para poder acceder desde el front al backend
CORS(app)

# configuración de la bbdd
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/refugiaditos'
#
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# para poder crear la tabla de la bbdd
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Mascota(db.Model):
  # campos/col de la tabla mascota
  id = db.Column(db.Integer, primary_key = True)
  nombre = db.Column(db.String(20))
  tipo = db.Column(db.String(20))
  descripcion  = db.Column(db.String(150))
  imagen  = db.Column(db.String(400))

  def __init__(self, nombre, tipo, descripcion, imagen) -> None:
    self.nombre = nombre
    self.tipo = tipo
    self.descripcion = descripcion
    self.imagen = imagen

print(str(app.app_context()))
# Crear la tabla, si ya existe no la crea
with app.app_context():
  db.drop_all()
  db.create_all()
  mascotas_iniciales = [
    Mascota( nombre = 'Max', tipo = 'Perro', descripcion = 'Leal y protector, Max es el compañero perfecto para aventuras y abrazos.', imagen = 'https://images.pexels.com/photos/160846/french-bulldog-summer-smile-joy-160846.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'),
    Mascota( nombre = 'Roko', tipo = 'Perro', descripcion = 'Activo y atlético, Roko siempre está listo para jugar y explorar contigo.', imagen = 'https://images.pexels.com/photos/2253275/pexels-photo-2253275.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'),
    Mascota( nombre = 'Hércules', tipo = 'Gato',descripcion = 'Juguetón y cariñoso, Hércules ilumina tu hogar con su energía traviesa.', imagen = 'https://images.pexels.com/photos/1404819/pexels-photo-1404819.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'),
    Mascota( nombre = 'Mika', tipo = 'Perro', descripcion = 'Amigable y sociable, Mika se lleva bien con todos, humanos y peludos por igual.', imagen = 'https://images.pexels.com/photos/1404727/pexels-photo-1404727.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'),
    Mascota( nombre = 'Mochi', tipo = 'Gato', descripcion = 'Dulce y tranquila, Mochi te ofrece serenidad y afecto en cada rincón.', imagen = 'https://images.pexels.com/photos/104827/cat-pet-animal-domestic-104827.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'),
    Mascota( nombre = 'Simba', tipo = 'Perro', descripcion = 'Fiel y protector, aunque parece serio le encanta jugar y correr.', imagen ='https://images.pexels.com/photos/733416/pexels-photo-733416.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'),
    Mascota( nombre = 'Roma', tipo = 'Perro',descripcion = 'Divertido y obediente, Roma trae risas y lealtad a tu vida diaria.', imagen = 'https://images.pexels.com/photos/53261/pexels-photo-53261.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'),
    Mascota(nombre = 'Cleo', tipo =  'Gato', descripcion = 'Elegante y curiosa, Cleo añade un toque de gracia y misterio a tu vida.', imagen = 'https://images.pexels.com/photos/208773/pexels-photo-208773.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')
  ]

  db.session.bulk_save_objects(mascotas_iniciales)
  db.session.commit()


# defino los campos
class MascotaSchema(ma.Schema):
  class Meta:
    fields = ('id', 'nombre', 'tipo', 'descripcion', 'imagen')

# para almacenar una mascota
mascota_schema = MascotaSchema()
# para almacenar varios mascotas
mascotas_schema = MascotaSchema(many = True)

# -------- END POINTS --------
@app.route('/mascotas', methods = ['GET'])
def get_mascotas():
  all_mascotas = Mascota.query.all() # query.all() lo hereda de db.Model
  result = mascotas_schema.dump(all_mascotas) # dump() trae todos los registros de la tabla

  print("cantindad: ", Mascota.query.count())

  return jsonify(result) # convertir a json todos los registros

@app.route('/mascotas/<id>', methods = ['GET'])
def get_mascota(id):
  mascota = Mascota.query.get(id)

  return mascota_schema.jsonify(mascota) # convierte a json

@app.route('/mascotas/<id>', methods = ['DELETE'])
def delete_mascota(id):
  mascota = Mascota.query.get(id)
  db.session.delete(mascota)
  db.session.commit()
  return mascota_schema.jsonify(mascota) # para saber qué borré

@app.route('/mascotas', methods = ['POST'])
def create_mascota():

  cantidad_de_mascotas = Mascota.query.count()

  if (cantidad_de_mascotas < 30):
    nombre = request.json['nombre']
    tipo = request.json['tipo']
    descripcion = request.json['descripcion']
    imagen = request.json['imagen']

    new_mascota = Mascota(nombre, tipo, descripcion,imagen)

    db.session.add(new_mascota)
    db.session.commit()

    return mascota_schema.jsonify(new_mascota)
  else:
    return "BASE DE DATOS LLENA"

@app.route('/mascotas/<id>', methods = ['PUT'])
def update_mascota(id):
  mascota = Mascota.query.get(id)

  nombre = request.json['nombre']
  tipo = request.json['tipo']
  descripcion = request.json['descripcion']
  imagen = request.json['imagen']

  mascota.nombre = nombre
  mascota.tipo = tipo
  mascota.descripcion = descripcion
  mascota.imagen = imagen

  db.session.commit()

  return mascota_schema.jsonify(mascota)

# main
# if __name__ == '__main__':
#   app.run(debug=True, port=5000)

@app.route('/')
def hello_world():
    return 'Hello from flask'
