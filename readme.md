# Curso básico de Django

## Introducción

### ¿Qué es Django?

Uno de los frameworks más populares para crear web apps. Es gratis y Open Source.

Instagram, Pinterest, National Geographic y Platzi usan Django.

[Django](https://www.djangoproject.com/) es rápido, seguro y escalable.

### Instalación de Django

Primero, [creamos nuestro entorno virtual](https://github.com/Mike-droid/CursoPythonIntermedio#el-primer-paso-profesional-creaci%C3%B3n-de-un-entorno-virtual).

Y ya dentro hacemos `pip install django`.

Finalmente, iniciamos el proyecto con `django-admin startproject 'nombre_del_proyecto'`.

### Explorando los archivos que creó Django

- __init__.py indica que es un paquete
- asgi.py y wsgi.py son archivos que sirven para el despliegue a producción del proyecto
- settings.py son configuraciones como BD, zona horaria, lenguaje, etc.
- urls.py es el archivo que tiene las rutas del proyecto.

### El servidor de desarrollo

Entramos a la carpeta del proyecto y hacemos `py manage.py runserver` para iniciar el servidor de Django.

### Nuestro primer proyecto: Premios Platzi App

Un __proyecto__ en Django, es un __conjunto de aplicaciones__.

Ejemplo: Instagram es un proyecto de Django, que tiene varias aplicaciones, como:

- Feed (donde se cargan las fotos)
- Stories
- Messages
- Etc

### Nuestro primer proyecto: Premios Platzi App 2

Para crear aplicaciones en Django hacemos `py manage.py startapp 'nombre_de_la_app'`.

En el archivo principal de urls.py podemos indicar qué rutas tendrá nuestro proyecto.

Además, podemos crear apps que tendrán más archivos urls.py para manejar las rutas de cada respectiva app y que trabajen dentro del mismo proyecto.

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls'))
]

```

Ese es el urls.py principal y en el de una app particular, podemos tener, por ejemplo:

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index")
]

```

### Ajustando el archivo settings.py

Por defecto, Django solo admite bases de datos relacionales.

[Documentación de Settings](https://docs.djangoproject.com/en/4.0/ref/settings/)

[List of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Models

### ¿Qué es ORM? ¿Qué es un modelo?

ORM -> Object Relational Mapping

Se trata de relacionar una RBD (Base de datos relacional) con la POO.

Cada archivo de Python será un 'modelo' (que representa una tabla de las BBDD) y se crea con clases.

Cada atributo de la clase, es la representación de las columnas.

Y los tipos de datos de las columnas, serán las clases dentro de los atributos.

### Creando un diagrama entidad-relación para nuestro proyecto

| questions                |
| ------------------------ |
| id -> int                |
| question_text -> varchar |
| pub_date -> datetime     |

relación uno a muchos con

| choices                |
| ---------------------- |
| id -> int              |
| question -> int        |
| choice_text -> varchar |
| votes -> int           |

### Creando los modelos Question y Choice

Comandos de la clase:

- `py manage.py makemigrations 'nombre_de_la_app'` -> Django describe toda la creación de las tablas de las BBDD.
- `py manage.py migrate` -> Django toma el archivo creado con el comando anterior y lo ejecuta en la BBDD.

## Interactive Shell

### La consola interactiva de Django

Ingresamos a la shell de Django con `py mange.py shell`

Y desde aquí trabajamos como lo haríamos normalmente en Python teniendo acceso a los módulos y paquetes de nuestro proyecto.

```python
(InteractiveConsole)
>>> from polls.models import Choice, Question
>>> Question.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> q = Question(question_text='¿Cuál es el mejor curso de Platzi?', pub_date=timezone.now())
>>> q.save()
```

### El método \_\_str\_\_

Agregamos el método de `def __str__` a ambas clases y podemos obtener mejor información en la shell.

```python
>>> from polls.models import Question, Choice
>>> Question.objects.all()
<QuerySet [<Question: ¿Cuál es el mejor curso de Platzi?>]>
>>>
```

### Filtrando los objetos creados desde la consola interactiva

_protip_: Para limpiar la terminal en Python desde Windows, escribe:

```python
>>> import os
>>> os.system('cls')
```

__protip__: Usando `__` en los atributos, Django nos permite hacer búsquedas más complejas sobre los datos.

```python
>>> Question.objects.get(pub_date__year=timezone.now().year)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "C:\Users\migue\Desktop\Desktop_files\CURSOS\platzi\curso_basico_django\venv\lib\site-packages\django\db\models\manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "C:\Users\migue\Desktop\Desktop_files\CURSOS\platzi\curso_basico_django\venv\lib\site-packages\django\db\models\query.py", line 499, in get
    raise self.model.MultipleObjectsReturned(
polls.models.Question.MultipleObjectsReturned: get() returned more than one Question -- it returned 3!
```

### El método filter

```python
>>> Question.objects.filter(pk=1)
<QuerySet [<Question: ¿Cuál es el mejor curso de Platzi?>]>
>>> Question.objects.filter(pk=2)
<QuerySet [<Question: ¿Quién es el mejor profesor de Platzi?>]>
>>> Question.objects.filter(pk=4)
<QuerySet []>
>>> Question.objects.filter(question_text__startswith='¿Cuál')
<QuerySet [<Question: ¿Cuál es el mejor curso de Platzi?>, <Question: ¿Cuál es la mejor escuela de Platzi?>]>
>>> Question.objects.filter(pub_date__year=timezone.now().year)
<QuerySet [<Question: ¿Cuál es el mejor curso de Platzi?>, <Question: ¿Quién es el mejor profesor de Platzi?>, <Question: ¿Cuál es la mejor
escuela de Platzi?>]>
>>>
```

### Accediendo al conjunto de respuestas

```python
>>> q = Question.objects.get(pk=1)
>>> q
<Question: ¿Cuál es el mejor curso de Platzi?>
>>> q.choice_set.all()
<QuerySet []>
>>> q.choice_set.create(choice_text="Curso Básico de Python", votes=0)
<Choice: Curso Básico de Python>
>>> q.choice_set.create(choice_text="Curso de Fundamentos de Ingeniería de Software", votes=0)
<Choice: Curso de Fundamentos de Ingeniería de Software>
>>> q.choice_set.create(choice_text="Curso de Elixir", votes=0)
<Choice: Curso de Elixir>
>>> q.choice_set.all()
<QuerySet [<Choice: Curso Básico de Python>, <Choice: Curso de Fundamentos de Ingeniería de Software>, <Choice: Curso de Elixir>]>
>>> q.choice_set.count()
3
>>> Choice.objects.filter(question__pub_date__year=timezone.now().year)
<QuerySet [<Choice: Curso Básico de Python>, <Choice: Curso de Fundamentos de Ingeniería de Software>, <Choice: Curso de Elixir>]>
>>>
```

## Django Admin

### El administrador de Django

__Comando súper peligroso__: `py manage.py createsuperuser`

¿Por qué es peligroso? Porque crearemos un usuario que tenga todo el control de la base de datos y este usuario solamente debe ser usado por el administrador de la BBDD.

Cuando asignamos un nombre de usuario, correo y contraseña, haremos lo siguiente:

Debemos entrar al archivo admin.py de nuestras apps y hacer que los modelos sean disponibles para la ruta localhost:8000/admin.

## Views

### ¿Qué son las views o vistas?

Django usa el modelo MTV -> Model Template View.

Django es un fullstack framework. En el backend tenemos las views y en el frontend las templates.

Una vista tiene:

- Función -> Function Based Views
- Clase -> Generic Views

### Creando vistas para la aplicación

Creamos las vistas en views.py:

```python
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("You are in the index page from Premios Platzi App")


def detail(request, question_id):
    return HttpResponse(f'You are watching the question # {question_id}')


def results(request, question_id):
    return HttpResponse(f'You are watching the results from the question # {question_id}')


def vote(request, question_id):
    return HttpResponse(f'You are voting to the question # {question_id}')

```

Y las importamos en el archivo urls.py:

```python
from django.urls import path

from . import views

urlpatterns = [
    # * ex: /polls/
    path('', views.index, name="index"),
    # * ex: /polls/3
    path('<int:question_id>/', views.detail, name="detail"),
    # * ex: /polls/3/results
    path('<int:question_id>/results/', views.results, name="results"),
    # * ex: /polls/3/vote
    path('<int:question_id>/vote/', views.vote, name="vote"),
]

```

### Templates en Django

Hacemos una configuración en settings.json para que VS Code use emmet en los templates de Django:

```json
"emmet.includeLanguages":{
    "django-html": "html"
}
```

### Creando el template del home

Conectamos a los templates con las views:

index.html:

```python
{% if latest_question_list %}
<ul>
  {% for question in latest_question_list %}
  <li><a href="/polls/{{ question.id }}">{{ question.question_text }}</a></li>
  {% endfor %}
</ul>
{% else %}
<p>No polls are available.</p>
{% endif %}
```

views.py:

```python
from django.shortcuts import render
from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.all()
    return render(request, "polls/index.html", {
        # * La variable ahora está disponible en index.html
        "latest_question_list": latest_question_list
    })
```

### Elevando el error 404

Django tiene un shortcut que es `get_object_or_404` justamente para este tipo de casos.

### Utilizando la etiqueta url para evitar el hard coding

Conectamos urls.py con los templates:

```python
from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    # * ex: /polls/
    path('', views.index, name="index"),
    # * ex: /polls/3
    path('<int:question_id>/', views.detail, name="detail"),
    # * ex: /polls/3/results
    path('<int:question_id>/results/', views.results, name="results"),
    # * ex: /polls/3/vote
    path('<int:question_id>/vote/', views.vote, name="vote"),
]

```

```python
{% if latest_question_list %}
<ul>
  {% for question in latest_question_list %}
  <li>
    <a href="{% url 'polls:detail' question.id %}"
      >{{ question.question_text }}</a
    >
    {% comment %} polls sale del app_name y detail sale del name de la vista en
    urls.py {% endcomment %}
  </li>
  {% endfor %}
</ul>
{% else %}
<p>No polls are available.</p>
{% endif %}

```

## Forms

### Formularios: lo básico

__pro tip__: SIEMPRE usa `{% csrf_token %}` en los formularios POST para evitar ataques de hacking.

### Creando la vista vote

Es buena práctica hacer redirect después de que el usuario usó un formulario

### Creando la vista results

Para que pluralize funcione, no debe de haber espacios:

```python
<h1>{{ question.question_text }}</h1>
<ul>
  {% for choice in question.choice_set.all %}
  <li>
    {{ choice.choice_tex }} -- {{ choice.votes }} vote{{choice.votes|pluralize}}
  </li>
  {% endfor %}
</ul>
<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```

## Generic Views

### Clase Generic Views

Las Generic views son funciones basadas en clases (POO).

[Classy Class-Based Views](http://ccbv.co.uk/)

### Implementado generic views en la aplicación

¿Cuándo usar Generic y Function views?

Si sigues el modelo de la BBDD, usa Generic Views. Si haces algo más complejo, usa Function-based views.

> Si se puede, Generic, si no se puede, Function.

## Examen

- ¿Cuál de los siguientes métodos devuelve un registro que cumpla una condición de una tabla?: `model.objects.if` 💢
- ¿Qué es una view o vista?: Una página web pública de nuestro proyecto
- Cuando se tiene una vista con una funcionalidad común en el desarrollo web, debería usar: Generic Views
- ¿Cuál de los siguientes comandos, para iniciar la consola interactiva de Django, está escrito correctamente?: `python manage.py shell`
- ¿Qué es Django?: Un framework de desarrollo web con Python, gratis y open source
- ¿Cuál de los siguientes métodos devuelve todos los registros de una tabla?: `model.objects.all`
- ¿Cuál de los siguientes comandos para crear un proyecto en Django está escrito correctamente?: `django-admin startproject premiosplatziapp`
- ¿Qué es un proyecto en Django?: Un conjunto de aplicaciones independientes
- ¿Qué contiene el archivo manage.py?: El código que hace que el comando django-admin funcione, y permite también ejecutar comandos específicos sobre el proyecto
- ¿Qué contiene el archivo asgi.py?: El código necesariopara conectar nuestro proyecto con un servidor, una vez que hagamos deploy del mismo
- ¿Cuál de los siguientes comandos, para crear una aplicación en Django, está escrito correctamente?: `python manage.py startapp polls`
- ¿Cuál de los siguientes comandos, para inicializar un super usuario en el administrador de Django, está escrito correctamente?: `python manage.py createsuperuser`
- ¿Qué es ORM (Object Relational Mapping)?: Es una técnica que utilizan ciertas librerías y frameworks, como Django, para replicar con POO, la estructura de una BBDD.
- ¿A qué equivale una columna de una tabla de una base de datos relacional (en programación orientada a objetos) con el ORM de Django?: atributo
- ¿Qué es el administrador de Django?: Una interfaz web, ya construida, que permite ver, crear, modificar y eliminar los diferentes registros de cada uno de los modelos que hayamos definido en nuestro proyecto.
- Al administrador de datos...: Podemos usarlo desde el principio, ya que viene preinstalado en Django
- ¿Cuál de los siguientes métodos devuelve un conjunto de registros que cumplan una condición de una tabla?: `models.objects.filter`
- ¿Cuál de los siguientes es un motor de base de datos soportado nativamente por Django?: Todas
- ¿Cuál de las siguientes es una característica de Django?: Todas
- ¿Para qué sirve la consola interactiva de Django?: Nos permite ejecutar comandos especiales que la consola de Python no 💢
- ¿Qué contiene el archivo urls.py?: Las direcciones web a las que se puede acceder en nuestro proyecto
- Una aplicación es un conjunto de proyectos independientes: falso
- Una vista es responsable de una de dos cosas: ambas
- ¿A qué equivale una tabla de una base de datos relacional (en programación orientada a objetos) con el ORM de Django?: A un modelo (clase)
- ¿Cuál de las siguientes empresas utiliza Django en su backend?: Instagram
- Las migrations son archivos históricos de todas las actualizaciones que hicimos sobre nuestros modelos, que Django utiliza para replicar en la base de datos, las clases que nosotros creamos: verdadero
- ¿Cuál de los siguientes archivos no es creado automáticamente por Django?: urls.py 💢
- Django está en el top 3 de frameworks de desarrollo web con Python: Verdadero
- ¿Cuál de las siguientes es una variable inexistente en el archivo settings.py?: APP_CONTAINER
- ¿Cuál de los siguientes comandos, para iniciar el servidor de desarrollo en Django, está escrito correctamente?: `py manage.py runserver`

## Django nivel intermedio

## Testing

### ¿Qué son los tests?

Los tests son funciones que verifican que tu código funcione correctamente. Con esto puedes evitar errores futuros.

¿Qué ventajas tiene?

1. Nos damos cuenta de errores que a simple vista no hubieramos visto.
2. Nos hace más profesionales.
3. Nos permite trabajar mejor en equipo.

TDD -> Test Driven Development. Antes de escribir el código, tienes que escribir el test.

### Escribiendo nuestro primer test

Analicemos que, una de nuestras funciones del proyecto regresa preguntas recientes, pero si creamos preguntas que son hechas en el futuro, se toman como recientes y esto no debe ser así.

```python
>>> import datetime
>>> from django.utils import timezone
>>> from polls.models import Question
>>> q = Question(question_text='¿Quién es el mejor Course Director de Platzi?', pub_date=timezone.now() + datetime.timedelta(days=30))
>>> timezone.now() + datetime.timedelta(days=30)
datetime.datetime(2022, 7, 28, 2, 42, 20, 144852, tzinfo=datetime.timezone.utc)
>>> q.was_published_recently()
True
>>>
```

Lo más común es hacer tests sobre modelos y/o vistas en Django.

Test creado:

```python
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# * Lo más común es hacer tests sobre modelos y/o vistas en Django


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(
            question_text="¿Quién es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

```

Resultado:

```python
(venv) λ py manage.py test polls
Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
F
======================================================================
FAIL: test_was_published_recently_with_future_questions (polls.tests.QuestionModelTests)
was_published_recently returns False for questions whose pub_date is in the future
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\migue\Desktop\Desktop_files\CURSOS\platzi\curso_basico_django\premiosplatziapp\polls\tests.py", line 18, in test_was_publis
hed_recently_with_future_questions
    self.assertIs(future_question.was_published_recently(), False)
AssertionError: True is not False

----------------------------------------------------------------------
Ran 1 test in 0.002s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

La prueba falló pero es lo que queríamos.

Modificamos el código de models.py:

```python
def was_published_recently(self):
  return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
  # * 1 día de antigüedad
```

Resultado:

```python
(venv) λ py manage.py test polls
Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
Destroying test database for alias 'default'...
```

__Pasos a seguir para los tests__:

1. Identificamos un problema
2. Creamos un test.
3. Corremos el test.
4. Arreglamos el problema.
5. Corremos el test.

Test para preguntas pasadas, presentes y futuras:

```python
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# * Lo más común es hacer tests sobre modelos y/o vistas en Django


class QuestionModelTests(TestCase):
    def setUp(self):
        self.question = Question(
            question_text='¿Quién es el mejor Course Director de Platzi?')
        self.future_time = timezone.now() + datetime.timedelta(days=30)
        self.past_time = timezone.now() - datetime.timedelta(days=30)
        self.recent_time = timezone.now()

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        self.question.pub_date = self.future_time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns True for questions whose pub_date is in the past"""
        self.question.pub_date = self.past_time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_recent_questions(self):
        """was_published_recently returns True for questions whose pub_date is today"""
        self.question.pub_date = self.recent_time
        self.assertIs(self.question.was_published_recently(), True)

```

Resultado:

```python
(venv) λ py manage.py test polls
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 0.003s

OK
Destroying test database for alias 'default'...
```

### Testing de Views

Hacemos una modificación en el index de polls en el archivo views.py. Esto lo hacemos porque aunque creamos una pregunta con tiempo en el futuro,la vista regresa esa pregunta, cosa que no debe de pasar.

```python
def get_queryset(self):
  "Return the last five published questions"
  return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
```

Creamos un nuevo test para la vista en tests.py:

```python
class QuestionIndexViewTests(TestCase):
  def test_no_questions(self):
    """If no question exist, an appropiate message is displayed"""
    # * Hago una petición GET al index de polls y guardo la respuesta en response
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context['latest_question_list'], [])
```

### Creando más tests para IndexView

Mejorando los tests:

```python
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# * Lo más común es hacer tests sobre modelos y/o vistas en Django


class QuestionModelTests(TestCase):
    def setUp(self):
        self.question = Question(
            question_text='¿Quién es el mejor Course Director de Platzi?')
        self.future_time = timezone.now() + datetime.timedelta(days=30)
        self.past_time = timezone.now() - datetime.timedelta(days=30)
        self.recent_time = timezone.now()

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        self.question.pub_date = self.future_time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns True for questions whose pub_date is in the past"""
        self.question.pub_date = self.past_time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_recent_questions(self):
        """was_published_recently returns True for questions whose pub_date is today"""
        self.question.pub_date = self.recent_time
        self.assertIs(self.question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with que given "question_text", and published the given numbers of days offset to now (negative for questions in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(QuestionModelTests, TestCase):
    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        # * Hago una petición GET al index de polls y guardo la respuesta en response
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_show_only_recent_questions(self):
        """The view should only show recent questions. It cannot show future questions from the date they are consulted."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        future_question = [self.question, self.future_time]
        self.assertNotContains(response, future_question)

    def test_future_questions(self):
        """
        Questions with a pub_date in the future aren't displayed on the index page.
        """
        create_question('Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        """
        Questions with a pub_date in the past are displayed on the index page.
        """
        question = create_question('Past question', days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [question])

```

### Ajustando detalles en los tests para IndexView

Nuevos tests:

```python
def test_future_question_and_past_question(self):
        """
        Even if both past and future exist, only past questions are displayed.
        """
        past_question = create_question(
            question_text='Past question', days=-30)
        future_question = create_question(
            question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [past_question])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        past_question1 = create_question(
            question_text='Past question 1', days=-30)
        past_question2 = create_question(
            question_text='past question 2', days=-40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [past_question1, past_question2])

    def test_two_future_questions(self):
        """
        This questions won't be displayed on the index page.
        """
        future_question1 = create_question(
            question_text='Future question 1', days=30)
        future_question2 = create_question(
            question_text='Future question 2', days=40)
        response = self.client.get(reverse('polls:index'))
        self.assertNotContains(response, [future_question1, future_question2])
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
```

### Creando tests para DetailView

Creamos el nuevo test:

```python
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 error not found.
        """
        future_question = create_question(
            question_text='Future question', days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past displays the question´s text.
        """
        past_question = create_question(
            question_text='Past question', days=-30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
```

Ajutamos la clase de DetailView:

```python
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that are not published yet
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
```

Consejos a la hora de usar tests:

1. Más tests es mejor, aunque parezca lo contrario.
2. Crea una clase para cada modelo o vista testeada.
3. Establece nombres de métodos de test lo más descriptivos posibles.

## Static Files

### Agregando estilos a nuestro proyecto

Creamos un archivo CSS en 'polls/static/polls.css':

```css
li a {
  color: green;
}
```

Y lo usamos en index.html:

```python
{% load static %}
<link rel="stylesheet" href="{% static 'polls/style.css' %}" />
```

### Añadiendo una imagen de fondo

styles.css:

```css
body {
  background: #4b6cb7;
  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #182848, #4b6cb7);
  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #182848, #4b6cb7);
  /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
  font-family: Arial, Helvetica, sans-serif;
}

.color-change-2x:hover {
  -webkit-animation: color-change-2x 2s linear infinite alternate both;
  animation: color-change-2x 2s linear infinite alternate both
}

@-webkit-keyframes color-change-2x {
  0% {
    background: #19dcea
  }

  100% {
    background: #b22cff
  }
}

@keyframes color-change-2x {
  0% {
    background: #19dcea
  }

  100% {
    background: #b22cff
  }
}

li {
  -webkit-backdrop-filter: blur(8.5px);
  backdrop-filter: blur(8.5px);
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  list-style: none;
  margin: 30px 0;
  padding: 5px;
  width: fit-content;
}

li:hover {
  cursor: pointer;
}

li a {
  color: #ffffff;
  font-size: 2em;
  text-decoration: none;
}
```

index.html:

```python
{% load static %}
<link rel="stylesheet" href="{% static 'polls/style.css' %}" />

{% if latest_question_list %}
<ul>
  {% for question in latest_question_list %}
  <li class="color-change-2x">
    <a href="{% url 'polls:detail' question.id %}"
      >{{ question.question_text }}</a
    >
    {% comment %} polls sale del app_name y detail sale del name de la vista en
    urls.py {% endcomment %}
  </li>
  {% endfor %}
</ul>
{% else %}
<p>No polls are available.</p>
{% endif %}

```

Páginas web que utilicé:

- [Glassmorphism CSS Generator](hype4.academy)
- [uiGradients](uigradients.com)
- [Animista - CSS Animations on Demand](animista.net)

## Django Admin - Intermedio

### Mejorando el Admin: Questions

Podemos mejorar el Django admin de la siguiente manera; en el archivo admin.py:

```python
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)

```

### Mejorando el Admin: Change List

Mejoramos aún más el Admin con:

```python
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)

```

[Documentación de The Django admin site](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/)

## Bonus: ajustes finales

### Comenzando a crear un Frontend

Le dimos una estructura HTML correcta al index.html.

### Añadiendo estilos al home de nuestra aplicación

Una buena práctica de CSS es usar [Reset CSS](https://meyerweb.com/eric/tools/css/reset/)

### Creando la estructura de la vista de detalle

La encuentras en el código 😉

### Finalizando los estilos de la vista de detalle

La encuentras en el código 😉

## Examen intermedio

- ¿Cuál de los siguientes formatos no se corresponde a un archivo estático?: py
- En Django se pueden crear tests tanto para Modelos como para Vistas. Esto es: verdadero
- ¿Qué son los tests?: Son funciones que verifican que tu código opera correctamente
- ¿Cuál es el atributo que permite cambiar el orden de los campos, en la creación de un modelo, en el administrador de Django?: fields
- ¿Cuál de los siguientes pasos no forma parte del flujo de escritura de tests sobre código ya escrito?: probamos manualmente la aplicación
- ¿Cómo debería ser el nombre de un test?: lo más largo y descriptivo posible
- ¿Cuál de los siguientes es el significado del acrónimo TDD?: Test Driven Development
- ¿Qué comando permite correr los tests escritos sobre una aplicación?: `python manage.py tests app_name` 💢
- ¿Cuál de las siguientes NO es una ventaja de hacer tests?: permite añadir milisegundos blab bla
- ¿Cuál de los siguientes atributos, añadidos a una clase, en el archivo admin.py, nos permite cambiar algún aspecto del administrador de Django?: todas