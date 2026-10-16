"""
Configuración de URLs del proyecto core.

Aquí solo se define la ruta al panel de administración y se delega
(mediante include) todo el resto de rutas del sitio a voluntariado_app,
que es la aplicación particular de este proyecto. Entre esas rutas está
la API REST, disponible bajo /api/.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('voluntariado_app.urls')),
]

# Handler del error 404: le indicamos a Django que use nuestra propia
# vista en vez de la página de error genérica.
handler404 = 'voluntariado_app.views.error_404'
