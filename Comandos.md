
# Comandos útiles.

## Creación de 'requirements' con las dependencias:
```console
pip freeze > requirements.txt
```

---

## Traer cambios entre ramas, de 'testing' a 'main'.
Pequeños comandos que uso para el paso de cambios entre ramas.

'main' es la rama principal, con cambios que funcionan siempre y está correctamente implementados.
'testing' es una rama experimental donde implemento dichos cambios por primera vez, para la depuración de errores.

```console
git checkout main
git pull origin main
git merge testing
git push origin main
```

---

## Uso del comando 'numequ'.
Comando creado para la tarea 'Consola de Administración'.
Dicho comando listará todos los equipos que existen actualmente en la base de datos. Con el uso de la opción '-o' y  's' ó 'n' (sí o no), se podrá filtrar por aquellos equipos que sean olímpicos o no.

```console
python manage.py numequ -h
```

### Ejemplo de uso rápido.
Lista aquellos equipos que existan en la base de datos que sean olímpicos.

```console
python manage.py numequ s
```

---



## Uso de Docker para entrar en la base de datos.
Será necesario que se ejecute dentro de la ruta donde se encuentre db.sqlite3, la base de datos.

```console
docker run -it --rm -v "$(pwd)":/data alpine:latest sh -c   "apk add --no-cache sqlite && sqlite3 /data/db.sqlite3"
```

---

## Creación de E/R a partir de 'django-extensions'.

```console
python manage.py graph_models register_par -o graph.dot
```

```console
dot -Tpng graph.dot -o graph.png
```

---

