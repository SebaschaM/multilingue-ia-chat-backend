from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()


def configure_mail(current_app):
    mail = Mail(current_app)
    current_app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    current_app.config["MAIL_PORT"] = 465
    current_app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    current_app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    current_app.config["MAIL_USE_TLS"] = False
    current_app.config["MAIL_USE_SSL"] = True
    return mail


def send_email(mail, email, name):
    try:
        msg = Message(
            "Bienvenido a nuestra aplicación",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[email],
        )
        msg.html = f"""
        <html>
        <head>
            <!-- Puedes agregar estilos CSS aquí -->
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    padding: 20px;
                }}
                .container {{
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                .code {{
                    font-size: 24px;
                    color: #007bff; /* Puedes cambiar el color según tus preferencias */
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <img src="https://logosmarcas.net/wp-content/uploads/2020/09/Microsoft-Logo.png" alt="Logo de la aplicación" width="150">
                <h1>Bienvenido, {name}!</h1>
                <p>Gracias por registrarte en nuestra aplicación.</p>
                <p>Esperamos que disfrutes de tu experiencia con nosotros.</p>
                <p>Saludos,</p>
                <p>El equipo de la aplicación</p>
            </div>
        </body>
        </html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False
