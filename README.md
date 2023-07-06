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

To deploy this project you will need an updated version of Python. First, we will create a virtual enviroment.
```bash
  python3 -m venv venv
```

Now, we need to activate the virtual enviroment.
On linux
```bash
  source venv/bin/activate
```
on Windows,
```bash
   dir venv/Scripts/activate
```
Once activated, we need to install Flask, SQL Arlchemy and other libraries:

```bash
  pip install -r requirements.txt
```

Con el entorno virtual activado, XAMPP activado y la base de datos "project_blog" en localhost, hay que ejecutar los siguientes comandos
```bash
  flask db migrate "001_estructura_tablas"
  flask db upgrade
  flask run
```
and access it through typing [localhost:5000](http://localhost:5000/) in your browser


## Authors

- [@Nazareno Bucciarelli](https://github.com/nazabucciarelliITEC)
- [@Luca Petrocchi](https://github.com/LucaPetrocchi)
- [@Facundo Lemo](https://github.com/FacundoEsteban-Lemo)
- [@Valentino Arballo](https://github.com/valentinoarballo)

