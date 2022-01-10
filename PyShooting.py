#2022.01.10
#Park Minhee
#Shooting Game


import pygame
import sys
import random #운석 랜덤으로 떨구기
from time import sleep

padWidth = 480 #배경 가로세로길이지정
padHeight = 640 #세로
rockImage = ['rock01.png','rock02.png','rock03.png','rock04.png','rock05.png', \
             'rock06.png','rock07.png','rock08.png','rock09.png','rock10.png', \
             'rock11.png','rock12.png','rock13.png','rock14.png','rock15.png', \
             'rock16.png','rock17.png','rock18.png','rock19.png','rock20.png', \
             'rock21.png','rock22.png','rock23.png','rock24.png','rock25.png', \
             'rock26.png','rock27.png','rock28.png','rock29.png','rock30.png']
explosionSound = ['explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav',]

def drawObject(obj, x, y): #게임에 등장하는 객체 드로잉
    global gamePad 
    gamePad.blit(obj,(x,y))

def writeScore(count):
    global gamePad
    font=pygame.font.Font('NanumGothic.ttf',20) #폰트
    text=font.render('파괴한 운석 수:'+str(count),True,(255,255,255))#RGB
    gamePad.blit(text,(10,0)) #위치

def writePassed(count): #놓친 운석 수 카운트
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf',20)
    text = font.render('놓친 운석 수:'+ str(count), True, (255,0,0))
    gamePad.blit(text,(350,0))

def writeMessage(text): #게임 메세지 출력
    global gamePad, gameOverSound
    textfont = pygame.font.Font('NanumGothic.ttf',80)
    text = textfont.render(text, True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2) #중앙위치
    gamePad.blit(text,textpos)
    pygame.display.update()
    pygame.mixer.music.stop() #배경음악정지
    gameOverSound.play() #게임 오버 사운드 재생
    sleep(2) #2초 멈춤
    pygame.mixer.music.play(-1) #배경 음악 재생
    runGame() #게임 실행

def crash(): #파괴 메세지
    global gamePad
    writeMessage('전투기 파괴!')

def gameOver(): #게임 오버 메세지
    global gamePad
    writeMessage('게임 오버!')
                     
    
def initGame(): #게임 시작 전 초기화하는 부분
    
    global gamePad, clock, background, fighter, missile,explosion, missileSound, gameOverSound #게임 패드, 시간 전역변수 지정
    pygame.init() #시작 시 초기화
    gamePad=pygame.display.set_mode((padWidth, padHeight)) #화면에 표시 될 gamePad 출력
    pygame.display.set_caption('PyShooting') #캡션부분 PyShootiong으로 표시
    background=pygame.image.load('background.png') #배경 그림
    fighter = pygame.image.load('fighter.png') #전투기 그림
    missile = pygame.image.load('missile.png') #미사일 그림
    explosion = pygame.image.load('explosion.png') #폭발 그림
    pygame.mixer.music.load('music.wav') #배경음악
    pygame.mixer.music.play(-1) #배경음악재생
    missileSound = pygame.mixer.Sound('missile.wav') #미사일 사운드
    gameOverSound = pygame.mixer.Sound('gameover.wav') #게임 오버 사운드
    clock = pygame.time.Clock()
    clock=pygame.time.Clock() 


