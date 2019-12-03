import random, sys, time, pygame
from pygame.locals import *

pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()


FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FLASHSPEED = 500 # milisegundos
FLASHDELAY = 200 
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 4 # segundos para el game over si no hay acciones.

#                R    G    B   (paleta de colores)
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 90)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# objetos rectangulo para cada boton
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT   = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT    = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT  = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4, FAIL

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('El Saimon')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Segui el patron clickeando los botones o usando las teclas Q, W, A, S.', 1, WHITE)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (70, WINDOWHEIGHT - 25)

    # cargar archivos de sonido - botones
    BEEP1 = pygame.mixer.Sound('Laser.ogg')
    BEEP2 = pygame.mixer.Sound('Laser.ogg')
    BEEP3 = pygame.mixer.Sound('Laser.ogg')
    BEEP4 = pygame.mixer.Sound('Laser.ogg')
    FAIL  = pygame.mixer.Sound('Fail.ogg')

    #musica de fondo
    pygame.mixer.music.load("Tetris.mp3")
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)

    # inicializar variables para nueva partida
    pattern = [] # guarda secuencia de los colores
    currentStep = 0 # proximo color que el jugador debe tocar
    lastClickTime = 0 # marca del ultimo boton tocado por el jugador
    puntos = 0


    esperaToque = False # False para reproducir el patron. True, a la espera del jugador para que siga la secuencia:

    perdiste= None
    
    while True: # Bucle principal del juego


        
#EXPERIMENTAL - - - - - - - - MENSAJE PERDISTE - - - - - - - - - - - - 
       
#EXPERIMENTAL - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        clickedButton = None # boton que fue tocado (toma valores YELLOW, RED, GREEN o BLUE)
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        scoreSurf = BASICFONT.render('Puntuacion: ' + str(puntos), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 370, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get(): # Eventos con mouse y/o teclas
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN



        if not esperaToque:
            # empieza secuencia
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            esperaToque = True
        else:
            # a la espera del jugador que ingresa secuencia
            if clickedButton and clickedButton == pattern[currentStep]:
                # toco boton correcto
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # toco el ultimo boton de la secuencia
                    changeBackgroundAnimation()
                    puntos += 1
                    esperaToque = False
                    currentStep = 0 # volver a primer secuencia

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # toco boton incorrecto o se quedo sin tiempo
                gameOverAnimation()
                # reiniciar variables para nueva partida:
                pattern = []
                currentStep = 0
                esperaToque = False
                puntos = 0
                perdiste= True
                pygame.time.wait(100)
                changeBackgroundAnimation()
                
        if perdiste == True:
            ##pygame.display.update()
    
            scoreSurf = BASICFONT.render('PERDISTE: ', 1, WHITE)
            scoreRect = scoreSurf.get_rect()
            scoreRect.topleft =(WINDOWWIDTH - 370, 10)
            DISPLAYSURF.blit(scoreSurf, scoreRect)
            pygame.display.flip()
##            (75,WINDOWHEIGHT - 35)
            pygame.time.wait(1000)
##            pygame.display.update()
            scoreSurf = BASICFONT.render('', 1, WHITE)
            scoreRect = scoreSurf.get_rect()
            scoreRect.topleft =(WINDOWWIDTH - 370, 10)
            DISPLAYSURF.blit(scoreSurf, scoreRect)
            pygame.display.flip()
            perdiste = False
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # tomar eventos QUIT
        terminate() # termina si hay eventos QUIT presentes
    for event in pygame.event.get(KEYUP): # toma eventos KEYUP 
        if event.key == K_ESCAPE:
            terminate() # termina si el evento KEYUP fue la tecla Esc
        pygame.event.post(event) # devuelve objetos de eventos KEYUP


def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))


def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE,   BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED,    REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN,  GREENRECT)


def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed): # bucle de animaciones
        checkForQuit()
        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0))

        drawButtons() # redibuja los botones

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor


def gameOverAnimation(color=WHITE, animationSpeed=50):
    # reproduce beeps y el fondo hace flahses
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    
    FAIL.play()
    
    r, g, b = color
    for i in range(3): # flashea 3 veces el fondo
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # La primer vuelta en este For establece el siguiente for 
            # para ir desde 0 a 255 y de ahi desde 255 a 0.
            for alpha in range(start, end, animationSpeed * step): # bucle de animacion
                # alpha es la transparencia. 255 opaco, 0 transparente
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)



def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint( (x, y) ):
        return YELLOW
    elif BLUERECT.collidepoint( (x, y) ):
        return BLUE
    elif REDRECT.collidepoint( (x, y) ):
        return RED
    elif GREENRECT.collidepoint( (x, y) ):
        return GREEN
    return None


if __name__ == '__main__':
    main()
