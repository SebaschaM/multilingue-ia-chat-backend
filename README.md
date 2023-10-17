<div align="center">
  <img src="https://raw.githubusercontent.com/56kcloud/Training/master/img/docker_logo.png" alt="Docker Logo" width="100" height="100" />
  <img src="https://flask-training-courses.uk/images/flask-logo.png" alt="Flask Logo" width="100" height="100" />
  <img src="https://th.bing.com/th/id/R.d8acd2b243a62aa4567215a9099b10b4?rik=Bgp%2fnQs8ZDhJbw&riu=http%3a%2f%2ficons.iconarchive.com%2ficons%2fcornmanthe3rd%2fplex%2f512%2fOther-python-icon.png&ehk=kKuy%2bH0f2AqPgUtHwzM%2fmN4VFDzN8IYiy%2fojW%2blY6jY%3d&risl=&pid=ImgRaw&r=0" alt="Python Logo" width="100" height="100" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/1985px-Postgresql_elephant.svg.png" alt="PostgreSQL Logo" width="100" height="100" />

  # Multilingue IA Chat
</div>

---
## Configuracion inicial
Clonar el archivo .env.template y renombrarlo a .env
```bash
DATABASE_URL=postgresql://postgres:sebas@localhost:5433/multilingue
# DATABASE_URL=postgresql://postgres:sebas@db:5432/multilingue
SECRET_KEY=

MAIL_SERVER=smtp.googlemail.com
MAIL_USERNAME=
MAIL_PASSWORD=
```
#### Detalles:
- DATABASE_URL: URL de la base de datos
- SECRET_KEY: Llave secreta para el manejo de sesiones y generacion de tokens
- MAIL_SERVER: Servidor de correo
- MAIL_USERNAME: Usuario de correo
- MAIL_PASSWORD: Contraseña de correo
En los casos de MAIL_USERNAME y MAIL_PASSWORD, se recomienda usar una cuenta de correo de gmail, y habilitar el acceso a aplicaciones menos seguras. Para mas informacion, puede consultar el siguiente enlace: https://support.google.com/accounts/answer/6010255?hl=es
## Crear entorno virtual
```bash
python -m venv venv
```

## Activar entorno virtual
```bash
./venv/Scripts/activate
```

## Instalación de requirements.txt 🗒️

Asegúrate de tener Python instalado y sigue estos pasos para instalar las dependencias de tu proyecto:

1. Abre una terminal y navega hasta la carpeta de tu proyecto.

2. Ejecuta el siguiente comando para instalar las dependencias desde el archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
## Configuración de Docker 🐳

Para configurar Docker en tu proyecto, sigue estos pasos:

1. Instala Docker en tu sistema operativo. Puedes seguir las instrucciones específicas para tu sistema en [el sitio oficial de Docker](https://docs.docker.com/get-docker/).

2. El docker-compose.yml contiene la configuración de los servicios que se van a ejecutar. En este caso, se ejecutará un servicio de Python y un servicio de PostgreSQL.

3. Ejecutalo de la siguiente manera en tu terminal para levantar los servicios:

   ```bash
   docker-compose up -d
   ```

## Configuracion PostgreSQL 🐘

Asegúrate de tener PostgreSQL instalado:

- Modificar el archivo .env.template con los datos de tu base de datos.



## Ejecución 🚀
- Si deseas ejecutar desde el propio proyecto, ejecuta el siguiente comando en tu terminal:

   ```bash
   python run.py
   ```

- Si deseas ejecutar desde Docker, ejecuta el siguiente comando en tu terminal:

   ```bash
    docker-compose up -d
    ```

## Documentación de la API 📖
- POSTMAN: https://documenter.getpostman.com/view/20632691/2s9YC5xXso

## Construido con 🛠️
- [Python](https://www.python.org/) - Lenguaje de programación
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Framework de Python
- [Docker](https://www.docker.com/) - Contenedores
- [PostgreSQL](https://www.postgresql.org/) - Base de datos
- [Docker Compose](https://docs.docker.com/compose/) - Orquestador de contenedores

## Autores ✒️