def runGame():#게임 시작할 때 실행되는 부분
    global gapdPad,clock, background,fighter, missile,explosion,missileSound

    #전투기 크기
    fighterSize=fighter.get_rect().size
    fighterWidth=fighterSize[0]
    fighterHeight=fighterSize[1]

    #전투기 초기 위치
    x=padWidth*0.45 
    y=padHeight*0.9
    fighterX=0

    #전투기 미사일에 운석이 맞은 경우 true
    isShot = False #맞은 경우 false
    shotCount = 0 #갯수 카운트
    rockPassed = 0 #놓친 것 카운트
    
    missileXY=[] #무기 좌표 리스트

    #운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage)) #이미지 중 하나 랜덤 초이스
    rockSize = rock.get_rect().size #크기를 다 다르게 설정
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound (random.choice(explosionSound))

    #운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - rockWidth) #운석 초기 위치 랜덤하게 설정
    rockY = 0 #꼭대기부터 떨어지게 
    rockSpeed = 2 #스피드 설정
    
    onGame=False #게임 진행 중에는 실행하지 않음
    while not onGame: 
        for event in pygame.event.get(): 
            if event.type in [pygame.QUIT]:  #게임 종료 부분
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:#KEYDOWN 이벤트 : 키 입력 받을 때
                if event.key == pygame.K_LEFT: #왼쪽 이동키를 누르면
                    fighterX -= 5 #(-5만큼 왼쪽 이동)

                elif event.key == pygame.K_RIGHT: #오른쪽 이동 키
                    fighterX += 5

                elif event.key == pygame.K_SPACE: #스페이스 - 미사일 발사
                    missileSound.play() #미사일 사운드 재생
                    missileX = x + fighterWidth/2 #전투기 가운데에서 나올 수 있게끔 좌표 설정
                    missileY = y - fighterHeight 
                    missileXY.append([missileX,missileY]) #x,y좌표값 저장


            if event.type in [pygame.KEYUP]: #KEYUP 이벤트 : 키 입력을 멈추면
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: 
                    fighterX=0 #전투기가 멈춤

            
            
        drawObject(background, 0, 0) #배경화면 그리기

        #위치가 바뀌었으니 전투기 위치 재조정
        x += fighterX #바뀐 좌표를 x좌표로 변경
        if x<0: #게임 왼쪽 밖으로 빠져나갈 수 없게 조정
            x=0
        elif x>padWidth - fighterWidth: #게임 오른 쪽 밖으로 빠져나갈 수 없게 조 
            x=padWidth - fighterWidth


        #전투기가 운석과 충돌했는 지 체크

        if y < rockY + rockHeight: #운석 좌표(x,y)
            if(rockX > x and rockX < x + fighterWidth) or \
                     (rockX + rockWidth > x and rockX + rockWidth):
                crash()
            
        drawObject(fighter,x,y) #비행기를 게임 화면 (x,y)좌표에 그리기

        #미사일을 화면에 노출시키기
        if len(missileXY) != 0: #미사일 length가 0이 아니면
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10 #미사일을 y좌표 기준 -10씩 발사
                missileXY[i][1] = bxy[1] #-10만큼 이동된 값이 missileXY로 변환

                if bxy[1] < rockY: #미사일이 운석 shot
                    if bxy[0] > rockX and bxy[0] < rockX+ rockWidth: #돌 부분 겹치냐
                        missileXY.remove(bxy) #없애고
                        isShot = True #샷은 트루
                        shotCount += 1 #샷 카운트 +
                    
                if bxy[1] <= 0: #미사일이 화면 밖으로 넘어가면
                    try:
                        missileXY.remove(bxy) #제거
                    except:
                        pass #아니면 패스

                    
        if len(missileXY)!=0: #미사일이 0이 아니면
            for bx, by in missileXY: 
                drawObject(missile, bx, by) #미사일 그리기


        writeScore(shotCount)#맞춘 것 카운트
        
        rockY += rockSpeed #운석 아래로 움직임


        if rockY > padHeight: #운석 y좌표 부분, 운석이 화면 밖으로 지나가면
            
            rock=pygame.image.load(random.choice(rockImage))
            rockSize=rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY=0
            rockPassed += 1 #놓친 것 카운
            #새로운 운석 고름

        #운석 일정 갯수 이상 놓치면, 게임 오
        if rockPassed == 3:
            gameOver()

        writePassed(rockPassed) #놓친 운석 수 표시

        if isShot: #운석 맞춘 경우
            #운석 폭발 노출
            drawObject(explosion, rockX,rockY)
            destroySound.play() #운석 폭발 사운드 재생

            #폭발 시켰으니까 새로운 운석 그린다.  
            rock=pygame.image.load(random.choice(rockImage))
            rockSize=rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY=0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            rockSpeed += 0.2 # 맞출수록 운석 스피드 증가
            if rockSpeed >= 100: #10이상이 되면 10으로 맞춰준다
                rockSpeed = 100
            
        drawObject(rock, rockX, rockY) #운석 그리기
        
                

        pygame.display.update() #게임 화면을 다시 update

        clock.tick(60) #게임 화면의 초당 프레임 수 60 지정

    pygame.quit() #pygame 종료

initGame() #initGame()함수 호출 
runGame() #runGame() 함수 호출
