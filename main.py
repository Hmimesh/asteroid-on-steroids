import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
import sys
from shot import *
from power_up import PowerUp
import random

updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()
power_ups = pygame.sprite.Group()

Player.containers = (updatable, drawable)
Asteroid.containers =(asteroids, updatable, drawable)
AsteroidField.containers =(updatable,)
Shot.containers = (updatable, drawable, shots)
PowerUp.containers = (updatable, drawable, power_ups)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_fields = AsteroidField()
    power_up_timer = 0
    power_up_spawn_interval = random.randrange(5, 15)

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill((0, 0, 0,))

        power_up_timer += dt

        if power_up_timer >= power_up_spawn_interval:
            print(f"Spawning power-up at {dt:.2f} seconds")
            PowerUp(SCREEN_WIDTH, SCREEN_HEIGHT)
            power_up_timer = 0
            power_up_spawn_interval = random.randrange(5, 15)
        
        for thing in updatable:
            thing.update(dt)
            for power_up in power_ups:
                if player.collides_with(power_up):
                    player.activate_mega_lazer()
                    print(f"{power_up} collected!")
                    power_up.kill()
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    print("GAME OVER!")
                    sys.exit()
                for shot in shots:
                    if asteroid.collides_with(shot):
                        asteroid.kill()
            for power_up in power_ups:
                if power_up.is_off_screen(SCREEN_HEIGHT):
                    power_up.kill()
        for thing in drawable:
            thing.draw(screen)
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        
    
    

    
    pygame.quit()

if __name__ == "__main__":
    main()