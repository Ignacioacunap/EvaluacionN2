"""
Rutas propias de voluntariado_app.

Estas rutas se incluyen desde core/urls.py mediante include(), por eso
aquí no repetimos prefijos del proyecto.

  /             -> página de bienvenida (vista de función)
  /api/         -> API REST (el DefaultRouter genera todas las rutas CRUD)
"""
from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'voluntariado_app'

# El router crea automáticamente, para cada ViewSet registrado:
#   /api/<prefijo>/        -> GET (listar) y POST (crear)
#   /api/<prefijo>/<id>/   -> GET, PUT, PATCH y DELETE
enrutador = routers.DefaultRouter()

enrutador.register(r'paises', views.PaisViewSet)
enrutador.register(r'regiones', views.RegionViewSet)
enrutador.register(r'provincias', views.ProvinciaViewSet)
enrutador.register(r'comunas', views.ComunaViewSet)
enrutador.register(r'direcciones', views.DireccionViewSet)
enrutador.register(r'categorias-actividad', views.CategoriaActividadViewSet)
enrutador.register(r'estados-actividad', views.EstadoActividadViewSet)
enrutador.register(r'organizaciones', views.OrganizacionViewSet)
enrutador.register(r'coordinadores', views.CoordinadorViewSet)
enrutador.register(r'voluntarios', views.VoluntarioViewSet)
enrutador.register(r'actividades', views.ActividadViewSet)
enrutador.register(r'inscripciones', views.InscripcionViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(enrutador.urls)),
]
