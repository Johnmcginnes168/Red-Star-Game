######################
#
#   Import Libraries
#
######################

import pgzrun          
import random          

######################
#
#   Initialize Actors and Variables
#
######################

# Constant values
FONT_COLOR = (255, 255, 255)    # White text color
WIDTH = 800                     # Width of game window
HEIGHT = 600                    # Height of game window
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y)
FINAL_LEVEL = 6                 # Last level of the game
START_SPEED = 10               # Base duration for star animations (lower = faster)
COLORS = ['green', "blue"]     # Non-red colors for decoy stars

# Game state variables
game_over = False
game_complete = False
current_level = 1
stars = []                     # List to store current stars on screen
animations = []                # List to keep track of active animations

######################
#
#   Main Drawing Function
#
######################

def draw():
    """Draw the game screen depending on game state."""
    global stars, current_level, game_over, game_complete
    screen.clear()
    screen.blit("space", (0, 0))  # Background image

    if game_over:
        # Show game over screen
        display_message("GAME OVER!", "Press the Space Bar to Try Again.")
    elif game_complete:
        # Show game win screen
        display_message("YOU WON!", "Well done! Press the Space Bar to Try Again.")
    else:
        # Draw all stars
        for star in stars:
            star.draw()

######################
#
#   Game Functions
#
######################

def update():
    """Update the game state each frame."""
    global stars, game_complete, game_over, current_level

    # If no stars are on screen, generate stars for current level
    if len(stars) == 0:
        stars = make_stars(current_level)

    # Restart game if it's over or completed and space bar is pressed
    if (game_complete or game_over) and keyboard.space:
        stars = []
        current_level = 1
        game_complete = False
        game_over = False

def make_stars(number_of_extra_stars):
    """Create a list of stars with one red and some decoys."""
    colors_to_create = get_colors_to_create(number_of_extra_stars)
    new_stars = create_stars(colors_to_create)
    layout_stars(new_stars)
    animate_stars(new_stars)
    return new_stars

def get_colors_to_create(number_of_extra_stars):
    """Return a list with one red star and a number of random colored decoys."""
    colors_to_create = ["red"]
    for i in range(0, number_of_extra_stars):
        random_color = random.choice(COLORS)
        colors_to_create.append(random_color)
    return colors_to_create

def create_stars(colors_to_create):
    """Create Actor objects from the list of colors."""
    new_stars = []
    for color in colors_to_create:
        star = Actor(color + "-star")
        new_stars.append(star)
    return new_stars

def layout_stars(stars_to_layout):
    """Position the stars horizontally across the screen."""
    number_of_gaps = len(stars_to_layout) + 1
    gap_size = WIDTH / number_of_gaps
    random.shuffle(stars_to_layout)  # Randomize their order

    for index, star in enumerate(stars_to_layout):
        new_x_pos = (index + 1) * gap_size
        star.x = new_x_pos

def animate_stars(stars_to_animate):
    """Animate the stars falling from top to bottom."""
    for star in stars_to_animate:
        duration = START_SPEED - current_level  # Speed up with each level
        star.anchor = ("center", "bottom")
        animation = animate(star, duration=duration, on_finished=handle_game_over, y=HEIGHT)
        animations.append(animation)

def handle_game_over():
    """Trigger game over state if star animation finishes."""
    global game_over
    game_over = True

def on_mouse_down(pos):
    """Handle mouse click events."""
    global stars, current_level
    for star in stars:
        if star.collidepoint(pos):  # Check if a star was clicked
            if "red" in star.image:
                red_star_click()
            else:
                handle_game_over()

def red_star_click():
    """Handle logic for successfully clicking the red star."""
    global current_level, stars, animations, game_complete
    stop_animations(animations)

    if current_level == FINAL_LEVEL:
        game_complete = True
    else:
        current_level += 1
        stars = []
        animations = []

def stop_animations(animations_to_stop):
    """Stop all active star animations."""
    for animation in animations_to_stop:
        if animation.running:
            animation.stop()

def display_message(heading_text, sub_heading_text):
    """Display centered text messages on the screen."""
    screen.draw.text(heading_text, fontsize=60, center=CENTER, color=FONT_COLOR)
    screen.draw.text(sub_heading_text,
                     fontsize=30,
                     center=(CENTER_X, CENTER_Y + 30),
                     color=FONT_COLOR)

# Start the game loop
pgzrun.go()
