import pygame
import serial
import random

try:
    ser = serial.Serial('COM12', 115200, timeout=1)
except serial.SerialException as e:
    print(f"Serial port error: {e}")
    exit()

pygame.init()
# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)
font50 = pygame.font.Font('freesansbold.ttf', 50)
font200 = pygame.font.Font('freesansbold.ttf', 200)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

MATCH_POINT = 10

MAX_SPEED = 12
# Basic parameters of the screen
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock() 
FPS = 60

class Paddle:
    def __init__(self, posx, posy, width, height, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.color = color
		# Rect that is used to control the position and collision of the object
        self.playerRect = pygame.Rect(posx, posy, width, height)
		# Object that is blit on the screen
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)
	
    def display(self):
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)
    
    def update(self, posy):
        self.posy = posy*(HEIGHT-self.height)
        self.playerRect.y = self.posy
#        print(self.posy)
    
    def displayScore(self, text, score, x, y, color):
        text = font50.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)
    
    def getRect(self):
        return self.playerRect

class Ball:
    def __init__(self, posx, posy, radius, speed, color, height):
        self.height = height
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speedx = speed
        self.speedy = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    def display(self):
         self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)
    
    def update(self):
        self.posx += self.speedx*self.xFac
        self.posy += self.speedy*self.yFac

		# If the ball hits the top or bottom surfaces, 
		# then the sign of yFac is changed and 
		# it results in a reflection
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0
        
    def reset(self):
        self.posx = WIDTH//2
        self.posy = HEIGHT//2
        self.xFac *= -1
        self.firstTime = 1
        self.speedx = 7
        self.speedy = 7

    def hit(self, posy_paddle):
        
        if self.posy + self.radius <= posy_paddle + self.height / 2:
            self.hitonpaddle = (self.posy - posy_paddle)/self.height
            print(self.hitonpaddle)

        if self.posy + self.radius >= posy_paddle + self.height / 2:
            self.hitonpaddle = (posy_paddle + self.height - self.posy)/self.height
            print(self.hitonpaddle)
            
        if self.speedx < MAX_SPEED:  # Define MAX_SPEED, e.g., MAX_SPEED = 15
            self.speedx += random.random() * 0.5
        else:
            self.speedx -= random.random() * 0.5
        
        if self.speedy < MAX_SPEED:  # Define MAX_SPEED, e.g., MAX_SPEED = 15
            self.speedy += random.random() * 0.5
        else:
            self.speedy -= random.random() * 0.5
        self.xFac *= -1

    def getRect(self):
        return self.ball
    
class main_option:
    def __init__(self):
        self.yes = 1

    def displaymain(self, text, x, y, color):
        text = font200.render(text, True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)

class Bar():
    def __init__(self, posx, posy, width, height, max):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.max = max

    def extend_the_bar(self):
        if self.width <= self.max:
            self.width += 3
        Bar = pygame.Rect(self.posx, self.posy, self.width, self.height)
        pygame.draw.rect(screen, WHITE, Bar)
    def reset_bar(self):
        self.width = 0

