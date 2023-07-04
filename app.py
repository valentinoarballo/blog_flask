from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clavesecreta123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/project_blog'
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
    tema_id = db.Column(
        db.Integer,
        db.ForeignKey('tema.id')
    )
    tema = db.relationship(
        'Tema',
        backref=db.backref('publicaciones', lazy=True)
    )
    
    def __str__(self):
        return self.name

class Tema(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    nombre = db.Column(
        db.String(50),
        unique=True
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
    descripcion = db.Column(
        db.String(100),
        nullable=False
    )
    id_publicacion = db.Column(
        db.Integer,
        db.ForeignKey('publicacion.id'),
        nullable=False
    )
    fecha_hora = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    def __str__(self):
        return self.name

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    nombre = db.Column(
        db.String(100),
        nullable=False
    )
    email = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.String(200),
        nullable=False
    )
    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )

    def __str__(self):
        return self.name

@app.context_processor 
def inject_posteos():
    publicaciones = Publicacion.query.order_by(Publicacion.fecha_hora.desc()).all()
    comentarios = db.session.query(Comentario).all()
    temas = db.session.query(Tema).all()
    return  dict(
        publicaciones=publicaciones,  #esto va a estar disponible en todos los templates
        comentarios=comentarios,
        temas=temas
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tendencias')
def tendencias():
    return render_template('tendencias.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# agregar publicacion
@app.route('/agregar_publicacion', methods = ["POST"])
def nuevo_posteo():
    if request.method == "POST": 
        autor = request.form["autor"] # llama al retorno del form autor 
        descripcion = request.form["descripcion"]
        palabras = descripcion.split()  # Divide la descripción en palabras
        hashtag = next((palabra for palabra in palabras if palabra.startswith('#')), None) # expresión generadora para encontrar la primera palabra que comienza con '#'
        tematica = hashtag[1:] if hashtag else None
        tema = Tema.query.filter_by(nombre=tematica).first()
        if not tema:
            tema = Tema(nombre=tematica)
            flash('Tu publicacion esta en tendencias!')
        nuevo_posteo = Publicacion(autor=autor, descripcion=descripcion, tema=tema) # crea un post asignando nombre del autor y el post en si
        db.session.add(nuevo_posteo) # agrega el cambio
        db.session.commit() # lo commitea
        return redirect(url_for("index"))

# agregar usuario
@app.route('/agregar_usuario', methods = ["POST"])
def nuevo_usuario():
    if request.method == "POST": 
        nombre = request.form["nombre"] # llama al retorno del form autor 
        email = request.form["email"]
        password = request.form["password"]
        nuevo_usuario = Usuario(nombre=nombre, email=email, password=password) # crea un post asignando nombre del autor y el post en si
        db.session.add(nuevo_usuario) # agrega el cambio
        db.session.commit() # lo commitea
        return redirect(url_for("index"))

# eliminar publicacion
@app.route("/borrar_publicacion/<id>")
def borrar_publicacion(id):
    publicacion = Publicacion.query.get(id) # busca el post que coinsida con el id de la url
    tema = publicacion.tema

    comentarios_asociados = Comentario.query.filter_by(id_publicacion=id).all() # tambien tengo q buscar los comentarios
    for comentario_asociado in comentarios_asociados:
        db.session.delete(comentario_asociado) # borro todos los comentarios de la publicacion

    db.session.delete(publicacion) # borra la publicacion

    if db.session.query(Publicacion).filter_by(tema_id=tema.id).count() == 0:
        db.session.delete(tema)

    flash('Publicacion eliminada.')

    db.session.commit() # commitea el cambio
    return redirect(url_for("index"))   

# agregar comentario 
@app.route('/agregar_comentario', methods = ["POST"])
def nuevo_comentario():
    if request.method == "POST": 
        autor = request.form["autor"]
        descripcion = request.form["descripcion"]
        id_publicacion = request.form["id_publicacion"] # recupera la id de la publicacion en la que se comento
        nuevo_comentario = Comentario(autor=autor, descripcion=descripcion, id_publicacion=id_publicacion) # crea un objeto comentario
        db.session.add(nuevo_comentario) # lo agrega
        db.session.commit() # lo commitea
        return redirect(url_for("index"))

@app.route("/borrar_comentario/<id>")
def borrar_comentario(id):
    comentario = Comentario.query.get(id) # busca el post que coinsida con el id de la url
    db.session.delete(comentario) # lo borra
    db.session.commit() # lo commitea
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
