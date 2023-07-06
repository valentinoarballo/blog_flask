# Blog en Flask

Un miniblog hecho en flask, SQL Alchemy y Bootstrap

## Set-Up
Primero hay que clonar el repositorio
```bash
  git clone git@github.com:valentinoarballo/blog_flask.git
```

Vas a necesitar XAMPP descargado en tu computadora. Hay que activar los modulos Apache y MySQL. Si estas en linux puedes abrir LAMPP con el siguiente comando
```bash
  sudo /opt/lampp/./manager-linux-x64.run
```

Tambien vas a necesitar una base de datos vacia en el localhost con el nombre de "project_blog"
<br>

Para ejecutar el proyecto tambien es necesario tener Python 3.10.11 instalado. Hay que crear un entorno virtual, con el siguiente comando. 
```bash
  python3 -m venv venv
```

Ademas, hay que activarlo.
En linux
```bash
  source venv/bin/activate
```
En Windows
```bash
   dir venv/Scripts/activate
```

Una vez activado, hay que instalar Flask, SQL Alchemy y otras librerias, con el siguiente comando. 

```bash
  pip install -r requirements.txt
```

Con la base de datos "project_blog" en localhost, el entorno virtual y XAMPP activado, hay que ejecutar los siguientes comandos
```bash
  flask db migrate "001_estructura_tablas"
  flask db upgrade
  flask run
```
and access it through typing [localhost:5000](http://localhost:5000/) in your browser


## Authors
- [@Valentino Arballo](https://github.com/valentinoarballo)