def WINNER(Player):
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        text = font50.render("The Winner is "+Player, True, WHITE)
        textRect = text.get_rect()
        textRect.center = (WIDTH//2, HEIGHT//2)
        screen.blit(text, textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = False

        pygame.display.update()


def Gameplay():
    running = True

    player1 = Paddle(20, 0, 15, 200, WHITE)
    player2 = Paddle(WIDTH-30, 0, 15, 1080, WHITE)
    ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE, 200)

    listOfPlayer = [player1, player2]

    last_value1, last_value2 = 0, 0
    
    player1score, player2score = 0, 0
    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
		
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            data = data.strip('()')

            value1, value2 = data.split(',')
            value1 = float(value1)
            value2 = float(value2)

            player1.update(value1)
            player2.update(value2)

            last_value1, last_value2 = value1, value2
        else:
            player1.update(last_value1)
            player2.update(last_value2)
        
        for player in listOfPlayer:
            if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                ball.hit(player.posy)

        point = ball.update()

        if point == -1:
            player1score += 1
        elif point == 1:
            player2score += 1

        if point:
            ball.reset()

        player1.display()
        player2.display()
        ball.display()

        player1.displayScore("Player_1 : ", player1score, 400, 50, WHITE)
        player2.displayScore("Player_2 : ", player2score, WIDTH-400, 50, WHITE)

        if player1score == MATCH_POINT:
            WINNER("player_1")
            running = False
        elif player2score == MATCH_POINT:
            WINNER("player_2")
            running = False
        
        pygame.display.update()

def Setting():
    running = True
    Menu_cursor = main_option()
    player = Paddle(20, 0, 15, 200, WHITE)
    last_value1 = 0

    Bar1 = Bar(55, 370, 0, 30, 1400)
    Bar2 = Bar(55, 675, 0, 30, 565)

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        Menu_cursor.displaymain("MATCH POINT", 750, 300, WHITE)
        Menu_cursor.displaymain("BACK", 330, 600, WHITE)

        if player.posy >= 150 and player.posy <= 250:
            Bar1.extend_the_bar()
        else:
            Bar1.reset_bar()

        if player.posy >= 410 and player.posy <= 550:
            Bar2.extend_the_bar()
        else:
            Bar2.reset_bar()

        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            data = data.strip('()')

            value1, value2 = data.split(',')
            value1 = float(value1)
            value2 = float(value2)

            player.update(value1)

            last_value1 = value1
        else:
            player.update(last_value1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and player.posy >= 150 and player.posy <=250:
                    Matchpoint()
                if event.key == pygame.K_p and player.posy >= 410 and player.posy <=550:
                    running = False
        player.display()
        pygame.display.update()

def Matchpoint():
    running = True
    Menu_cursor = main_option()
    player = Paddle(20, 0, 15, 200, WHITE)
    last_value1 = 0
    
    global MATCH_POINT

    Bar1 = Bar(55, 970, 0, 30, 565)

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)

        str_MATCH_POINT = MATCH_POINT
        Menu_cursor.displaymain(str(str_MATCH_POINT), 220, 395, WHITE)
        Menu_cursor.displaymain("BACK", 330, 900, WHITE)

        if player.posy >= 750 and player.posy <=850:
            Bar1.extend_the_bar()
        else:
            Bar1.reset_bar()

        if player.posy >= 30 and player.posy <=140:
            pygame.draw.polygon(screen, WHITE, [(220, 80), (140, 270), (300, 270)])
            pygame.draw.polygon(screen, BLACK, [(220, 90), (150, 260), (290, 260)])
        
        if player.posy >= 430 and player.posy <=540:
            pygame.draw.polygon(screen, WHITE, [(220, 670), (140, 480), (300, 480)])
            pygame.draw.polygon(screen, BLACK, [(220, 660), (150, 490), (290, 490)])

        pygame.draw.polygon(screen, WHITE, [(220, 100), (160, 250), (280, 250)])
        pygame.draw.polygon(screen, WHITE, [(220, 650), (160, 500), (280, 500)])

        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            data = data.strip('()')

            value1, value2 = data.split(',')
            value1 = float(value1)
            value2 = float(value2)

            player.update(value1)

            last_value1 = value1
        else:
            player.update(last_value1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and player.posy >= 30 and player.posy <=140 and MATCH_POINT < 100:
                    MATCH_POINT += 1
                if event.key == pygame.K_p and player.posy >= 430 and player.posy <=540 and MATCH_POINT > 1:
                    MATCH_POINT -= 1
                if event.key == pygame.K_p and player.posy >= 750 and player.posy <=850:
                    running = False
        player.display()
        pygame.display.update()

def main():
    running = True
    Menu_cursor = main_option()
    player = Paddle(20, 0, 15, 200, WHITE)
    last_value1 = 0

    Bar1 = Bar(55, 370, 0, 30, 570)
    Bar2 = Bar(55, 675, 0, 30, 1010)
    Bar3 = Bar(55, 975, 0, 30, 487)

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        Menu_cursor.displaymain("PONG", 340, 300, WHITE)
        Menu_cursor.displaymain("SETTINGS", 560, 600, WHITE)
        Menu_cursor.displaymain("QUIT", 290, 900, WHITE)

        if player.posy >= 150 and player.posy <= 250:
            Bar1.extend_the_bar()
        else:
            Bar1.reset_bar()

        if player.posy >= 410 and player.posy <= 550:
            Bar2.extend_the_bar()
        else:
            Bar2.reset_bar()

        if player.posy >= 750 and player.posy <= 850:
            Bar3.extend_the_bar()
        else:
            Bar3.reset_bar()
        
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            data = data.strip('()')

            value1, value2 = data.split(',')
            value1 = float(value1)
            value2 = float(value2)

            player.update(value1)

            last_value1 = value1
        else:
            player.update(last_value1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and player.posy >= 150 and player.posy <= 250:
                    Gameplay()
                if event.key == pygame.K_p and player.posy >= 410 and player.posy <= 550:
                    Setting()
                if event.key == pygame.K_p and player.posy >= 750 and player.posy <= 850:
                    running = False

        player.display()
        pygame.display.update()



if __name__ == "__main__":
	main()
	pygame.quit()