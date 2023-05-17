import pygame
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHTYELLOW = (150, 150, 0)
BLUE = (0, 0, 255)
SKYBLUE = (135, 206, 250)
GREEN = (0, 255, 0)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
BALL_SIZE = 15

# 볼 클래스
class Ball :
    def __init__(self) :
        # 공의 중심 좌표를 임의로 지정
        self.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
        self.y = random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)

        # 다음 이동 방향을 설정
        self.change_x = 0
        while self.change_x == 0 or self.change_y == 0 :
            self.change_x = random.randint(-4, 4)
            self.change_y = random.randint(-4, 4)

        # 공의 색상을 지정
        r = random.randint(1, 255)
        g = random.randint(1, 255)
        b = random.randint(1, 255)
        self.color = (r, g, b)

# 글자 출력 메소드
def txtprint(txt, cor, w, h) :
    STR = str(txt)
    text = font.render(STR, True, cor)
    screen.blit(text, [w, h])

# 게임 시작 메소드
def playgame() :
    # 여러 볼의 갖는 리스트에 첫 볼을 저장
    lstballs = []
    lstballs.append(Ball())

    USERCOLOR = WHITE # 유저 색
    USERSPEED = 5 # 유저 이동 속도
    usersize = 20 # 유저 사이즈
    user = pygame.Rect(400, 400, usersize, usersize) # 유저 x, y 사이즈

    moveDown = False
    moveUp = False
    moveLeft = False
    moveRight = False

    done = False
    Start_time = time.time() # 시작 시간
    
    while not done :
        Last_time = time.time() - Start_time # 경과 시간
        Last_time = round(Last_time, 2)
        Ball_time = Last_time # 볼 생성 시간

        # 게임 진행 시간 출력
        txtprint(str(Last_time), WHITE, 700, 10)
        pygame.display.update()
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                done = True
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    exit()
                    # 게임 종료
                elif event.key == pygame.K_UP :
                    moveUp = True
                    moveDown = False
                elif event.key == pygame.K_DOWN :
                    moveDown = True
                    moveUp = False
                elif event.key == pygame.K_LEFT :
                    moveLeft = True
                    moveRight = False
                elif event.key == pygame.K_RIGHT :
                    moveRight = True
                    moveLeft = False
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP :
                    moveUp = False
                elif event.key == pygame.K_DOWN :
                    moveDown = False
                elif event.key == pygame.K_LEFT :
                    moveLeft = False
                elif event.key == pygame.K_RIGHT :
                    moveRight = False
        
        if (round(Ball_time % 1, 2) < 0.02): # 1초 마다 랜덤으로 볼 생성
            lstballs.append(Ball())
            Ball_time = 0.02
        

        for ball in lstballs :
            # 볼의 중심 좌표를 이동
            ball.x += ball.change_x
            ball.y += ball.change_y

            # 윈도 벽에 맞고 바운싱
            # x 좌표가 좌, 우를 벗어나면
            if ball.x > SCREEN_WIDTH - BALL_SIZE or ball.x < BALL_SIZE :
                ball.change_x *= -1 # 다음 이동 좌표의 증가 값을 부호 변경
                
            # y 좌표가 위, 아래를 벗어나면
            if ball.y > SCREEN_HEIGHT - BALL_SIZE or ball.y < BALL_SIZE :
                ball.change_y *= -1 # 다음 이동 좌표의 증가 값을 부호 변경

        screen.fill(BLACK)

        # 모든 볼을 그리기
        for ball in lstballs :
            pygame.draw.circle(screen, ball.color, [ball.x, ball.y], BALL_SIZE)

        # 유저 이동
        if moveDown and user[1] < SCREEN_HEIGHT - usersize :
            user[1] += USERSPEED
        if moveUp and user[1] > 0 :
            user[1] -= USERSPEED
        if moveLeft and user[0] > 0 :
            user[0] -= USERSPEED
        if moveRight and user[0] < SCREEN_WIDTH - usersize :
            user[0] += USERSPEED

        # 유저 그리기
        for i in range(1) :
            pygame.draw.rect(screen, USERCOLOR, user)

        # 아웃 판정
        for ball in lstballs :
            X = abs(ball.x - user[0])
            Y = abs(ball.y - user[1])
            SX = abs((ball.x + BALL_SIZE) - (user[0] + usersize))
            SY = abs((ball.y + BALL_SIZE) - (user[1] + usersize))
            
            if X <= 14 and Y <= 14 :
                done = True

            if SX <= 14 and SY <= 14 :
                done = True

        # 초당 60 프레임으로 그리기
        clock.tick(60)
        pygame.display.flip()

    # 게임 종료 후 결과
    res = True
    name = ""
    while res :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                res = False
            if event.type == pygame.KEYDOWN :
                if event.unicode.isalpha() :
                    name += event.unicode
                elif event.key == pygame.K_BACKSPACE :
                    name = name[:-1]
                elif event.key == pygame.K_SPACE :
                    f = open('GOMBARANK.txt', 'a')
                    f.write(str(name + ' '))
                    f.write(str(Last_time) + '\n')
                    f.close()
                    res = False
        
        screen.fill(BLACK)

        txtprint('PRESS SPACE KEY', WHITE, 210, 150)
        txtprint('NAME : ', WHITE, 250, 350)
        txtprint(name, WHITE, 405, 350)
        txtprint(str(Last_time), WHITE, 360, 500)
        pygame.display.update()

