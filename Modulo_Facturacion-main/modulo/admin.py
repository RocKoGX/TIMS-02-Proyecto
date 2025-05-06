from django.contrib import admin
from .models import Cliente  # Importa tu modelo Cliente

# Registrar el modelo para que aparezca en Django Admin
admin.site.register(Cliente)
