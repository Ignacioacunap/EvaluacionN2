"""
Modelo de datos de la Plataforma de Voluntariados y Actividades Comunitarias.

Sigue el mismo estilo del ejemplo del profesor (biblio_app):
  - tablas geográficas de Chile (Region -> Provincia -> Comuna -> Direccion),
  - tablas de catálogo (CategoriaActividad, EstadoActividad),
  - tablas principales (Organizacion, Coordinador, Voluntario, Actividad),
  - tabla de relación con historial de participación (Inscripcion).

Cada modelo incluye 'habilitado' (borrado lógico) y, cuando corresponde,
'created_at' / 'updated_at' para auditoría.
"""
from django.db import models

# Textos reutilizados en varios modelos (evita repetir literales).
int_habilitado = 1
str_fecha_creacion = "Fecha Creación"
str_fecha_actualizacion = "Fecha Actualización"
str_codigo = "Código"
str_nombre = "Nombre"
str_descripcion = "Descripción"
str_www = "WWW"
str_email = "Email"
str_telefono = "Teléfono"
str_fecha_nac = "Fecha Nacimiento"


# ---------------------------------------------------------------------------
# Tablas geográficas (datos cargados desde fixtures)
# ---------------------------------------------------------------------------
class Pais(models.Model):
    nombre = models.CharField("País", max_length=50, null=False)
    nacionalidad = models.CharField("Nacionalidad", max_length=30, null=False)
    iso_2 = models.CharField("ISO 2", max_length=2, null=False)
    iso_3 = models.CharField("ISO 3", max_length=3, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)

    class Meta:
        db_table_comment = "Países del mundo, para asociar a la nacionalidad de los voluntarios."
        verbose_name_plural = "Países"

    def __str__(self):
        return self.nombre


class Region(models.Model):
    codigo = models.CharField(str_codigo, max_length=2, null=False)
    region = models.CharField("Región", max_length=41, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)

    class Meta:
        db_table_comment = "Regiones de Chile, data de SUBDERE."
        verbose_name_plural = "Regiones"

    def __str__(self):
        return self.region


class Provincia(models.Model):
    codigo = models.CharField(str_codigo, max_length=3, null=False)
    provincia = models.CharField("Provincia", max_length=50, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)

    class Meta:
        db_table_comment = "Provincias de Chile, data de SUBDERE. Pertenece a una región específica."

    def __str__(self):
        return self.provincia


class Comuna(models.Model):
    codigo = models.CharField(str_codigo, max_length=5, null=False)
    comuna = models.CharField("Comuna", max_length=60, null=False)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)

    class Meta:
        db_table_comment = "Comunas de Chile, data de SUBDERE. Pertenece a una provincia específica."

    def __str__(self):
        return self.comuna


class Direccion(models.Model):
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, null=False)
    calle = models.CharField("Calle", max_length=100, null=True, blank=True)
    numero = models.CharField("Número", max_length=10, null=True, blank=True)
    departamento = models.CharField("Dpto/Oficina", max_length=10, null=True, blank=True)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        db_table_comment = "Direcciones físicas de organizaciones, voluntarios y actividades."
        verbose_name_plural = "Direcciones"

    def __str__(self):
        return f"{self.calle or ''} {self.numero or ''}, {self.comuna}".strip()


# ---------------------------------------------------------------------------
# Tablas de catálogo
# ---------------------------------------------------------------------------
class CategoriaActividad(models.Model):
    categoria = models.CharField("Categoría", max_length=50, null=False)
    descripcion = models.CharField(str_descripcion, max_length=255, null=True, blank=True)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        db_table_comment = "Categorías temáticas de actividades comunitarias (educación, salud, medioambiente, etc.)."
        verbose_name_plural = "Categorías de actividad"

    def __str__(self):
        return self.categoria


class EstadoActividad(models.Model):
    estado = models.CharField("Estado", max_length=30, null=False)
    descripcion = models.CharField(str_descripcion, max_length=255, null=True, blank=True)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        db_table_comment = "Estados del ciclo de vida de una actividad (planificada, en curso, finalizada, cancelada)."
        verbose_name_plural = "Estados de actividad"

    def __str__(self):
        return self.estado


