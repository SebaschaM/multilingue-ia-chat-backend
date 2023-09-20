from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

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


def send_email(mail, email, name, token=None):
    expiration_time = datetime.now() + timedelta(minutes=5)
    expiration_time_str = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    verification_link = f"https://tuaplicacion.com/verificar?token={token}"

    try:
        msg = Message(
            "Bienvenido a nuestra aplicación",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[email],
        )
        msg.html = f"""
        <html>
            <head>
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
                .verification-button {{
                    background-color: #007bff;
                    color: #ffffff !important;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    text-decoration: none;
                    font-weight: bold;
                }}
                .message-box {{
                    margin-top: 20px;
                }}
                .message-text {{
                    color: #808080;
                    font-weight: bold;
                }}
                </style>
            </head>
            <body>
                <div class="container">
                <img
                    src="https://logosmarcas.net/wp-content/uploads/2020/09/Microsoft-Logo.png"
                    alt="Logo de la aplicación"
                    width="150"
                />
                <p>Gracias por registrarte en nuestra aplicación.</p>
                <p>Para verificar tu cuenta, haz clic en el siguiente botón:</p>
                <a class="verification-button" href="{verification_link}" target="_blank"
                    >
                    Verificar mi cuenta
                    </a
                >

                <div class="message-box">
                    <p class="message-text">
                    El enlace de verificación caducará el {expiration_time_str}. Si no has
                    solicitado la verificación, puedes ignorar este mensaje.
                    </p>
                </div>

                <p>Esperamos que disfrutes de tu experiencia con nosotros.</p>
                <p>Saludos, el equipo de la aplicación</p>
                </div>
            </body>
        </html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False
