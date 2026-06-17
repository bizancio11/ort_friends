"""
F1 Arcade - Estructura base
Requisitos: pip install pygame
Ejecutar:   python f1_arcade.py
"""
import getpass
import sys
import pygame

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
ANCHO, ALTO = 800, 600
FPS = 60
TITULO = "F1 Reacing"

COLOR_FONDO = (30, 30, 40)
COLOR_PISTA = (60, 60, 60)
COLOR_LINEA = (220, 220, 220)
COLOR_JUGADOR = (220, 30, 30)
COLOR_RIVAL = (30, 120, 220)


# ---------------------------------------------------------------------------
# Entidades
# ---------------------------------------------------------------------------
class Coche:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.ancho = 40
        self.alto = 70
        self.color = color
        self.velocidad = 0
        self.vel_max = 12
        self.aceleracion = 0.2
        self.friccion = 0.1
        self.vidas = 3
        self.invulnerable = 0

    def acelerar(self):
        self.velocidad = min(self.velocidad + self.aceleracion, self.vel_max)

    def frenar(self):
        self.velocidad = max(self.velocidad - self.aceleracion * 2, 0)

    def mover(self, dx, dy):
        self.x += dx
        self.y += dy
        margen = (ANCHO - 400) // 2
        self.x = max(margen, min(self.x, ANCHO - margen - self.ancho))

    def actualizar(self):
        self.velocidad = max(self.velocidad - self.friccion, 0)
        if self.invulnerable > 0:
            self.invulnerable -= 1

    def dibujar(self, surface):
        if self.invulnerable > 0 and (self.invulnerable // 5) % 2 == 0:
            return
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.ancho, self.alto))


class Rival(Coche):
    def __init__(self, x, y):
        super().__init__(x, y, COLOR_RIVAL)
        self.velocidad = 4

    def ia(self, pista, jugador):
        self.y += (jugador.velocidad - self.velocidad)
        if self.y > ALTO:
            import random
            margen = (ANCHO - 400) // 2
            self.y = -100
            self.x = random.randint(margen, ANCHO - margen - self.ancho)
            self.velocidad = random.uniform(3, 7)


