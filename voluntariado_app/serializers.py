"""
Serializers de voluntariado_app.

Un ModelSerializer por cada clase del modelo de datos. Convierten los
objetos del ORM a JSON (y viceversa) para que los ViewSets puedan
exponerlos en la API REST.
"""
from rest_framework import serializers

from .models import (
    Pais, Region, Provincia, Comuna, Direccion,
    CategoriaActividad, EstadoActividad,
    Organizacion, Coordinador, Voluntario, Actividad, Inscripcion,
)


class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = '__all__'


class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'


class CategoriaActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaActividad
        fields = '__all__'


class EstadoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoActividad
        fields = '__all__'


class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacion
        fields = '__all__'


class CoordinadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinador
        fields = '__all__'


class VoluntarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voluntario
        fields = '__all__'


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'

    def validate(self, datos):
        """La fecha de término no puede ser anterior a la de inicio."""
        inicio = datos.get('fecha_inicio', getattr(self.instance, 'fecha_inicio', None))
        termino = datos.get('fecha_termino', getattr(self.instance, 'fecha_termino', None))
        if inicio and termino and termino < inicio:
            raise serializers.ValidationError(
                {'fecha_termino': 'La fecha de término no puede ser anterior a la fecha de inicio.'}
            )
        return datos


class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'
