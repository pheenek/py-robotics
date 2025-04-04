import pygame

# Arm parameters (lengths of the two arm segments)
L1 = 10  # Length of first arm link
L2 = 10  # Length of second arm link

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # pygame.event.pump()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    pygame.draw.circle(screen, "red", player_pos, 40)

    # Check for key events
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:  # Move left (decrease x)
        player_pos.x -= 300 * dt
        print("left")
    if keys[pygame.K_RIGHT]:  # Move right (increase x)
        player_pos.x += 300 * dt
        print("right")
    if keys[pygame.K_UP]:  # Move up (increase y)
        player_pos.y -= 300 * dt
        print("up")
    if keys[pygame.K_DOWN]:  # Move down (decrease y)
        player_pos.y += 300 * dt
        print("down")
    if keys[pygame.K_x]:
        print("quit")
        running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    
# Close pygame when done
pygame.quit()


# Example file showing a circle moving on screen
# import pygame

# # pygame setup
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True
# dt = 0

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # fill the screen with a color to wipe away anything from last frame
#     screen.fill("purple")

#     pygame.draw.circle(screen, "red", player_pos, 40)

#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_w]:
#         player_pos.y -= 300 * dt
#     if keys[pygame.K_s]:
#         player_pos.y += 300 * dt
#     if keys[pygame.K_a]:
#         player_pos.x -= 300 * dt
#     if keys[pygame.K_d]:
#         player_pos.x += 300 * dt

#     # flip() the display to put your work on screen
#     pygame.display.flip()

#     # limits FPS to 60
#     # dt is delta time in seconds since last frame, used for framerate-
#     # independent physics.
#     dt = clock.tick(60) / 1000

# pygame.quit()
