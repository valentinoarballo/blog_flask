# Blog en Flask

Un miniblog hecho con Flask, SQL Alchemy y Bootstrap. Este proyecto es una implementación práctica desarrollada como parte de la asignatura de Práctica Profesionalisante. El objetivo principal es crear un sistema web que permita a los usuarios publicar y compartir contenido.

## Características  principales

1. Crear una publicación (Te pedirá crear una cuenta si no hay ninguna) (ojo que se ordenan cronológicamente).<br><br>
2. Crear tendencias o temas de charla con el uso de # antes del tema, por ejemplo, "tomando #mate" crea un tema "Mate" en tendencias. <br><br>
3. Comentar en una publicación. <br><br>
4. Borrar una publicación (Elimina los comentarios y, si es el último post hablando de cierto tema, el tema se borra de tendencias). <br><br>
5. Borrar comentarios. <br><br>
6. Registrarse como usuario (No permite emails repetidos, te pedirá que ingreses otro). <br><br>
7. Borrar un usuario, junto con sus publicaciones, los temas que haya creado y sus comentarios. <br><br>

## Problemas que me enfrenté haciendo el proyecto (y dudas)
1. Trabajé  con mi computadora de escritorio y mi notebook, cuando cambiaba de computadora y pulleaba el proyecto del repo remoto, la forma mas rapida que encontré para que funcionaran las migraciones era no subirlas directamente y hacer un flask db migrate , flask db upgrade sobre la base de datos vacía, seguro hay alguna forma mas rapida para trabajar con dos localhost diferentes. <br><br>
2. No creo haber estructurado correctamente el proyecto. Tengo todo el código, incluyendo las tablas de SQLAlchemy, las rutas, la configuración y el context processor, en un solo archivo app.py. También hay otras cuestiones como la secret key o la URI del servidor, que en este caso no importa que se suban a GitHub, pero en un proyecto real, supongo que deberían estar en un archivo aparte, al igual que otras partes del código. <br><br>
3. Leí por arriba la documentación de Login de Flask y me di cuenta que no lo iba a tener para el viernes si me ponia a hacer un login de verdad, asi que queda pendiente eso... de momento. <br><br>
## Set-Up
Primero, debes clonar el repositorio
```bash
  git clone git@github.com:valentinoarballo/blog_flask.git
```
<br><br>

Necesitarás tener XAMPP instalado en tu computadora. Debes activar los módulos de Apache y MySQL. Si estás en Linux, puedes abrir XAMPP con el siguiente comando:
```bash
  sudo /opt/lampp/./manager-linux-x64.run
```
<br>
<br>

También necesitarás una base de datos vacía en localhost con el nombre "project_blog".

<br>
<br>

Para ejecutar el proyecto, también es necesario tener Python 3.10.11 instalado. Debes crear un entorno virtual con el siguiente comando: 
```bash
  python3 -m venv venv
```
<br><br>

Luego, debes activarlo.<br>
En Linux:
```bash
  source venv/bin/activate
```
En Windows:
```bash
   dir venv/Scripts/activate
```
<br><br>

Una vez activado, debes instalar Flask, SQLAlchemy y otras bibliotecas con el siguiente comando: 
```bash
  pip install -r requirements.txt
```

<br><br>

Con la base de datos "project_blog" en localhost, el entorno virtual activado y XAMPP ejecutándose, debes ejecutar los siguientes comandos:
```bash
  flask db migrate -m "001_estructura_tablas"
  flask db upgrade
  flask run
```

<br><br>

Puedes ver el proyecto en funcionamiento en [localhost:5000](http://localhost:5000/)


## Autor
- [@Valentino Arballo](https://github.com/valentinoarballo)

