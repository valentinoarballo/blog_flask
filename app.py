from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/blog'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Publicacion(db.Model):
    __tablename__ = 'publicacion'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    autor = db.Column(
        db.String(100),
        nullable=False
    )
    descripcion = db.Column(
        db.String(100),
        nullable=False
    )
    
    def __str__(self):
        return self.name

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    autor = db.Column(
        db.String(100),
        nullable=False
    )
    pais = db.Column(
        db.Integer,
        db.ForeignKey('publicacion.id'),
        nullable=False
    )

    def __str__(self):
        return self.name

@app.context_processor 
def inject_paises():
    publicaciones = db.session.query(Publicacion).all()
    return  dict(
        paises=publicaciones  #esto va a estar disponible en todos los templates
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_pais', methods = ["POST"])
def nuevo_posteo():
    if request.method == "POST": 
        autor = request.form["nombre"]    # llama al retorno del form nombre 
        descripcion = request.form["descripcion"]
        nuevo_posteo = Publicacion(autor=autor, descripcion=descripcion)   # crea un pais asignandole el nombre que fue obtenido arriba
        db.session.add(nuevo_posteo)              # agrega el cambio
        db.session.commit()                     # lo commitea
        return redirect(url_for("index"))       # recarga index, hace que todo se actualice de forma automatica

@app.route("/borrar_pais/<id>")
def borrar_pais(id):
    pais = Publicacion.query.get(id)   # busca el pais que coinsida con el id de la url
    db.session.delete(pais)     # lo borra
    db.session.commit()         # lo commitea
    return redirect(url_for("index"))   


if __name__ == '__main__':
    app.run(debug=True)