# ---------------------------------------------------------------------------
# Tablas principales
# ---------------------------------------------------------------------------
class Organizacion(models.Model):
    nombre = models.CharField(str_nombre, max_length=100, null=False)
    descripcion = models.TextField(str_descripcion, null=True, blank=True)
    web = models.URLField(str_www, null=True, blank=True)
    correo = models.EmailField(str_email, null=True, blank=True)
    telefono = models.CharField(str_telefono, max_length=15, null=True, blank=True)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, null=True, blank=True)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        db_table_comment = "Organizaciones sociales que convocan voluntarios y organizan actividades."
        verbose_name_plural = "Organizaciones"

    def __str__(self):
        return self.nombre


class Coordinador(models.Model):
    nombre = models.CharField(str_nombre, max_length=150, null=False)
    rut = models.CharField("RUT", max_length=12, null=False)
    correo = models.EmailField(str_email, null=True, blank=True)
    telefono = models.CharField(str_telefono, max_length=15, null=True, blank=True)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        db_table_comment = "Coordinadores responsables de organizar y supervisar actividades."
        verbose_name_plural = "Coordinadores"

    def __str__(self):
        return self.nombre


class Voluntario(models.Model):
    nombre = models.CharField(str_nombre, max_length=150, null=False)
    rut = models.CharField("RUT", max_length=12, null=False)
    correo = models.EmailField(str_email, null=True, blank=True)
    telefono = models.CharField(str_telefono, max_length=15, null=True, blank=True)
    fecha_nacimiento = models.DateField(str_fecha_nac, null=False)
    nacionalidad = models.ForeignKey(Pais, on_delete=models.CASCADE, null=True, blank=True)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, null=True, blank=True)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, null=False)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        db_table_comment = "Personas registradas como voluntarias en una organización."

    def __str__(self):
        return self.nombre


class Actividad(models.Model):
    nombre = models.CharField(str_nombre, max_length=150, null=False)
    descripcion = models.TextField(str_descripcion, null=True, blank=True)
    fecha_inicio = models.DateTimeField("Fecha Inicio", null=False)
    fecha_termino = models.DateTimeField("Fecha Término", null=False)
    cupos = models.PositiveIntegerField("Cupos de voluntarios", null=False)
    categoria = models.ForeignKey(CategoriaActividad, on_delete=models.CASCADE, null=False)
    estado = models.ForeignKey(EstadoActividad, on_delete=models.CASCADE, null=False)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, null=False)
    coordinador = models.ForeignKey(Coordinador, on_delete=models.CASCADE, null=False)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, null=True, blank=True)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    created_at = models.DateTimeField(str_fecha_creacion, auto_now_add=True)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        db_table_comment = "Actividades comunitarias organizadas por una organización y a cargo de un coordinador."
        verbose_name_plural = "Actividades"

    def __str__(self):
        return self.nombre


class Inscripcion(models.Model):
    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE, null=False)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, null=False)
    fecha_inscripcion = models.DateTimeField("Fecha Inscripción", auto_now_add=True)
    asistio = models.BooleanField("Asistió", default=False, null=False)
    horas_aportadas = models.PositiveIntegerField("Horas aportadas", default=0, null=False)
    observacion = models.CharField("Observación", max_length=255, null=True, blank=True)
    habilitado = models.BooleanField(int_habilitado, default=True, null=False)
    updated_at = models.DateTimeField(str_fecha_actualizacion, auto_now=True)

    class Meta:
        db_table_comment = "Inscripción de un voluntario a una actividad; guarda el historial de participación."
        constraints = [
            models.UniqueConstraint(
                fields=["voluntario", "actividad"],
                name="uq_inscripcion_voluntario_actividad",
            )
        ]
        verbose_name_plural = "Inscripciones"

    def __str__(self):
        return f"{self.voluntario} -> {self.actividad}"