class Pista:
    def __init__(self):
        self.scroll = 0
        self.ancho_pista = 400
        self.curvatura = 0
        self.largo_vuelta = 2400
        self.progreso = 0

    def actualizar(self, velocidad_jugador):
        self.scroll = (self.scroll + velocidad_jugador) % 80
        self.progreso += velocidad_jugador
        if self.progreso >= self.largo_vuelta:
            self.progreso -= self.largo_vuelta
            return True
        return False

    def meta_y(self, ref_y):
        return ref_y - (self.largo_vuelta - self.progreso)

    def dibujar(self, surface):
        pygame.draw.rect(
            surface,
            COLOR_PISTA,
            ((ANCHO - self.ancho_pista) // 2, 0, self.ancho_pista, ALTO),
        )
        cx = ANCHO // 2
        y = -80 + self.scroll
        while y < ALTO:
            pygame.draw.rect(surface, COLOR_LINEA, (cx - 4, y, 8, 40))
            y += 80

        my = self.meta_y(ALTO - 50)
        if -40 < my < ALTO:
            margen = (ANCHO - self.ancho_pista) // 2
            cuadros = self.ancho_pista // 20
            for i in range(cuadros):
                color = (255, 255, 255) if (i % 2 == 0) else (0, 0, 0)
                pygame.draw.rect(surface, color, (margen + i * 20, my, 20, 20))


# ---------------------------------------------------------------------------
# Estados / HUD
# ---------------------------------------------------------------------------
class HUD:
    def __init__(self, fuente, nombre="Guest"):
        self.fuente = fuente
        self.nombre = nombre
        self.vuelta = 1
        self.total_vueltas = 35
        self.tiempo = 0
        self.posicion = 1

    def actualizar(self, dt, jugador):
        self.tiempo += dt

    def dibujar(self, surface, jugador):
        lineas = [
            f"Piloto: {self.nombre}",
            f"Vel: {int(jugador.velocidad * 20)} km/h",
            f"Vuelta: {self.vuelta}/{self.total_vueltas}",
            f"Vidas: {jugador.vidas}",
            f"Tiempo: {self.tiempo:0.1f}s",
        ]
        for i, t in enumerate(lineas):
            surface.blit(self.fuente.render(t, True, (255, 255, 255)), (10, 10 + i * 22))


# ---------------------------------------------------------------------------
# Juego principal
# ---------------------------------------------------------------------------
class Juego:
    def __init__(self, nombre="Guest"):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("consolas", 20)
        self.fuente_grande = pygame.font.SysFont("consolas", 48, bold=True)
        self.nombre = nombre

        self.pista = Pista()
        self.jugador = Coche(ANCHO // 2 - 20, ALTO - 120, COLOR_JUGADOR)
        margen = (ANCHO - 400) // 2
        self.rivales = [
            Rival(margen + 30, -50),
            Rival(ANCHO - margen - 70, -250),
            Rival(ANCHO // 2 - 20, -450),
        ]
        self.hud = HUD(self.fuente, nombre)

        self.activo = True
        self.pausado = False
        self.terminado = False
        self.gano = False

    # --- input -------------------------------------------------------------
    def manejar_eventos(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.activo = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    self.activo = False
                if ev.key == pygame.K_p:
                    self.pausado = not self.pausado

    def leer_teclas(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.jugador.acelerar()
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.jugador.frenar()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.jugador.mover(-5, 0)
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.jugador.mover(5, 0)

    # --- ciclo -------------------------------------------------------------
    def actualizar(self, dt):
        if self.pausado or self.terminado:
            return
        vuelta_completa = self.pista.actualizar(self.jugador.velocidad)
        if vuelta_completa:
            if self.hud.vuelta >= self.hud.total_vueltas:
                self.terminado = True
                self.gano = True
            else:
                self.hud.vuelta += 1
        self.jugador.actualizar()
        for r in self.rivales:
            r.ia(self.pista, self.jugador)
            r.actualizar()
        self.hud.actualizar(dt, self.jugador)
        self.detectar_colisiones()
        if self.jugador.vidas <= 0:
            self.terminado = True
            self.gano = False

    def detectar_colisiones(self):
        if self.jugador.invulnerable > 0:
            return
        rect_j = pygame.Rect(self.jugador.x, self.jugador.y,
                             self.jugador.ancho, self.jugador.alto)
        for r in self.rivales:
            rect_r = pygame.Rect(r.x, r.y, r.ancho, r.alto)
            if rect_j.colliderect(rect_r):
                self.jugador.vidas -= 1
                self.jugador.invulnerable = 90
                self.jugador.velocidad *= 0.3
                break

    def dibujar(self):
        self.pantalla.fill(COLOR_FONDO)
        self.pista.dibujar(self.pantalla)
        for r in self.rivales:
            r.dibujar(self.pantalla)
        self.jugador.dibujar(self.pantalla)
        self.hud.dibujar(self.pantalla, self.jugador)
        if self.pausado:
            txt = self.fuente.render("PAUSA", True, (255, 255, 0))
            self.pantalla.blit(txt, (ANCHO // 2 - 30, ALTO // 2))
        if self.terminado:
            msg = "GANASTE!" if self.gano else "GAME OVER"
            color = (50, 220, 50) if self.gano else (220, 50, 50)
            txt = self.fuente_grande.render(msg, True, color)
            self.pantalla.blit(txt, (ANCHO // 2 - txt.get_width() // 2, ALTO // 2 - 40))
            sub = self.fuente.render("ESC para salir", True, (255, 255, 255))
            self.pantalla.blit(sub, (ANCHO // 2 - sub.get_width() // 2, ALTO // 2 + 20))
        pygame.display.flip()

    def ejecutar(self):
        while self.activo:
            dt = self.reloj.tick(FPS) / 1000.0
            self.manejar_eventos()
            self.leer_teclas()
            self.actualizar(dt)
            self.dibujar()
        pygame.quit()
        sys.exit()


# ---------------------------------------------------------------------------
def Autenticacion():
    usuarios = {"Guest": "Guest", "SP": "shadow123"}
    login = input("Nombre de Usuario: ")
    if login in usuarios:
        password = getpass.getpass(f"Cual es tu contraseña {login}: ")
        if password in usuarios[login]:
            print(f"Bienvenido {login}")
            Juego(nombre=login).ejecutar()
        else:
            return False
    else:
        return False

if __name__ == "__main__":
    Autenticacion()
