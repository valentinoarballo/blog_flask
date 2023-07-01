from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/alchemy'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Pais(db.Model):
    __tablename__ = 'pais'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    nombre = db.Column(
        db.String(100),
        nullable=False
    )
    
    def __str__(self):
        return self.name

class Provincia(db.Model):
    __tablename__ = 'provincia'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    nombre = db.Column(
        db.String(100),
        nullable=False
    )
    pais = db.Column(
        db.Integer,
        db.ForeignKey('pais.id'),
        nullable=False
    )

    def __str__(self):
        return self.name

class Localidad(db.Model):
    __tablename__ = 'localidad'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    nombre = db.Column(
        db.String(100),
        nullable=False
    )
    provincia = db.Column(
        db.Integer,
        db.ForeignKey('provincia.id'),
        nullable=False
    )

    def __str__(self):
        return self.name

class Persona(db.Model):
    __tablename__ = 'persona'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    nombre = db.Column(
        db.String(100),
        nullable=False
    )
    apellido = db.Column(
        db.String(100),
        nullable=False
    )
    email = db.Column(
        db.String(100),
        nullable=True
    )
    telefono = db.Column(
        db.Integer,
        nullable=True
    )
    domicilio = db.Column(
        db.String(100),
        nullable=False
    )
    fech_naci = db.Column(
        db.Date,
        nullable=False
    )
    activo = db.Column(
        db.Boolean,
        nullable=False
    )
    localidad = db.Column(
        db.Integer,
        db.ForeignKey('localidad.id'),
        nullable = False
    )

    def __str__(self):
        return self.name

@app.context_processor 
def inject_paises():
    paises = db.session.query(Pais).all()
    return  dict(
        paises=paises  #esto va a estar disponible en todos los templates
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_pais', methods = ["POST"])
def nuevo_pais():
    if request.method == "POST": 
        nombre_pais = request.form["nombre"]    # llama al retorno del form nombre 
        nuevo_pais = Pais(nombre=nombre_pais)   # crea un pais asignandole el nombre que fue obtenido arriba
        db.session.add(nuevo_pais)              # agrega el cambio
        db.session.commit()                     # lo commitea
        return redirect(url_for("index"))       # recarga index, hace que todo se actualice de forma automatica

@app.route("/borrar_pais/<id>")
def borrar_pais(id):
    pais = Pais.query.get(id)   # busca el pais que coinsida con el id de la url
    db.session.delete(pais)     # lo borra
    db.session.commit()         # lo commitea
    return redirect(url_for("index"))   


if __name__ == '__main__':
    app.run(debug=True)
