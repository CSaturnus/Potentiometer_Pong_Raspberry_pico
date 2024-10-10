import pygame
import serial

pygame.init()
font20 = pygame.font.Font('freesansbold.ttf', 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pong")

clock = pygame.time.Clock()
FPS = 60

ser = serial.Serial('COM12', 115200, timeout=1)

class Striker:
    def __init__(self, posx, posy, width, height, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.color = color
        #player rectangle pong
        self.playerRect = pygame.Rect(posx, posy, width, height)
        #object that will be drawn on the screen
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)
    def display(self):
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)
    
    def update(self, Value):
        self.posy = Value
        self.playerRect = (self.posx, self.posy, self.width, self.height)
    def displayScore(self, text, score, x, y, color):
        text = font20.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)
    
    def getRect(self):
         return self.playerRect

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
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
        self.posx += self.speed*self.xFac
        self.posy += self.speed*self.yFac

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

	# Used to reflect the ball along the X-axis
    def hit(self):
        self.speed += 0.1
        self.xFac *= -1

    def getRect(self):
        return self.ball

# Game Manager




def main():
    running = True

    player1 = Striker(20, 0, 10, 100, GREEN)
    player2 = Striker(WIDTH-30, 0, 10, 100, GREEN)
    ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)

    listOfPlayer = [player1, player2]

    last_value1, last_value2 = 0, 0

    player1score, player2score = 0, 0
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if ser.in_waiting > 0:
            # Try to read the serial data
            
            data = ser.readline().decode('utf-8').strip()
            data = data.strip('()')

            # Split the data and convert to float
            value1, value2 = data.split(',')
            value1 = float(value1)
            value2 = float(value2)

        # Scale the values to fit the screen height (assuming 600 as the maximum Y value)
            value1 = int(value1 * 500)  # Convert to int and scale for player 1
            value2 = int(value2 * 500)  # Convert to int and scale for player 2

        # Store the latest valid values in case of future errors
            last_value1, last_value2 = value1, value2

        else:
            value1, value2 = last_value1, last_value2

        for geek in listOfPlayer:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()
		
        player1.update(value1)
        player2.update(value2)
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

        player1.displayScore("Player_1 : ", player1score, 100, 20, WHITE)
        player2.displayScore("Player_2 : ", player2score, WIDTH-100, 20, WHITE)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
	main()
	pygame.quit()