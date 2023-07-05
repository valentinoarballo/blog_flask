from flask import (Flask,
                    render_template,
                    redirect,
                    request,
                    url_for,
                    flash
                )
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_migrate import Migrate
from datetime import datetime
from random import *

app = Flask(__name__)
app.secret_key = 'clavesecreta123'
URI = 'mysql+pymysql://root:@localhost/project_blog'
app.config['SQLALCHEMY_DATABASE_URI'] = URI
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

    perfil = db.Column(
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

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id')
    )

    usuario = db.relationship(
        'Usuario',
        backref=db.backref('publicaciones', lazy=True)
    )

    def __str__(self):
        return self.name

class Tema(db.Model):
    __tablename__ = 'tema'

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

    perfil = db.Column(
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

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id'),
        nullable=False
    )

    usuario = db.relationship(
        'Usuario',
        backref=db.backref('comentarios', lazy=True)
    )
    

    def __str__(self):
        return self.name

class Usuario(db.Model):
    __tablename__ = 'usuario'

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

    perfil = db.Column(
        db.String(150),
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

    #publicaiones ordenadas por su fecha de forma decendiente
    publicaciones = (Publicacion.query
                    .order_by(Publicacion.fecha_hora.desc())
                    .all())
    
    comentarios = db.session.query(Comentario).all()
    temas = db.session.query(Tema).all()
    usuarios = db.session.query(Usuario).all()
    
    return  dict(
        publicaciones=publicaciones,  
        comentarios=comentarios,
        temas=temas,
        usuarios=usuarios
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


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# agregar publicacion
@app.route('/agregar_publicacion', methods = ["POST"])
def nuevo_posteo():

    # esta dentro de un try pq no se puede postear sin cuenta
    try:
        usuario_id = request.form["usuario_id"]
        descripcion = request.form["descripcion"]
        palabras = descripcion.split()


        usuario = Usuario.query.filter_by(id=usuario_id).first()
        autor = usuario.nombre
        perfil = usuario.perfil

        # expresión generadora para encontrar 
        # la primera palabra que comienza con '#'
        hashtag = next(
            (palabra for palabra in palabras if palabra.startswith('#')),
            None
        )

        #como hashtag puede ser none, corroboro que no lo sea para guardarlo
        tematica = hashtag[1:] if hashtag else None

        #busco en la db si existe, sino, lo creo
        tema = Tema.query.filter_by(nombre=tematica).first()
        if not tema:
            tema = Tema(nombre=tematica)
            flash('Tu publicacion esta en tendencias!')

        #creo el objeto
        nuevo_posteo = Publicacion(
            autor=autor,
            descripcion=descripcion,
            tema=tema,
            usuario_id=usuario_id,
            perfil=perfil
        )

        db.session.add(nuevo_posteo)
        db.session.commit()
        return redirect(url_for("index"))
    
    except:
        flash('Debes crearte una cuenta para poder publicar.')
        return redirect(url_for("login"))

# agregar usuario
@app.route('/agregar_usuario', methods = ["POST", "GET"])
def nuevo_usuario():

    # esta en un try pq no puede haber 2 usuarios con el mismo email
    try:
        nombre = request.form["nombre"] 
        email = request.form["email"]
        password = request.form["password"]
        numero_random = randint(1,17)
        perfil = f'gato{numero_random}.png'

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password=password,
            perfil=perfil
        
        )

        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Usuario creado.")    
        return redirect(url_for("index"))
    
    except:
        flash("Ya existe una cuenta con este email.")
        return redirect(url_for("login"))

# eliminar usuario
@app.route("/borrar_usuario", methods=["POST"])
def borrar_usuario():
    
    try: 
        usuario_id = request.form.get('usuario_id')
        usuario = Usuario.query.get(usuario_id)
        
        if usuario:
            publicaciones_relacionadas = Publicacion.query.filter_by(usuario_id=usuario_id).all()
            comentarios_relacionados = Comentario.query.filter_by(usuario_id=usuario_id).all()
            
            for comentario in comentarios_relacionados:
                db.session.delete(comentario)

            for publicacion in publicaciones_relacionadas:
                db.session.delete(publicacion)
            
            db.session.delete(usuario)
            db.session.commit()
            flash("Usuario eliminado.")
        else:
            flash("El usuario no fue encontrado")

    except:
        flash("Error al eliminar el usuario.")
        
    return redirect(url_for("index"))

# eliminar publicacion
@app.route("/borrar_publicacion/<id>")
def borrar_publicacion(id):

    publicacion = Publicacion.query.get(id)
    tema = publicacion.tema

    # comentarios filtrados por clave foranea = id del post que estoy borrando
    comentarios_asociados = (Comentario.query
                            .filter_by(id_publicacion=id)
                            .all()
                        )
    
    # borro todos los comentarios asociados a la publicacion
    for comentario_asociado in comentarios_asociados:
        db.session.delete(comentario_asociado)

    db.session.delete(publicacion)

    # si el post borrado era el ultimo qe hablaba de cierto tema, borro el tema
    if db.session.query(Publicacion).filter_by(tema_id=tema.id).count() == 0:
        db.session.delete(tema)

    flash('Publicacion eliminada.')
    db.session.commit()
    return redirect(url_for("index"))   

# agregar comentario 
@app.route('/agregar_comentario', methods = ["POST"])
def nuevo_comentario():

    # esta en un try pq no se puede comentar sin cuenta
    try:
        usuario_id = request.form["usuario_id"]
        descripcion = request.form["descripcion"]
        id_publicacion = request.form["id_publicacion"]

        usuario = Usuario.query.filter_by(id=usuario_id).first()
        autor = usuario.nombre
        perfil = usuario.perfil

        nuevo_comentario = Comentario(
            autor=autor,
            descripcion=descripcion,
            id_publicacion=id_publicacion,
            usuario_id=usuario_id,
            perfil=perfil
        )

        db.session.add(nuevo_comentario)
        db.session.commit()
        return redirect(url_for("index"))
    
    except:
        flash('Debes crearte una cuenta para poder comentar.')
        return redirect(url_for("login"))

@app.route("/borrar_comentario/<id>")
def borrar_comentario(id):

    comentario = Comentario.query.get(id)
    db.session.delete(comentario)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
