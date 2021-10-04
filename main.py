import pygame, sys, random

WIDTH = 360
HEIGHT = 640
FPS = 120
TEXT_COLOR = (255,255,255)


pygame.init()
pygame.display.set_caption('FLAPPY BIRD') 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font('04B_19.ttf',28)
font_small = pygame.font.Font('04B_19.ttf',19)
clock = pygame.time.Clock()


# background 
bg_img = pygame.image.load('images/background.png').convert()
bg_surface = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# base
base_img = pygame.image.load('images/base.png').convert_alpha()
base_surface = pygame.transform.scale(base_img, (WIDTH, WIDTH//3))

# pipes
pipe_surface = pygame.image.load('images/pipe.png').convert_alpha()
flip_pipe_surface = pygame.transform.flip(pipe_surface, False, True)

# game over
game_over_surface = pygame.image.load('images/gameover.png').convert_alpha()

# bird
bird_1 = pygame.transform.scale(pygame.image.load('images/bird-downflap.png').convert_alpha(), (54, 40))
bird_2 = pygame.transform.scale(pygame.image.load('images/bird-midflap.png').convert_alpha(), (54, 40))
bird_3 = pygame.transform.scale(pygame.image.load('images/bird-upflap.png').convert_alpha(), (54, 40))

# sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
die_sound = pygame.mixer.Sound('sound/sfx_die.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

# flapping effect
BIRD_FLAP = pygame.USEREVENT
pygame.time.set_timer(BIRD_FLAP, 200)

class Bird():
    def __init__(self):
        self.idx = 0
        self.frames = [bird_1, bird_2, bird_3]
        self.gravity = 0.25
        self.movement = 0
        self.y = 250
        self.bird_surface = None
        self.bird_rect = None
          
    def draw_bird(self):
        self.bird_surface = pygame.transform.rotozoom(self.frames[self.idx], -self.movement*3, 1)
        self.bird_rect = self.bird_surface.get_rect(topleft=(70, self.y))
        screen.blit(self.bird_surface, self.bird_rect)

    def fly_up(self):
        self.movement = 0
        self.movement -= 6
        flap_sound.play()

    def fall_down(self):
        self.movement += self.gravity
        self.y += self.movement 
           
    def check_collision(self, pipes):
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe.top_pipe) or self.bird_rect.colliderect(pipe.bottom_pipe):
                hit_sound.play()
                die_sound.play()
                return True
        
        if self.y <= 0 or self.y >= HEIGHT - base_surface.get_height() - self.bird_surface.get_height():
            hit_sound.play()
            die_sound.play()
            return True

        return False
    
    def reset(self):
        self.movement = 0
        self.y = 250



class Pipe():
    def __init__(self):
        self.gap = 160
        self.pos = random.choice([340, 380, 270, 305])
        self.bottom_pipe = pipe_surface.get_rect(midtop=(WIDTH + 30, self.pos))
        self.top_pipe = pipe_surface.get_rect(midbottom=(WIDTH + 30, self.pos - self.gap))
    
    def draw_pipes(self):        
        screen.blit(flip_pipe_surface, self.top_pipe)
        screen.blit(pipe_surface, self.bottom_pipe)
    
    def move_pipes(self, speed):
        self.bottom_pipe.centerx -= (speed + 2)
        self.top_pipe.centerx -= (speed + 2)



def draw_base(base_x):
    base_surface_rect_1 = base_surface.get_rect(bottomleft=(base_x, HEIGHT)) 
    screen.blit(base_surface, base_surface_rect_1)
    base_surface_rect_2 = base_surface.get_rect(bottomleft=(base_x + WIDTH, HEIGHT))
    screen.blit(base_surface, base_surface_rect_2)


def draw_score(score):
    score_surface = font.render('Score: ' + str(score), True, TEXT_COLOR)
    score_rect = score_surface.get_rect(center = (WIDTH//2, 55))
    screen.blit(score_surface, score_rect)

def draw_text(game_over):
    text_surface = font_small.render('Press up arrow to play.', True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center = (WIDTH//2, HEIGHT//2))
    screen.blit(text_surface, text_rect)
    if game_over:
        game_over_surface_rect = game_over_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
        screen.blit(game_over_surface, game_over_surface_rect)

def main():
    running = False
    base_x_pos = 0
    speed = 1
    pipe_list = [Pipe()]
    remove_list = []
    bird = Bird()
    game_over = False
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not running:
                    game_over = False
                    pipe_list = [Pipe()]
                    speed = 1
                    remove_list = []
                    bird.reset()
                    score = 0
                    running = True

                if event.key == pygame.K_UP and running:
                    bird.fly_up()
                
            if event.type == BIRD_FLAP:
                if not game_over:
                    if bird.idx == 2:
                        bird.idx = 0
                    else:
                        bird.idx += 1
                

           
                
        screen.blit(bg_surface, (0,0))

        if running:

            if len(pipe_list) > 0 and pipe_list[-1].top_pipe.centerx <= WIDTH//4:
                pipe_list.append(Pipe())
                score_sound.play()
                score += 1
           
            
            for pipe in pipe_list:
                pipe.move_pipes(speed)
                if pipe.top_pipe.centerx <= -WIDTH:
                    remove_list.append(pipe)
                
            
            for pipe in remove_list:
                pipe_list.remove(pipe)
            
            remove_list.clear()

            # move base
            if base_x_pos <= -WIDTH:
                base_x_pos = 0
            else:
                base_x_pos -= speed
            
            bird.fall_down()

            if bird.check_collision(pipe_list):
                game_over = True
                running = False
            
            if (score == 10 and speed == 1) or (score == 20 and speed == 2):
                speed += 1
        

        for pipe in pipe_list:
            pipe.draw_pipes()    

        draw_base(base_x_pos)

        bird.draw_bird()

        draw_score(score)

        if not running:
            draw_text(game_over)

        if game_over:
            if bird.y < HEIGHT - base_surface.get_height() - bird.bird_surface.get_height()/2:
                bird.movement += bird.gravity
                bird.y += bird.movement
            

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()