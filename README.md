# Blog en Flask

Un miniblog hecho con Flask, SQL Alchemy y Bootstrap. Este proyecto es una implementación práctica desarrollada como parte de la asignatura de Práctica Profesionalisante. El objetivo principal es crear un sistema web que permita a los usuarios publicar y compartir contenido.

## Caracteristicas principales

1. Crear una publicacion (Te pide crear una cuenta si no hay ninguna) (ojo que se ordenan cronologicamente) <br><br>
2. Crear tendencias o temas de charla con el uso de #, antes de el tema, por ej. "tomando #mate" crea un tema "Mate" en tendencias <br><br>
3. Comentar en una publicacion <br><br>
4. Borrar una publicacion (Elimina los comentarios, y si es el ultimo post hablando de cierto tema, el tema se borra de tendencias) <br><br>
5. Borrar comentarios <br><br>
6. Registrarse como usuario (No permite Emails repetidos, te va a pedir que ingreses otro) <br><br>
7. Borrar un usuario, junto a sus publicaciones, los temas que haya creado y sus comentarios <br><br>


## Set-Up
Primero hay que clonar el repositorio
```bash
  git clone git@github.com:valentinoarballo/blog_flask.git
```
<br><br>

Vas a necesitar XAMPP descargado en tu computadora. Hay que activar los modulos Apache y MySQL. Si estas en linux puedes abrir LAMPP con el siguiente comando
```bash
  sudo /opt/lampp/./manager-linux-x64.run
```
<br>
<br>

Tambien vas a necesitar una base de datos vacia en el localhost con el nombre de "project_blog"

<br>
<br>

Para ejecutar el proyecto tambien es necesario tener Python 3.10.11 instalado. Hay que crear un entorno virtual, con el siguiente comando. 
```bash
  python3 -m venv venv
```
<br><br>

Ademas, hay que activarlo.<br>
En linux
```bash
  source venv/bin/activate
```
En Windows
```bash
   dir venv/Scripts/activate
```
<br><br>

Una vez activado, hay que instalar Flask, SQL Alchemy y otras librerias, con el siguiente comando. 
```bash
  pip install -r requirements.txt
```

<br><br>

Con la base de datos "project_blog" en localhost, el entorno virtual y XAMPP activado, hay que ejecutar los siguientes comandos
```bash
  flask db migrate "001_estructura_tablas"
  flask db upgrade
  flask run
```

<br><br>

Puedes ver el proyecto corriendo en [localhost:5000](http://localhost:5000/)


## Autor
- [@Valentino Arballo](https://github.com/valentinoarballo)

