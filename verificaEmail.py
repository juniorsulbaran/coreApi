import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage 
import os

def enviarCorreoVerificacion(email,nombreApellido):
    """
    Función para enviar un correo electrónico de verificación.
    
    :param email_from: Correo del remitente.
    :param email_to: Correo del destinatario.
    :param subject: Asunto del correo.
    :param body: Cuerpo del correo.
    """
    # Configuración del servidor SMTP
    smtp_server = "smtp.gmail.com"  # Servidor SMTP de Gmail (puede ser otro)
    smtp_port = 587  # Puerto para TLS
    email_from = "testsencillo@gmail.com"
    password = "mgrh fevq zgvo pnkw"  # Considera usar variables de entorno para esto
    email_to = email

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = email_from
    mensaje["To"] = email_to
    mensaje["Subject"] = "Bienvenido a Good Juego"

    # Cuerpo del mensaje
    # Cuerpo del mensaje en HTML con la imagen
    html = f"""
        <html>
            <body>
                <p>Hola {nombreApellido}, Bienvenido</p>
                <p>Este es un correo de prueba del registro en la plataforma Good Juego.</p>
                <div style="text-align: center;">
                <img src="cid:imagen1" style="max-width: 100%; height: auto;">
                </div>
            </body>
        </html>
    """

    # Adjuntar el HTML
    mensaje.attach(MIMEText(html, 'html'))

    # Ruta a la imagen (ajusta según tu estructura de archivos)
    ruta_imagen = os.path.join(os.path.dirname(__file__), 'static', 'image', 'logobody.jpg')

    try:
        with open(ruta_imagen, 'rb') as f:
            img_data = f.read()
            imagen = MIMEImage(img_data)
            imagen.add_header('Content-ID', '<imagen1>')  # Referencia en HTML con cid:imagen1
            imagen.add_header('Content-Disposition', 'inline', filename=os.path.basename(ruta_imagen))
            mensaje.attach(imagen)
    except FileNotFoundError:
        print(f"Error: No se encontró la imagen en {ruta_imagen}")
    except Exception as e:
        print(f"Error al adjuntar la imagen: {e}")
        # Enviar el correo
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Habilitar encriptación TLS
        server.login(email_from, password)
        texto = mensaje.as_string()
        server.sendmail(email_from, email_to, texto)
        print("Correo enviado exitosamente!")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        server.quit()

