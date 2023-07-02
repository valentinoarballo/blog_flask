from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_migrate import Migrate
from datetime import datetime

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
    fecha_hora = db.Column(
        db.DateTime,
        default=datetime.now,
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
    publicacion = db.Column(
        db.Integer,
        db.ForeignKey('publicacion.id'),
        nullable=False
    )

    def __str__(self):
        return self.name

@app.context_processor 
def inject_posteos():
    publicaciones = db.session.query(Publicacion).all()
    return  dict(
        publicaciones=publicaciones  #esto va a estar disponible en todos los templates
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_publicacion', methods = ["POST"])
def nuevo_posteo():
    if request.method == "POST": 
        autor = request.form["autor"]    # llama al retorno del form autor 
        descripcion = request.form["descripcion"]
        nuevo_posteo = Publicacion(autor=autor, descripcion=descripcion)   # crea un post asignando nombre del autor y el post en si
        db.session.add(nuevo_posteo)              # agrega el cambio
        db.session.commit()                     # lo commitea
        return redirect(url_for("index"))       # recarga index, hace que todo se actualice de forma automatica

@app.route("/borrar_publicacion/<id>")
def borrar_publicacion(id):
    publicacion = Publicacion.query.get(id)   # busca el post que coinsida con el id de la url
    db.session.delete(publicacion)     # lo borra
    db.session.commit()         # lo commitea
    return redirect(url_for("index"))   


if __name__ == '__main__':
    app.run(debug=True)
