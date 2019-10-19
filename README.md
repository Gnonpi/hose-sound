# 🚿 Hose

## Intent
Having a website where exchanging music with someone is easy and cool.
Users are linked by hoses (no pun intended).

## Getting started

This is a basic (and surely poorly done) Django project.
So, make sure to gather your favorite Python tools.
The database is in PostgreSQL, make sure you have one around.

### Prerequisities

#### Backend

**Hose** is a Python3.6 project.
You can handle your Python versions easily with [*pyenv*](https://github.com/pyenv/pyenv).

I chose to use the standard `pyproject.toml` to define the dependencies.
To use it, you get your hand on [*poetry*](https://github.com/sdispater/poetry).

#### Frontend

Frontend is really not my strong point.

I used [*Webpack*](https://webpack.js.org/)+[*VueJs*](https://vuejs.org/)+[*Bootstrap*](https://getbootstrap.com/).
* Webpack is used to build the project: 
it's really hard to configure but seems complete and there's lot of guides online
* VueJs is used to make the front intelligent:
it's easy to use, well documented and I like the component system.
* Bootstrap is used to give CSS components:
it's a crutch as I don't want to spend time on that and I have no skills in that.

I recommend using *nvm* to manipulate the NodeJs versions you install
and *yarn* to manipulate JS dependencies. 

### Installing

#### Backend

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

#### Frontend

Once you got yarn,
we can start going for the dev server:
```
$ cd hose/frontend
# Install dependencies from package.json
$ yarn install
$ yarn dev
 DONE  Compiled successfully in 11122ms
 I  Your application is running here: http://localhost:8080
```

### Running the tests
🔧
The coverage is really far from perfect

We use *pytest* and *pytest-django* for backend tests:
```
$ poetry shell
$ cd hose
$ pytest tests/
```

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
