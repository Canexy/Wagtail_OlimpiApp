# Django 'OlimpiApp' - Versión con Wagtail
## Sistema de gestión para competiciones deportivas desarrollado con Django.

## Implementaciones:

### Modelos (*models.py*)
Los siguientes modelos están debidamente implementados para su creación en */admin*.
- **Equipos**: Con opción *'olímpico'*.
- **Disciplinas**: Configuración de límites de equipos, participantes por equipo y duración.
- **Pistas**: Con opción *'cubierta'*.
- **Árbitros**: Creación de perfiles de árbitros.
- **Participantes**: Creación de perfiles de participantes, relacionados con equipos y con validaciones frente a su eliminación.
- **Encuentros**: Gestión de eventos con estados automáticos y validaciones para el resto de campos.

Se ha añadido también una tabla *n:m* que incluye la relación de *Encuentros* y *Equipos*.

### Funcionalidades:
- Validaciones de integridad de datos en modelos (no a nivel de base de datos).
- Panel de administración Django personalizado con vistas de búsqueda.
- Estados automáticos de encuentros basados en las fechas previstas en su creación.
- Prevención de eliminación de equipos con encuentros asociados.

### Configuración y ejecución (contemplada únicamente en Linux):

#### Instalación de Python y Pip (en distribución Debian)
Con los siguientes comandos instalaremos Python y Pip respectivamente.

```console
sudo apt update
sudo apt install python3
```

```console
sudo apt install python3-pip
```

---

#### Creación del entorno virtual
Creamos el entorno virtual sobre el que trabajaremos y donde tendremos todas las dependencias que necesitemos para el proyecto.

```console
python3 -m venv .venv
```

#### Activación del entorno virtual
Con el siguiente comando activaremos dicho entorno virtual creado. Sobre la ruta donde se haya creado:

```console
source .venv/bin/activate
```

---

### Clonación del repositorio
#### Instalación de Git
Será necesario la instalación de Git para el posterior comando de clonación de repositorios.

```console
sudo apt install git
sudo apt update
```

Comprobamos que la instalación se ha realizado con éxito.

```console
git --version
```

<sup>Se recomienda encarecidamente configurar Git para futuros usos relacionados.

#### Clonación en local
Con el siguiente comando tendremos una copia en local del repositorio disponible en Github con los últimos cambios.

```console
git clone https://github.com/Canexy/Django_OlimpiApp.git
```

Hecho esto, navegamos dentro de la carpeta creada donde ejecutaremos el resto de comandos para su configuración y uso.

```console
cd Django_OlimpiApp/
```

---

#### Instalación de dependencias dentro del entorno virtual creado:
Es ahora cuando sobre el entorno virtual, instalaremos las dependencias necesarias para la aplicación.

```console
pip install -r requirements.txt
```

---

### Ejecución del servidor de la aplicación
Asegurándonos que el entorno virtual está activado y todas las dependencias están instaladas debidamente, ejecutamos el comando desde raíz del proyecto.

```console
python3 manage.py runserver
```

Si todo va bien, aparecerá un enlace `http://127.0.0.1:8080`, haciendo referencia al 'localhost' y puerto sobre el que se está inicializando. Copiando dicha dirección en un navegador o haciendo Ctrl + click sobre el enlace que se muestra en consola, nos llevará a la página principal.

---

### Vista de Administrador

Por defecto, aún no hay un 'index' como tal de nuestra web. Es decir, el enlace de antes no nos llevará a ningún lado o no mostrará nada, sólo un código de error.

Añadiendo `/admin` al final del enlace nos llevará a la vista de Administrador de Django:

`http://127.0.0.1:8080/admin/`


#### Accediendo a la vista

Por defecto, las credenciales son `admin` para usuario y `admin` para contraseña.

Ya dentro, podremos ver cada tabla y acceder al contenido de cada una de ellas.

---

### Novedades:

- Se han añadido diferentes vistas de lista y detalle para Equipos. 

Será accesible desde el enlace `http://127.0.0.1:8000/register_par/equipos/` para la visualización completa de todos los equipos registrados en la base de datos actual.

Una vez dentro, podemos seleccionar cada equipo para visualizar los detalles del mismo, como su ID, participantes y la opción *olímpico*.

> Un equipo olímpico se forma con la idea de que sus miembros no pertenezcan al mismo centro educativo.

- Se ha creado el comando `numequ` para el visionado por consola del número de Equipos.

De nuevo, nace de la idea del visionado de los diferentes equipos existentes en la base de datos, ya sean todos, o según la opción *olímpico*.

```console
python3 manage.py numequ
```

Sin opción veremos la totalidad de equipos existentes. Usando la opción `-o` seguido de `s` ó `n` podemos ver los equipos *olímpicos* o *no olímpicos*. Alternativamente, se puede usar con la opción `-h` para más información sobre su uso.