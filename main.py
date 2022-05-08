import pygame
import random
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1v1 spaceship battle")

#colours
white = (255, 255, 255)
blue = (0, 100, 255)
black = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#border
border = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
#fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 25)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

spaceship_width, spaceship_height = 55, 40

#user events
yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2
yorb_hit = pygame.USEREVENT + 3
rorb_hit = pygame.USEREVENT + 4

#images
yellow_spaceship_image = pygame.image.load('spaceship_yellow.png')
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_image, (spaceship_width, spaceship_height)), 90)

red_spaceship_image = pygame.image.load('spaceship_red.png')
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship_image, (spaceship_width, spaceship_height)), 270)

space = pygame.transform.scale(pygame.image.load('space.png'), (WIDTH,HEIGHT))

ENERGY_ORB = pygame.transform.scale(pygame.image.load('energy_orb.png'), (40, 40))

#draws the window and everything inside it every frame
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_powerup, yellow_powerup, energy_orbs):
    WINDOW.blit(space, (0, 0))
    pygame.draw.rect(WINDOW, black, border)

    #renders the text on screen
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, white)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, white)
    red_powerup_text = HEALTH_FONT.render("Latest Powerup: " + red_powerup, 1, white)
    yellow_powerup_text = HEALTH_FONT.render("Latest Powerup: " + yellow_powerup, 1, white)

    #draws the text on screen
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))
    WINDOW.blit(red_powerup_text, (WIDTH - red_powerup_text.get_width() - 10, 35))
    WINDOW.blit(yellow_powerup_text, (10, 35))

    #draws spaceship
    WINDOW.blit(yellow_spaceship, (yellow.x, yellow.y))
    WINDOW.blit(red_spaceship, (red.x, red.y))

    #draws every red bullet on screen
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    #draws every yellow bullet on screen
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    #draws every power up on screen
    for energy_orb in energy_orbs:
        WINDOW.blit(ENERGY_ORB, (energy_orb.x, energy_orb.y))

    pygame.display.update()

#moves yellow spaceship
def yellow_movement(keys_pressed, yellow, yvelocity):
    #move left
    if keys_pressed[pygame.K_a] and yellow.x - yvelocity > 0:
        yellow.x -= yvelocity
    #move right
    if keys_pressed[pygame.K_d] and yellow.x + yvelocity + yellow.width < border.x:
        yellow.x += yvelocity
    #moves up
    if keys_pressed[pygame.K_w] and yellow.y - yvelocity > 0:
        yellow.y -= yvelocity
    #moves down
    if keys_pressed[pygame.K_s] and yellow.y + yvelocity + yellow.width < HEIGHT:
        yellow.y += yvelocity

#moves red spaceship
def red_movement(keys_pressed, red, rvelocity):
    #move left
    if keys_pressed[pygame.K_LEFT] and red.x - rvelocity > border.x + border.width:
        red.x -= rvelocity
    #move right
    if keys_pressed[pygame.K_RIGHT] and red.x + rvelocity + red.width < WIDTH:
        red.x += rvelocity
    #move up
    if keys_pressed[pygame.K_UP] and red.y - rvelocity > 0:
        red.y -= rvelocity
    #move down
    if keys_pressed[pygame.K_DOWN] and red.y + rvelocity + red.height < HEIGHT - 15:
        red.y += rvelocity

#moves bullets and looks at bullet interactions
def handle_bullets(yellow_bullets, red_bullets, yellow, red, ybullet_vel, rbullet_vel):
    #checks if yellow bullet hits red player or goes out of bounds
    for bullet in yellow_bullets:
        bullet.x += ybullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    #checks if red bullet hits yellow player or goes out of bounds
    for bullet in red_bullets:
        bullet.x -= rbullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

    #checks if a red bullet and a yellow bullet collide
    for ybullet in yellow_bullets:
        for rbullet in red_bullets:
            if ybullet.colliderect(rbullet):
                yellow_bullets.remove(ybullet)
                red_bullets.remove(rbullet)

#handles power up orbs and its interactions
def handle_energyorb(yellow, red, energy_orbs):
    for energy_orb in energy_orbs:
        #if red touches orb
        if red.colliderect(energy_orb):
            pygame.event.post(pygame.event.Event(rorb_hit))
            energy_orbs.remove(energy_orb)
        #if yellow touches orb
        elif yellow.colliderect(energy_orb):
            pygame.event.post(pygame.event.Event(yorb_hit))
            energy_orbs.remove(energy_orb)

#draws the winner text when a winner is found
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, white)
    WINDOW.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

#main function that runs the program
def main():
    red = pygame.Rect(700, 300, spaceship_width, spaceship_height)
    yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)
    red_bullets = []
    yellow_bullets = []
    energy_orbs = []
    timer = 0
    red_powerup = "none"
    yellow_powerup = "none"
    red_health = 10
    yellow_health = 10
    #values for each spaceship that are changed through powerups
    rvelocity = 5
    yvelocity = 5
    rbullet_vel = 7
    ybullet_vel = 7
    rbullet_max = 3
    ybullet_max = 3
    clock = pygame.time.Clock()
    run = True
    while run:
        #60 fps
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            #timer for power ups to appear
            timer += 1
            if timer % 100 == 0:
                energy_orb = pygame.Rect(random.randint(0, 900), random.randint(0,500), 30, 30)
                energy_orbs.append(energy_orb)
            #makes sure that max bullets are not exceeded for each colour
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < ybullet_max:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10 , 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < rbullet_max:
                    bullet = pygame.Rect(red.x, red.y + red.height// 2 - 2, 10, 5)
                    red_bullets.append(bullet)
            #if red spaceship is hit
            if event.type == red_hit:
                red_health -= 1
            #if yellow spaceship is hit
            if event.type == yellow_hit:
                yellow_health -= 1
            #if red spaceship hits a powerup
            if event.type == rorb_hit:
                power = random.randint(1, 4)
                if power == 1:
                    red_powerup = "Faster Bullets"
                    rbullet_vel += 1
                elif power == 2:
                    red_powerup = "More Bullets"
                    rbullet_max += 1
                elif power == 3:
                    red_powerup = "Faster Spaceship"
                    rvelocity += 1
            #if yellow spaceship hits a powerup
            if event.type == yorb_hit:
                power = random.randint(1, 4)
                if power == 1:
                    yellow_powerup = "Faster Bullets"
                    ybullet_vel += 1
                elif power == 2:
                    yellow_powerup = "More Bullets"
                    ybullet_max += 1
                elif power == 3:
                    yellow_powerup = "Faster Spaceship"
                    yvelocity += 1

        #checks if a winner is found
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            timer = 0
            break

        #calling methods for game to run
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow, yvelocity)
        red_movement(keys_pressed, red, rvelocity)
        handle_bullets(yellow_bullets, red_bullets, yellow, red, ybullet_vel, rbullet_vel)
        handle_energyorb(yellow, red, energy_orbs)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_powerup, yellow_powerup, energy_orbs)

    main()

if __name__ == "__main__":
    main()