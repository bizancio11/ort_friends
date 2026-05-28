import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
import getpass
import time
import random

def type_text(text, delay=0.015, extra_random=False, end="\n"):
    """Efecto de tipeo letra por letra como en Hacknet, con end opcional"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay + random.uniform(-0.008, 0.012) if extra_random else delay)
    sys.stdout.write(end)
    sys.stdout.flush()

def init_text():
    type_text("""
        Bienvenido a Repuls io portatil
        
        Por favor iniciar sesion
          
        Creador: bizancio11(Repuls)
            
        Human Made, No AI slop
        
        

    """, delay=0.05)



            


# Inicializa la aplicación
app = QApplication(sys.argv)

# Crea la vista web y carga la URL
view = QWebEngineView()
view.setUrl(QUrl("https://repuls.io/"))
view.setObjectName("Repuls IO")
# Muestra la ventana y ejecuta el bucle de la app


def Auth():
    users = { "@SP": "shadow123"}
    login = input(type_text("Usuario: ", delay=0.05))
    if login in users:
        password = getpass.getpass(type_text("Contraseña: ", delay=0.05))
        if password == users[login]:
            init_text()
            view.show()
            sys.exit(app.exec_())

Auth()