# 랭크 출력 및 정렬 메소드
def grank() :
    f = open('GOMBARANK.txt', 'r')
    lines = f.readlines()
    f.close()

    name = []
    time = []
    
    for i in lines :
        i = i.split()
        name.append(i[0])
        time.append(float(i[1]))

    topname = []
    toptime = []

    for i in range(5) :
        if not time :
            break;
        topname.append(name[time.index(max(time))])
        toptime.append(time[time.index(max(time))])
        del name[time.index(max(time))]
        del time[time.index(max(time))]
    
    res = True
    while res :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                res = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    res = False
        screen.fill(BLACK)

        txtprint('PRESS SPACE KEY', WHITE, 210, 150)
        
        wid = 230
        hei = 300
        i = 1
        for name in topname:
            txtprint(str(i) + ' : ', WHITE, wid, hei)
            wid += 60
            txtprint(name, WHITE, wid, hei)
            hei += 80
            i += 1
            wid = 230
            
        wid = 450
        hei = 300
        for time in toptime :
            txtprint(time, WHITE, wid, hei)
            hei += 80
            i += 1

        pygame.display.update()
            



# 메인 프로그램
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("곰바운드")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 50) # 폰트, 사이즈

menu = True

gamestart = pygame.Rect(250, 150, 300, 100)
gamerank = pygame.Rect(250, 350, 300, 100)
gameend = pygame.Rect(250, 550, 300, 100)

lstmenu = []
lstmenu.append(gamestart)
lstmenu.append(gamerank)
lstmenu.append(gameend)

SNOW_CNT = 150 # 눈의 개수
snow_list = [] # 눈의 좌표 리스트

for i in range(SNOW_CNT) :
    x = random.randrange(0, SCREEN_WIDTH)
    y = random.randrange(1, SCREEN_HEIGHT)
    snow_list.append([x, y])

# 화면 수정에 사용될 시계 저장
clock = pygame.time.Clock()

USERCOLOR = RED # 유저 색
USERSPEED = 5 # 유저 이동 속도
usersize = 20 # 유저 사이즈
user = pygame.Rect(400, 400, usersize, usersize) # 유저 x, y 사이즈

moveDown = False
moveUp = False
moveLeft = False
moveRight = False

SELECT = False
GSTA = False
GRAK = False
GEND = False

# 메인 메뉴
while menu :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            done = True
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE :
                SELECT = True
            elif event.key == pygame.K_UP :
                moveUp = True
                moveDown = False
            elif event.key == pygame.K_DOWN :
                moveDown = True
                moveUp = False
            elif event.key == pygame.K_LEFT :
                moveLeft = True
                moveRight = False
            elif event.key == pygame.K_RIGHT :
                moveRight = True
                moveLeft = False
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_SPACE :
                SELECT = False
            elif event.key == pygame.K_UP :
                moveUp = False
            elif event.key == pygame.K_DOWN :
                moveDown = False
            elif event.key == pygame.K_LEFT :
                moveLeft = False
            elif event.key == pygame.K_RIGHT :
                moveRight = False

    screen.fill(BLACK)

    # 눈 내리는 모습 그리기
    for i in range(len(snow_list)) :
        # 눈 모양 원 그리기
        radius = 1
        pygame.draw.circle(screen, WHITE, snow_list[i], radius)
        snow_list[i][1] += 1
        snow_list[i][0] += random.randint(-1, 1)
        if snow_list[i][1] > SCREEN_HEIGHT :
            snow_list[i][1] = random.randrange(-5, 0)
            snow_list[i][0] = random.randrange(0, SCREEN_WIDTH)
    
    # 메뉴 그리기
    for lsmenu in lstmenu :
        pygame.draw.rect(screen, LIGHTYELLOW, lsmenu)

    # 게임 스타트 셀렉트
    if user[0] >= 250 and user[0] <= 550 and user[1] >= 150 and user[1] <= 250 :
        pygame.draw.rect(screen, SKYBLUE, gamestart)
        GSTA = True
    else :
        GSTA = False

    # 게임 랭크 셀렉트
    if user[0] >= 250 and user[0] <= 550 and user[1] >= 350 and user[1] <= 450 :
        pygame.draw.rect(screen, SKYBLUE, gamerank)
        GRAK = True
    else :
        GRAK = False

    # 게임 종료 셀렉트
    if user[0] >= 250 and user[0] <= 550 and user[1] >= 550 and user[1] <= 650 :
        pygame.draw.rect(screen, SKYBLUE, gameend)
        GEND = True
    else :
        GEND = False

     # 유저 이동
    if moveDown and user[1] < SCREEN_HEIGHT - usersize :
        user[1] += USERSPEED
    if moveUp and user[1] > 0 :
        user[1] -= USERSPEED
    if moveLeft and user[0] > 0 :
        user[0] -= USERSPEED
    if moveRight and user[0] < SCREEN_WIDTH - usersize :
        user[0] += USERSPEED

    # 메뉴 셀렉트
    if GSTA == True and SELECT == True :
        GSTA = False
        SELECT = False
        playgame()
    elif GRAK == True and SELECT == True :
        GRAK = False
        SELECT = False
        grank()
    elif GEND == True and SELECT == True :
        GEND = False
        SELECT = False
        exit()

    # 메뉴 글씨
    txtprint('GAME START', GREEN, 270, 170)
    txtprint('GAME RANK', GREEN, 275, 370)
    txtprint('END', GREEN, 360, 570)
    
    # 유저 그리기
    for i in range(1) :
        pygame.draw.rect(screen, USERCOLOR, user)

    clock.tick(60)
    pygame.display.flip()
