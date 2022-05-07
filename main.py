import pygame
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1v1 spaceship battle")

white = (255, 255, 255)
blue = (0, 100, 255)
black = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

border = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('comicsans', 25)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

spaceship_width, spaceship_height = 55, 40
velocity = 5
bullet_vel = 7
bullet_max = 3

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

yellow_spaceship_image = pygame.image.load('spaceship_yellow.png')
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_image, (spaceship_width, spaceship_height)), 90)

red_spaceship_image = pygame.image.load('spaceship_red.png')
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship_image, (spaceship_width, spaceship_height)), 270)

space = pygame.transform.scale(pygame.image.load('space.png'), (WIDTH,HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WINDOW.blit(space, (0, 0))
    pygame.draw.rect(WINDOW, black, border)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, white)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, white)

    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    WINDOW.blit(yellow_spaceship, (yellow.x, yellow.y))
    WINDOW.blit(red_spaceship, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)
    pygame.display.update()

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - velocity > 0:
        yellow.x -= velocity
    if keys_pressed[pygame.K_d] and yellow.x + velocity + yellow.width < border.x:
        yellow.x += velocity
    if keys_pressed[pygame.K_w] and yellow.y - velocity > 0:
        yellow.y -= velocity
    if keys_pressed[pygame.K_s] and yellow.y + velocity + yellow.height < HEIGHT - 15:
        yellow.y += velocity

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - velocity > border.x + border.width:
        red.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and red.x + velocity + red.width < WIDTH:
        red.x += velocity
    if keys_pressed[pygame.K_UP] and red.y - velocity > 0:
        red.y -= velocity
    if keys_pressed[pygame.K_DOWN] and red.y + velocity + red.height < HEIGHT - 15:
        red.y += velocity

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, white)
    WINDOW.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():

    red = pygame.Rect(700, 300, spaceship_width, spaceship_height)
    yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)

    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < bullet_max:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10 , 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < bullet_max:
                    bullet = pygame.Rect(red.x, red.y + red.height// 2 - 2, 10, 5)
                    red_bullets.append(bullet)
            if event.type == red_hit:
                red_health -= 1
            if event.type == yellow_hit:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()