import pygame, random, sys
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(0,0)
        self.new_block=False

        #Loading Images for snake's movements
        
        self.head_up=pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down=pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right=pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left=pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up=pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down=pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_left=pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.tail_right=pygame.image.load('Graphics/tail_right.png').convert_alpha()

        self.body_vertical=pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal=pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr=pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl=pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br=pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl=pygame.image.load('Graphics/body_bl.png').convert_alpha()

        #Loading Munching Sound
        self.crunch_sound=pygame.mixer.Sound('Sound/crunch.wav')

    def drawSnake(self):
        #calling functions to update the snake graphics
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos=int(block.x * cell_size)
            y_pos=int(block.y * cell_size)
            block_rect=pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block=self.body[index + 1] - block
                next_block=self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x==-1 and next_block.y==-1 or previous_block.y==-1 and next_block.x==-1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x==-1 and next_block.y==1 or previous_block.y==1 and next_block.x==-1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x==1 and next_block.y==-1 or previous_block.y==-1 and next_block.x==1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x==1 and next_block.y==1 or previous_block.y==1 and next_block.x==1:
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation=self.body[1]-self.body[0]
        if head_relation==Vector2(1,0) : self.head = self.head_left
        elif head_relation==Vector2(-1,0) : self.head = self.head_right
        elif head_relation==Vector2(0,1) : self.head = self.head_up
        elif head_relation==Vector2(0,-1) : self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation=self.body[-2]-self.body[-1]
        if tail_relation==Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation==Vector2(1,0): self.tail = self.tail_left
        elif tail_relation==Vector2(0,-1): self.tail = self.tail_down
        elif tail_relation==Vector2(0,1): self.tail = self.tail_up

    def moveSnake(self):
        if self.new_block==True:
            bodyCopy=self.body[:]
            bodyCopy.insert(0,bodyCopy[0] + self.direction)
            self.body=bodyCopy[:]
            self.new_block=False
        else:
            bodyCopy=self.body[:-1]
            bodyCopy.insert(0,bodyCopy[0] + self.direction)
            self.body=bodyCopy[:]

    def add_block(self):
        self.new_block=True

    def reset(self):
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(0,0)

class Fruit:
    def __init__(self):
        self.randomise()

    def drawFruit(self):
        fruit_rect=pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)

    def randomise(self):
        self.x=random.randint(0,cell_number-1)
        self.y=random.randint(0,cell_number-1)
        self.pos=Vector2(self.x,self.y)

class Main:
    def __init__(self):
        self.snake=Snake()
        self.fruit=Fruit()
        pygame.mixer.music.load('Sound/bg_music.mp3')
        pygame.mixer.music.play(-1,1.0)

    def update(self):
        self.snake.moveSnake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.drawFruit()
        self.snake.drawSnake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos== self.snake.body[0]:
            self.fruit.randomise()
            self.snake.add_block()
            self.snake.crunch_sound.play()

        # redraw fruit at different location if it appeared at body of the snake
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomise()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number:
            self.gameOver()
        if not 0 <= self.snake.body[0].y < cell_number:
            self.gameOver()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()

    def gameOver(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            for col in range(cell_number):
                if row%2==0:
                    if col%2==1:
                        grass_rect=pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
                else:
                    if col%2==0:
                        grass_rect=pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score_text= str(len(self.snake.body)-3)
        score_surface= game_font.render(score_text,True,(56,74,12))
        score_x=int(cell_size*cell_number)-60
        score_y=40
        score_rect=score_surface.get_rect(center=(score_x,score_y))
        apple_rect=apple.get_rect(midright=(score_rect.left-2,score_rect.centery))
        bg_rect=pygame.Rect(apple_rect.left-4,apple_rect.top-2,apple_rect.width + 10 + score_rect.width,apple_rect.height+4)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size=40
cell_number=20

screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size),0,32)
pygame.display.set_caption("Snake")

apple=pygame.image.load('Graphics/apple2.png').convert_alpha()
game_font= pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE=pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game=Main()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==SCREEN_UPDATE:
            main_game.update()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                if main_game.snake.direction.y !=1:
                    main_game.snake.direction= Vector2(0,-1)
            if event.key==pygame.K_DOWN:
                if main_game.snake.direction.y !=-1:
                    main_game.snake.direction=Vector2(0,1)
            if event.key==pygame.K_LEFT:
                if main_game.snake.direction.x !=1:
                    main_game.snake.direction=Vector2(-1,0)
            if event.key==pygame.K_RIGHT:
                if main_game.snake.direction.x !=-1:
                    main_game.snake.direction=Vector2(1,0)

    screen.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    pygame.time.Clock().tick(60)
