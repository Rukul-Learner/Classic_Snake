import pygame, random, sys
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(1,0)
        self.new_block=False

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

    def drawSnake(self):
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
        # for block in self.body:
        #     xpos=int(block.x*cell_size)
        #     ypos=int(block.y*cell_size)
        #     block_rect=pygame.Rect(xpos,ypos,cell_size,cell_size)

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


class Fruit:
    def __init__(self):
        self.randomise()

    def drawFruit(self):
        fruit_rect=pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        #pygame.draw.rect(screen,(126,166,144),fruit_rect)

    def randomise(self):
        self.x=random.randint(0,cell_number-1)
        self.y=random.randint(0,cell_number-1)
        self.pos=Vector2(self.x,self.y)

class Main:
    def __init__(self):
        self.snake=Snake()
        self.fruit=Fruit()

    def update(self):
        self.snake.moveSnake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.drawFruit()
        self.snake.drawSnake()

    def check_collision(self):
        if self.fruit.pos== self.snake.body[0]:
            self.fruit.randomise()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number:
            self.gameOver()
        if not 0 <= self.snake.body[0].y < cell_number:
            self.gameOver()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()

    def gameOver(self):
        pygame.quit()

pygame.init()
cell_size=40
cell_number=20

screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size),0,32)
pygame.display.set_caption("Snake")

apple=pygame.image.load('Graphics/apple2.png').convert_alpha()

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
