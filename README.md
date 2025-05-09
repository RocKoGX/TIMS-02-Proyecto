# Modulo_Facturacion
Módulo de Facturación para el curso de TESTING, IMPLANTACIÓN Y MANTENIMIENTO DE SISTEMAS
- Para ejecutar esta app primero se debe descomprimir el archivo "venv.rar" y activar el entorno virtual usando el comando *venv\Scripts\activate* en el cmd de la carpeta raiz "Modulo_Facturación-main".
•	NOTA: Si no funciona con el archivo ‘venv’ descomprimido se debe crear el entorno virtual con el siguiente comando: *python -m venv venv*
•	Volvemos a ejecutar el comando para activar el entorno virtual: *venv\Scripts\activate*
•	Cuando esté activado, instalamos Django dentro del entorno (esto en caso ocurra un error en la cual no encuentre la librería Django ya instalada anteriormente) con el comando: *pip install django*

- Luego, estando en modo venv, ejecutamos *python manage.py migrate* para que todo el sistema Django funcione correctamente.
- Ingresamos el comando *python manage.py runserver* para ejecutar la app.
- En un navegador web dirigirse a la URL: http://127.0.0.1:8000/ para comenzar a interactuar con el módulo de facturación.