# Haircut voting thing
# September 2018
# Aaron Burton
# for python 3

import pygame
import json

def readData():
    with open('data.json') as file:
        data = json.load(file)
    return data
        

def writeData(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)


pygame.init()
width = 00
height = 00
bground = (30,30,30)
window = pygame.display.set_mode((width,height),pygame.FULLSCREEN)
#mainDisplay = pygame.display.set_mode((width,height))
height = pygame.display.Info().current_h
width = pygame.display.Info().current_w
pygame.display.set_caption('Racer Registration')
clock = pygame.time.Clock()

textFont  = pygame.font.Font(pygame.font.match_font("courier"),24)
nameFont  = pygame.font.Font(pygame.font.match_font("Impact"),42)

pygame.mixer.init()
coin = pygame.mixer.Sound("smb_coin.wav")
powerup = pygame.mixer.Sound("smb_powerup.wav")
pause = pygame.mixer.Sound("smw_pause.wav")
clear = pygame.mixer.Sound("smb_stage_clear.wav")

def button(text,x,y,w,h,ic,ac):
    clicked = False
    mouse = pygame.mouse.get_pos()
    if x < mouse[0] < x+w and y < mouse[1] < y+h:
        color = ac
        if pygame.mouse.get_pressed()[0]:
            clicked = True
    else:
        color = ic
    pygame.draw.rect(window, color, [x,y,w,h])
    textSurf = textFont.render(text, True, (0,0,0))
    textRect = textSurf.get_rect()
    textRect.center = (x+(w/2),y+(h/2))
    window.blit(textSurf,textRect)
    return clicked

teachers = readData()

running = True
while running:

    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: running = False
            if event.key == pygame.K_ESCAPE: running = False
    

    for i,teacher in enumerate(teachers):
        y = 100+100*i
        nameText = nameFont.render(teacher['name'], True, (0,0,0))
        nameRect = nameText.get_rect()
        nameRect.topright = (290,y)
        pygame.draw.rect(window, (99,99,99), nameRect)
        window.blit(nameText,nameRect)
        votes = 0
        for j, cut in enumerate(teacher['cuts']):
            x = 300+300*j
            percent = cut[1]/teacher['votes']
            if button(cut[0]+': '+str(cut[1]),x,y,250,50,
                      ((1-percent)*255,percent*255,0),
                      (100,100,255)):
                cut[1] += 1
                coin.play()
                print(teacher['name'], cut[0], cut[1])
            votes += cut[1]
        teacher['votes'] = votes
                
    if button('Save',width-100,height-50,100,50,(0,0,150),(50,50,255)):
        writeData(teachers)
        pause.play()
    if button('Quit',width-100,0,100,50,(150,0,0),(255,50,50)):
        running = False
        clear.play()
        pygame.time.delay(5500)
    if button('ReLoad',0,height-50,100,50,(0,150,0),(50,255,50)):
        teachers = readData()
        powerup.play()
    
    pygame.display.update()
    clock.tick(15)
    while pygame.mouse.get_pressed()[0]:
        pygame.event.get()

pygame.quit()
