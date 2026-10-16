from django.shortcuts import render
from rest_framework import viewsets

from .models import (
    Pais, Region, Provincia, Comuna, Direccion,
    CategoriaActividad, EstadoActividad,
    Organizacion, Coordinador, Voluntario, Actividad, Inscripcion,
)
from .serializers import (
    PaisSerializer, RegionSerializer, ProvinciaSerializer, ComunaSerializer,
    DireccionSerializer, CategoriaActividadSerializer, EstadoActividadSerializer,
    OrganizacionSerializer, CoordinadorSerializer, VoluntarioSerializer,
    ActividadSerializer, InscripcionSerializer,
)


# ---------------------------------------------------------------------------
# Vistas basadas en función (FBV): sitio web básico de la Evaluación 1
# ---------------------------------------------------------------------------
def home(request):
    """
    Vista de bienvenida del proyecto.

    Reemplaza la página por defecto de Django y presenta el proyecto
    "Plataforma de Voluntariados y Actividades Comunitarias".
    """
    contexto = {
        'titulo_proyecto': 'Plataforma de Voluntariados y Actividades Comunitarias',
        'descripcion': (
            'Sistema para centralizar la gestión de organizaciones sociales, '
            'voluntarios, coordinadores y actividades comunitarias, permitiendo '
            'llevar un historial consistente de la participación y el estado '
            'de cada actividad.'
        ),
    }
    return render(request, 'voluntariado_app/home.html', contexto)


def error_404(request, exception):
    """
    Vista personalizada para el error 404.

    Django la invoca automáticamente (ver handler404 en core/urls.py)
    cada vez que se solicita una ruta que no existe.
    """
    return render(request, 'voluntariado_app/404.html', status=404)


# ---------------------------------------------------------------------------
# Vistas basadas en clase (CBV): API REST con ModelViewSet
#
# Cada ModelViewSet entrega automáticamente el CRUD completo:
#   GET (listar / detalle), POST (crear), PUT (reemplazar),
#   PATCH (modificar parcialmente) y DELETE (eliminar).
# ---------------------------------------------------------------------------
class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer


class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer


class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer


class CategoriaActividadViewSet(viewsets.ModelViewSet):
    queryset = CategoriaActividad.objects.all()
    serializer_class = CategoriaActividadSerializer


class EstadoActividadViewSet(viewsets.ModelViewSet):
    queryset = EstadoActividad.objects.all()
    serializer_class = EstadoActividadSerializer


class OrganizacionViewSet(viewsets.ModelViewSet):
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer


class CoordinadorViewSet(viewsets.ModelViewSet):
    queryset = Coordinador.objects.all()
    serializer_class = CoordinadorSerializer


class VoluntarioViewSet(viewsets.ModelViewSet):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer


class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer


class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
