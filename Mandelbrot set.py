import pygame,os
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

import datetime

def updateScreen():
    global res,mid,screen
    res = [int(1920/pixelSize),int(1080/pixelSize)]
    mid = [res[0]*pixelSize/2,res[1]*pixelSize/2]
    screen = pygame.display.set_mode((mid[0]*2,mid[1]*2))

org = int(input('Pixel size: '))
pixelSize = org
updateScreen()
clock = pygame.time.Clock()

power = 14
zoom = 1.5**power
cPos = [0,0]
x,y = -mid[0]/zoom+cPos[0],-mid[1]/zoom+cPos[1]
maxI = 100

def checkExit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def computeDraw():
    global x,y
    x,y = -mid[0]/zoom+cPos[0],-mid[1]/zoom+cPos[1]
    for i in range(res[0]):
        for j in range(res[1]):
            a,b = 0,0
            c = complex(x,y)
            n = -1
            while n < maxI and (a**2+b**2)**0.5<=2:
                n += 1
                a,b  = a**2-b**2+c.real,2*a*b+c.imag
            if n == maxI:
                color = 0
            else:
                color = min(n*(1/(maxI/1000)),255)
                color = -color+255
            pygame.draw.rect(screen,(color,color,color),(i*pixelSize,j*pixelSize,pixelSize,pixelSize))
            y += pixelSize/zoom
        x += pixelSize/zoom
        y = -mid[1]/zoom+cPos[1]
        if i%30 == 0 and i > 0:
            pygame.display.update()
            checkExit()
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                print('Aborted, but still saved')
                return
            if pixelSize == 1:
                print(round((i+1)/res[0]*100,1),'%','done',end='\r')
    if pixelSize == 1:
        print(round((i+1)/res[0]*100,1),'%','done',end='\r')

computeDraw()

r = 0.1

while True:
    checkExit()
    key = pygame.key.get_pressed()
    
    if key[pygame.K_LSHIFT]:
        s = 3
    else:
        s = 1
    
    if key[pygame.K_w]: power += s*1; zoom = 1.5**power;power = min(power,100); r = 50/zoom
    if key[pygame.K_s]: power -= s*1; zoom = 1.5**power;power = max(power,10); r = 50/zoom
    if key[pygame.K_UP]: cPos[1] -= s*r; cPos[1] = max(cPos[1],-8)
    if key[pygame.K_DOWN]: cPos[1] += s*r; cPos[1] = min(cPos[1],8)
    if key[pygame.K_RIGHT]: cPos[0] += s*r; cPos[0] = min(cPos[0],8)
    if key[pygame.K_LEFT]: cPos[0] -= s*r; cPos[0] = max(cPos[0],-8)
    if key[pygame.K_q]: maxI += s*5; maxI = min(maxI,1000)
    if key[pygame.K_a]: maxI -= s*5; maxI = max(maxI,2)
    if any(key[k] for k in [pygame.K_w,pygame.K_s,pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT,pygame.K_q,pygame.K_a]):
        computeDraw()
    
    if key[pygame.K_p]:
        print('Working directory: '+os.getcwd())
        path = input('Save image to path (with extension): ')
        sTime = datetime.datetime.now().strftime("%H:%M:%S")
        sSeconds = int(datetime.datetime.now().strftime("%H"))*60*60+int(datetime.datetime.now().strftime("%M"))*60+int(datetime.datetime.now().strftime("%S"))
        pixelSize = 1
        updateScreen();computeDraw()
        
        print()
        
        pygame.image.save(screen,path)
        print('START TIME:',sTime)
        eTime = datetime.datetime.now().strftime("%H:%M:%S")
        eSeconds = int(datetime.datetime.now().strftime("%H"))*60*60+int(datetime.datetime.now().strftime("%M"))*60+int(datetime.datetime.now().strftime("%S"))
        print('END TIME:',eTime)
        seconds = eSeconds-sSeconds
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if eTime < sTime:
            hours += 24        
        
        print('Time passed:',f'{hours}:{minutes}:{seconds}')
        pixelSize = org
        updateScreen();computeDraw()
    
    pygame.display.update()
    clock.tick(60)