# 🚿 Hose

## Intent
Having a website where exchanging music with someone is easy and cool.
Users are linked by hoses (no pun intended).

## Getting started

This is a basic (and surely poorly done) Django project.
So, make sure to gather your favorite Python tools.
The database is in PostgreSQL, make sure you have one around.

### Prerequisities

**Hose** is a Python3.6 project.
You can handle your Python versions easily with [*pyenv*](https://github.com/pyenv/pyenv).

I chose to use the standard `pyproject.toml` to define the dependencies.
To use it, you get your hand on [*poetry*](https://github.com/sdispater/poetry).

### Installing

Once you're set, download or clone this repo and go in it.
Then, with *poetry*, you can simply do:
```
$ poetry install
```
Then, open a shell linked to poetry, 
that way we can use the different Django commands smoothly:
```
$ poetry shell
Spawning shell within <path>
$ cd hose
$ # Prepare the database 
$ python manage.py makemigrations
$ python manage.py migrate
$ # Spin a develop server
$ python manage.py runserver
```
After that last command, you should see:
`Starting development server at http://127.0.0.1:8000/`.
That means the development server is up ✅,
you can go for it in your browser or
start toying with the models in django-shell.

### Running the tests
🔧
Shame on me!

I'll add the tests when I'll have a clear view of the structure
of the project.
It'll probably be with *pytest*.

### Coding style

Shame!

### Deployment

I don't plan on making that website live yet.
I'll probably have huge legal problems with the materials people will pass around.

## Built with

* Python: https://python.org
* Django: https://djangoproject.com/
* Poetry: https://github.com/sdispater/poetry
* Bootstrap: https://getbootstrap.com/

## Contributing

🙉
It's kindof an educational project for me,
but feel free to give feedback 

## Authors

Gnonpy < le.gnonpi@gmail.com >

## License

Don't know yet
