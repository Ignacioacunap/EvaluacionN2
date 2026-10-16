# Plataforma de Voluntariados y Actividades Comunitarias

Backend en Python + Django + Django REST Framework (MySQL) para digitalizar la
gestión de actividades comunitarias de una organización social: centraliza la
información de organizaciones, voluntarios, coordinadores y actividades,
manteniendo el historial de participación de cada voluntario.

> **Evaluación 2 – Programación Backend (INACAP 2026).** Sobre la base de la
> Evaluación 1 se agregan: modelo de datos, persistencia en MySQL, migraciones,
> variables de entorno, Django REST Framework (serializers, ModelViewSet y
> Router) y CRUD completo.

## Estructura del proyecto

```
proyecto_voluntariado/
├── core/                      # Núcleo Django (settings.py lee todo desde .env)
├── voluntariado_app/
│   ├── fixtures/              # Datos iniciales (países, regiones, comunas, catálogos)
│   ├── migrations/            # Migraciones del modelo de datos
│   ├── templates/voluntariado_app/   # base.html, home.html, 404.html
│   ├── models.py              # Modelo de datos (12 clases)
│   ├── admin.py               # Registro de los modelos en el admin
│   ├── serializers.py         # Un ModelSerializer por modelo
│   ├── views.py               # Un ModelViewSet por modelo (+ home y error_404)
│   └── urls.py                # DefaultRouter con todas las rutas de la API
├── sql/                       # Scripts SQL: base de datos, usuario y permisos
├── .env.example               # Plantilla de variables de entorno
├── manage.py
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.12 o superior
- MySQL Server 8 (y cliente `mysql` o MySQL Workbench)
- Git

> En Windows, `mysqlclient` suele instalarse sin problemas con `pip`. En
> Linux requiere `libmysqlclient-dev` y `pkg-config` antes del `pip install`.

## Instalación paso a paso

1. **Clonar el repositorio y crear el ambiente virtual**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd proyecto_voluntariado
   python -m venv .venv
   ```
2. **Activar el ambiente virtual**
   - Windows (PowerShell): `.venv\Scripts\Activate`
   - macOS / Linux: `source .venv/bin/activate`
3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```
4. **Crear la base de datos, el usuario y los permisos** (scripts en `sql/`).
   Ejecutar como `root` de MySQL:
   ```bash
   mysql -u root -p < sql/00_configuracion_completa.sql
   ```
   (equivale a ejecutar en orden `01_crear_base_datos.sql`,
   `02_crear_usuario.sql` y `03_asignar_permisos.sql`).
5. **Variables de entorno**: copiar `.env.example` como `.env` y completar los
   valores. `DB_PASSWORD` debe ser la misma clave usada en
   `sql/02_crear_usuario.sql`. Para generar una `SECRET_KEY` nueva:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
   ```
6. **Aplicar las migraciones**
   ```bash
   python manage.py migrate
   ```
7. **Cargar los datos iniciales** (fixtures; respetar el orden):
   ```bash
   python manage.py loaddata data_paises data_regiones data_provincias data_comunas data_estados_actividad data_categorias_actividad
   ```
8. **(Opcional) Crear un superusuario** para el panel `/admin/`:
   ```bash
   python manage.py createsuperuser
   ```
9. **Levantar el servidor**
   ```bash
   python manage.py runserver
   ```

## Variables de entorno (`.env`)

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | `True` en desarrollo (permite ver estilos de la API y del admin) |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por coma |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Credenciales de la base MySQL |
| `DB_HOST`, `DB_PORT` | Servidor y puerto de MySQL |

El archivo `.env` está en `.gitignore`: no se sube al repositorio.
Para ver la página 404 personalizada, poner `DEBUG=False` en el `.env`
(con `DEBUG=True` Django muestra su página técnica de depuración).

## Modelo de datos

| Modelo | Descripción | Relaciones principales |
|---|---|---|
| `Pais`, `Region`, `Provincia`, `Comuna` | Tablas geográficas (fixtures SUBDERE) | Región → Provincia → Comuna |
| `Direccion` | Dirección física | → Comuna |
| `CategoriaActividad`, `EstadoActividad` | Catálogos | — |
| `Organizacion` | Organización social | → Direccion |
| `Coordinador` | Responsable de actividades | → Organizacion |
| `Voluntario` | Persona voluntaria | → Organizacion, Pais, Direccion |
| `Actividad` | Actividad comunitaria | → Organizacion, Coordinador, Categoria, Estado, Direccion |
| `Inscripcion` | Voluntario inscrito a una actividad (historial: asistencia y horas) | → Voluntario, Actividad (par único) |

## API REST

Base: `http://127.0.0.1:8000/api/` (la raíz lista todos los endpoints).

| Endpoint | Modelo |
|---|---|
| `/api/paises/` | Pais |
| `/api/regiones/` | Region |
| `/api/provincias/` | Provincia |
| `/api/comunas/` | Comuna |
| `/api/direcciones/` | Direccion |
| `/api/categorias-actividad/` | CategoriaActividad |
| `/api/estados-actividad/` | EstadoActividad |
| `/api/organizaciones/` | Organizacion |
| `/api/coordinadores/` | Coordinador |
| `/api/voluntarios/` | Voluntario |
| `/api/actividades/` | Actividad |
| `/api/inscripciones/` | Inscripcion |

Cada endpoint soporta, mediante `ModelViewSet` + `DefaultRouter`:

| Método | Ruta | Acción |
|---|---|---|
| GET | `/api/<recurso>/` | Listar |
| POST | `/api/<recurso>/` | Crear |
| GET | `/api/<recurso>/<id>/` | Detalle |
| PUT | `/api/<recurso>/<id>/` | Reemplazar |
| PATCH | `/api/<recurso>/<id>/` | Modificar parcialmente |
| DELETE | `/api/<recurso>/<id>/` | Eliminar |

### Ejemplo de uso (orden sugerido para crear datos)

1. `POST /api/organizaciones/`
   ```json
   { "nombre": "Fundación Manos Solidarias", "correo": "contacto@manos.cl" }
   ```
2. `POST /api/coordinadores/`
   ```json
   { "nombre": "Ana Pérez", "rut": "12345678-9", "organizacion": 1 }
   ```
3. `POST /api/voluntarios/`
   ```json
   { "nombre": "Luis Rojas", "rut": "20123456-7", "fecha_nacimiento": "2000-05-10", "organizacion": 1 }
   ```
4. `POST /api/actividades/`
   ```json
   {
     "nombre": "Limpieza de playa", "fecha_inicio": "2026-11-01T10:00:00Z",
     "fecha_termino": "2026-11-01T14:00:00Z", "cupos": 20,
     "categoria": 3, "estado": 1, "organizacion": 1, "coordinador": 1
   }
   ```
5. `POST /api/inscripciones/`
   ```json
   { "voluntario": 1, "actividad": 1 }
   ```
6. `PATCH /api/inscripciones/1/`
   ```json
   { "asistio": true, "horas_aportadas": 4 }
   ```

Reglas de validación: la `fecha_termino` de una actividad no puede ser anterior
a su `fecha_inicio`, y un voluntario no puede inscribirse dos veces a la misma
actividad.

## Otras rutas

| Ruta | Descripción |
|---|---|
| `/` | Página de bienvenida |
| `/admin/` | Panel de administración de Django |
| cualquier otra | Página 404 personalizada |
