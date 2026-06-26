import pygame
import random
import sys


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("alarm.mp3")
pygame.mixer.music.play(-1)

# Configuración
ANCHO = 1920
ALTO = 1080
FPS = 60

PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Bad Tero")

RELOJ = pygame.time.Clock()

# Colores
CELESTE = (135, 206, 235)
VERDE = (50, 180, 50)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Fuentes
fuente_grande = pygame.font.SysFont(None, 72)
fuente_media = pygame.font.SysFont(None, 48)
fuente_pequena = pygame.font.SysFont(None, 32)

# Física
GRAVEDAD = 0.5
SALTO = -9

# Tubos
ANCHO_TUBO = 80
ESPACIO = 180
VEL_TUBO = 4

# Sprite
tero_img = pygame.image.load("tero.png").convert_alpha()
tero_img = pygame.transform.scale(tero_img, (150, 150))


def dibujar_texto(texto, fuente, color, y):
    surf = fuente.render(texto, True, color)
    PANTALLA.blit(
        surf,
        (ANCHO // 2 - surf.get_width() // 2, y)
    )


def pantalla_principal():
    while True:
        PANTALLA.fill(CELESTE)

        dibujar_texto("BAD TERO", fuente_grande, NEGRO, 150)
        dibujar_texto("ESPACIO PARA JUGAR", fuente_media, NEGRO, 280)
        dibujar_texto("ESC PARA SALIR", fuente_pequena, NEGRO, 350)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def cuenta_regresiva():
    for numero in [3, 2, 1]:
        inicio = pygame.time.get_ticks()

        while pygame.time.get_ticks() - inicio < 1000:

            PANTALLA.fill(CELESTE)

            dibujar_texto(
                str(numero),
                fuente_grande,
                NEGRO,
                240
            )

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


def crear_tubo():
    altura = random.randint(120, 350)

    return {
        "x": ANCHO,
        "arriba": pygame.Rect(
            ANCHO,
            0,
            ANCHO_TUBO,
            altura
        ),
        "abajo": pygame.Rect(
            ANCHO,
            altura + ESPACIO,
            ANCHO_TUBO,
            ALTO - altura - ESPACIO
        ),
        "contado": False
    }


def game_over(puntaje):
    while True:

        PANTALLA.fill((30, 30, 30))

        dibujar_texto(
            "GAME OVER",
            fuente_grande,
            BLANCO,
            150
        )

        dibujar_texto(
            f"Puntaje: {puntaje}",
            fuente_media,
            BLANCO,
            260
        )

        dibujar_texto(
            "R = REINTENTAR",
            fuente_pequena,
            BLANCO,
            340
        )

        dibujar_texto(
            "ESC = SALIR",
            fuente_pequena,
            BLANCO,
            380
        )

        pygame.display.flip()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_r:
                    return

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def jugar():

    tero_x = 150
    tero_y = ALTO // 2
    tero_vel = 0

    puntaje = 0

    tubos = []

    for i in range(3):
        tubo = crear_tubo()

        tubo["x"] += i * 300
        tubo["arriba"].x = tubo["x"]
        tubo["abajo"].x = tubo["x"]

        tubos.append(tubo)

    jugando = True

    while jugando:

        RELOJ.tick(FPS)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_SPACE:
                    tero_vel = SALTO

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        tero_vel += GRAVEDAD
        tero_y += tero_vel

        tero_rect = pygame.Rect(
            tero_x + 8,
            int(tero_y) + 8,
            48,
            48
        )

        for tubo in tubos:

            tubo["x"] -= VEL_TUBO

            tubo["arriba"].x = tubo["x"]
            tubo["abajo"].x = tubo["x"]

            if tubo["x"] < -ANCHO_TUBO:

                nuevo = crear_tubo()

                nuevo["x"] = max(
                    t["x"] for t in tubos
                ) + 300

                nuevo["arriba"].x = nuevo["x"]
                nuevo["abajo"].x = nuevo["x"]

                tubos.remove(tubo)
                tubos.append(nuevo)

                break

            if (
                not tubo["contado"]
                and tubo["x"] + ANCHO_TUBO < tero_x
            ):
                tubo["contado"] = True
                puntaje += 1

            if (
                tero_rect.colliderect(tubo["arriba"])
                or tero_rect.colliderect(tubo["abajo"])
            ):
                jugando = False

        if tero_y < -50 or tero_y > ALTO:
            jugando = False

        PANTALLA.fill(CELESTE)

        for tubo in tubos:

            pygame.draw.rect(
                PANTALLA,
                VERDE,
                tubo["arriba"]
            )

            pygame.draw.rect(
                PANTALLA,
                VERDE,
                tubo["abajo"]
            )

        angulo = max(-30, min(30, -tero_vel * 3))

        sprite = pygame.transform.rotate(
            tero_img,
            angulo
        )

        PANTALLA.blit(
            sprite,
            (tero_x, int(tero_y))
        )

        texto = fuente_media.render(
            str(puntaje),
            True,
            NEGRO
        )

        PANTALLA.blit(
            texto,
            (ANCHO // 2, 30)
        )

        pygame.display.flip()

    return puntaje


while True:

    pantalla_principal()
    cuenta_regresiva()

    resultado = jugar()

    game_over(resultado)
