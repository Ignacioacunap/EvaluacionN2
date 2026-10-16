from django.contrib import admin

from .models import (
    Pais, Region, Provincia, Comuna, Direccion,
    CategoriaActividad, EstadoActividad,
    Organizacion, Coordinador, Voluntario, Actividad, Inscripcion,
)

# Registro de todas las clases del modelo de datos en el administrador de Django.
admin.site.register(Pais)
admin.site.register(Region)
admin.site.register(Provincia)
admin.site.register(Comuna)
admin.site.register(Direccion)
admin.site.register(CategoriaActividad)
admin.site.register(EstadoActividad)
admin.site.register(Organizacion)
admin.site.register(Coordinador)
admin.site.register(Voluntario)
admin.site.register(Actividad)
admin.site.register(Inscripcion)
