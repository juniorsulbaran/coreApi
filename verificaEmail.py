from conexiones import conectar_base_datos 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage 
import os
import requests
db = conectar_base_datos()

def obtener_verificacion_por_email(token):
    try:
        cursor = db.cursor()
        
        # La solución clave: Asegurar que el token sea enviado como tupla
        cursor.execute("SELECT password, activo FROM usuarios WHERE password = ?", (str(token),))
        
        resultado = cursor.fetchone()

        if resultado:
            return True
        else:
            return False

    except Exception as e:
        print(f"Error al verificar usuario: {str(e)}")
        return False
    finally:
        cursor.close()
            


def enviarCorreoVerificacion(email, nombreApellido, hashed_password):
    """
    Función para enviar un correo electrónico de verificación y luego hacer POST a la URL.
    
    :param email: Correo del destinatario.
    :param nombreApellido: Nombre del usuario.
    :param hashed_password: Hash para la verificación.
    """
    # Configuración del servidor SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_from = "testsencillo@gmail.com"
    password = "mgrh fevq zgvo pnkw"  # Considera usar variables de entorno
    email_to = email

    # URL de verificación
    verification_url = f"http://10.0.0.40/verifica/?id={hashed_password}"

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = email_from
    mensaje["To"] = email_to
    mensaje["Subject"] = "Bienvenido a Good Juego"

    # Cuerpo del mensaje en HTML
    html = f"""
        <html>
            <body>
                <p>Hola {nombreApellido}, Bienvenido</p>
                <p>Este es un correo de prueba del registro en la plataforma Good Juego.</p>
                <div style="text-align: center;">
                    <img src="cid:imagen1" style="max-width: 100%; height: auto;">
                    <p>¡Gracias por unirte a nosotros!</p>
                    <a href="{verification_url}" style="text-decoration: none; color: #ffffff; background-color: #007bff; padding: 10px 20px; border-radius: 5px;">Verifica Tu Cuenta Good Juego</a>
                </div>
            </body>
        </html>
    """

    mensaje.attach(MIMEText(html, 'html'))

    # Adjuntar imagen
    ruta_imagen = os.path.join(os.path.dirname(__file__), 'static', 'image', 'logobody.jpg')
    
    try:
        with open(ruta_imagen, 'rb') as f:
            img_data = f.read()
            imagen = MIMEImage(img_data)
            imagen.add_header('Content-ID', '<imagen1>')
            imagen.add_header('Content-Disposition', 'inline', filename=os.path.basename(ruta_imagen))
            mensaje.attach(imagen)
    except Exception as e:
        print(f"Error al adjuntar imagen: {e}")

    # Enviar el correo
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_from, password)
        texto = mensaje.as_string()
        server.sendmail(email_from, email_to, texto)
        print("Correo enviado exitosamente!")
        
        # Ahora hacemos POST a la URL de verificación
        try:
            response = requests.post(verification_url)  # Cambiado a 'requests' en lugar de 'request'
            print(f"POST a {verification_url} - Estado: {response.status_code}")
        except Exception as e:
            print(f"Error al hacer POST: {e}")
            
    except Exception as e:
        print(f"Error al enviar correo: {e}")
    finally:
        if 'server' in locals():  # Verifica si la variable server existe
            server.quit()
