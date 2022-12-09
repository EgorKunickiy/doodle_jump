import random
import tkinter as tk
from types import SimpleNamespace

WIDTH = 800
HEIGHT = 600

# player physics
GRAVITY = 0.33
DRAG = 0.3
BOUNCE_VELOCITY = -12.5

w = tk.Tk()
w.geometry(f"{WIDTH}x{HEIGHT}")
w.title('Doodle Jump')
canvas = tk.Canvas(w, height=HEIGHT, width=WIDTH)
canvas.create_text(50, 100, text="Hello METANIT.COM", fill="#004D40")
canvas.place(x=0, y=0, relwidth=1, relheight=1)
person = tk.PhotoImage(file='underwater-right@2x.png')
green_platform = tk.PhotoImage(file='greenplatform.png')


# width and height of each platform and where platforms start
platform_width = 64
platform_height = 20
platform_start = HEIGHT - 50

# minimum and maximum vertical space between each platform
min_platform_space = 15
max_platform_space = 20

# information about each platform. the first platform starts in the
# bottom middle of the screen
platforms = [SimpleNamespace(
    x=WIDTH / 2 - platform_width / 2,
    y=platform_start
)]

#  fill the initial screen with platforms
y = platform_start
while y > 0:
    # the next platform can be placed above the previous one with a space
    # somewhere between the min and max space
    y -= platform_height + random.uniform(min_platform_space, max_platform_space)
    # a platform can be placed anywhere 25px from the left edge of the canvas
    # and 25px from the right edge of the canvas (taking into account platform
    # width).
    # however the first few platforms cannot be placed in the center so
    # that the player will bounce up and down without going up the screen
    # until they are ready to move
    x = None
    while True:
        x = random.uniform(25, WIDTH - 25 - platform_width)
        if not (y > HEIGHT / 2 and WIDTH / 2 - platform_width * 1.5 < x < WIDTH / 2 + platform_width / 2):
            break

    platforms.append(SimpleNamespace(x=x, y=y))

# the doodle jumper
DOODLE = SimpleNamespace(
    width=40,
    height=60,
    x=WIDTH / 2 - 20,
    y=platform_start - 60,
    # velocity
    dx=0,
    dy=0
)
#
# keep track of player direction and actions
playerDir = 0
key_down = False
prevDoodleY = DOODLE.y


# game loop
def loop():
    global min_platform_space, max_platform_space, playerDir, platforms, prevDoodleY
    # 17 is 1000//60
    canvas.after(17, loop)

    canvas.delete("all")

    # apply GRAVITY to doodle
    DOODLE.dy += GRAVITY
    #     if doodle reaches the middle of the screen, move the platforms down
    #     instead of doodle up to make it look like doodle is going up
    if DOODLE.y < HEIGHT / 2 and DOODLE.dy < 0:
        for platform in platforms:
            platform.y -= DOODLE.dy
        #
        #       add more platforms to the top of the screen as doodle moves up
        while platforms[len(platforms) - 1].y > 0:
            platforms.append(SimpleNamespace(
                x=random.uniform(25, WIDTH - 25 - platform_width),
                y=platforms[len(platforms) - 1].y - (platform_height + random.uniform(min_platform_space, max_platform_space)
                                                     )))
            #         add a bit to the min/max platform space as the player goes up
            min_platform_space += 0.5
            max_platform_space += 0.5
            #         cap max space
            max_platform_space = min(max_platform_space, HEIGHT / 2)
    else:
        DOODLE.y += DOODLE.dy

    #     only apply DRAG to horizontal movement if key is not pressed
    if not key_down:
        if playerDir < 0:
            DOODLE.dx += DRAG
            #          don't let dx go above 0
            if DOODLE.dx > 0:
                DOODLE.dx = 0
                playerDir = 0
        elif playerDir > 0:
            DOODLE.dx -= DRAG

            if DOODLE.dx < 0:
                DOODLE.dx = 0
                playerDir = 0

    DOODLE.x += DOODLE.dx
    #   make doodle wrap the screen
    if DOODLE.x + DOODLE.width < 0:
        DOODLE.x = WIDTH
    elif DOODLE.x > WIDTH:
        DOODLE.x = -DOODLE.width

    #     draw platforms
    for platform in platforms:
        canvas.create_image(int(platform.x), platform.y, image=green_platform)

    for platform in platforms:
        # make doodle jump if it collides with a platform from above
        # doodle is falling
        # doodle was previous above the platform
        # doodle collides with platform
        if DOODLE.dy > 0 and \
                prevDoodleY + DOODLE.height <= platform.y and \
                DOODLE.x < platform.x + platform_width and \
                DOODLE.x + DOODLE.width > platform.x and \
                DOODLE.y < platform.y + platform_height and \
                DOODLE.y + DOODLE.height > platform.y:
            # reset doodle position, so it's on top of the platform
            DOODLE.y = platform.y - DOODLE.height
            DOODLE.dy = BOUNCE_VELOCITY

    # draw doodle
    canvas.create_image(DOODLE.x, DOODLE.y, image=person)

    prevDoodleY = DOODLE.y
    #    remove any platforms that have gone off-screen
    platforms = [platform for platform in platforms if platform.y < HEIGHT]

    if DOODLE.y > HEIGHT:
        canvas.quit()


def handle_key_press(e):
    global key_down, playerDir
    if e.keysym == "d":
        key_down = True
        playerDir = -1
        DOODLE.dx = 3
    elif e.keysym == "a":
        key_down = True
        playerDir = 1
        DOODLE.dx = -3


def handle_key_release(e):
    global key_down
    key_down = False


if __name__ =='__main__':
    # Tkinter reacts to holding key as key repeating same with canvas
    # so use canvas' But that's not a problem her
    w.bind("<KeyPress>", handle_key_press)
    w.bind("<KeyRelease>", handle_key_release)

    # for 60 FPS
    canvas.after(17, loop)  # 17 is 1000//60
    w.mainloop()