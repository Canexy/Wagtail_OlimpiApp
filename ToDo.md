
# (13/11)
## Hecho:
- Instalación de Wagtail mediante Pip.
- Añadido de Wagtail en INSTALLED_APPS y MIDDLEWARE en `/olimpi_app/settings.py`, además de configuración extra necesarias a pie de página.
- Modificación de `/olimpi_app/urls.py` para añadir ruta a **Administración de Wagtail** (*/wadmin*), `/documents` (aún sin implementar bien) y *recursive path* para `/register_par/urls.py`.
- Acción *makemigrations* y *migrate* sobre los cambios.

## Cosas que aún no sé del todo.
- Origen y/o uso de `/admin` por parte de Wagtail (no sé dónde crea el archivo o cómo lo crea).
- Uso del propio Wagtail en general.

---