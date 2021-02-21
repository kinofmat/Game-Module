import arcade
import random
import math

# Royalty free music from https://www.FesliyanStudios.com
# Most images are from kenney.nl, unless otherwise noted.

# This is for initializing the window size, and the title of it.
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Save the World"
MUSIC_VOLUME = 0.8

# Different Scaling sizes, and the starting point of lives and asteroid on this game. 
CHARACTER_SCALING = 0.1
TILE_SCALING = 0.5
ASTEROID_SCALING = 0.5
LIFE_SCALING = 0.02
# These could potentially be changed for different levels to increase difficulty.
ASTEROID_COUNT = 50
START_LIFE = 4
LIFE_RARITY = 5

# This is used multiple times for creating different hearts.
HEART = ":resources:images/items/new_life.png" # This image is from other content I found and added to the resources.

PARTICLE_GRAVITY = 0.05 # The pull of "gravity" on the particles that make their movement pull downwards. If it is 0 then there is no downward pull.
PARTICLE_FADE_RATE = 8 # The rate at which the particles will fade.
# How fast the particle moves. Range is from 2.5 <--> 5 with 2.5 and 2.5 set.
PARTICLE_MIN_SPEED = 2.5
PARTICLE_SPEED_RANGE = 2.5
PARTICLE_COUNT = 10 # The number of particles spawned per explosion.
PARTICLE_RADIUS = 3 # The size of the particles
# The colors that the different particles can appear as.
PARTICLE_COLORS = [arcade.color.ALIZARIN_CRIMSON, arcade.color.COQUELICOT, arcade.color.LAVA, arcade.color.KU_CRIMSON, arcade.color.DARK_TANGERINE]
PARTICLE_SPARKLE_CHANCE = 0.02 # The chance that the particle will turn to white as a sparkle effect.


"""
The start of the main class that runs the game. The functions are default ones that are made to work with arcade.
The arcade.View sets up the class as part of arcade and creates a view, which is like a window.
"""
class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Variables that will hold sprite lists
        self.player_list = None
        self.asteroid_list = None
        self.explosions_list = None
        self.life_list = None
        self.asteroid_hit_list = None
        self.fall_life_list = None

        # Variables that are for a single sprite.
        self.life_sprite = None
        self.player_sprite = None

        self.score = 0

        self.view_bottom = 0
        self.view_left = 0

        self.background = None
        
        # Holds where the sounds are from, and tells the models to expect it.
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.music = arcade.Sound(":resources:music/8-Bit-Surf.mp3", streaming=True)

        self.window.set_mouse_visible(False) # Since the "curser" is the cross hairs we don't want to see the actual mouse curser.

    """
    All the play_song function will do is take the song and play it. 
    It can be written to allow for multiple different songs, but since I don't have any menu screen, I choose to just do one.
    """
    def play_song(self):
        self.current_player = self.music.play(MUSIC_VOLUME)
        
    """
    This function will setup the game. It initializes a lot of the parts of the game needed.
    """
    def setup(self):
        self.score = 0
        self.player_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.life_list = arcade.SpriteList()
        self.asteroid_hit_list = arcade.SpriteList()
        self.fall_life_list = arcade.SpriteList()

        # This image is something I created on my own. I tested it out in a few different colors and added them all to the resources file. Note I also added the cross_hairs folder as well.
        image_source = ":resources:images/animated_characters/cross_hairs/greenaimer.png" 
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        #Position the curser at the center of the screen.
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 400
        self.player_list.append(self.player_sprite)
        self.play_song() # Get the music going!
        self.background = arcade.load_texture(":resources:images/backgrounds/Galaxy.png")

        # Start out with as many lives as is stored in the Start_life constant
        for h in range(START_LIFE):
            life_sprite = Lives(HEART, LIFE_SCALING) # Call the lives class to create a heart.
            """The Lives class by default will make the hearts fall to the bottom of the screen.
            These next two lines of code will override that and set it up as a hear count at the top of the screen."""
            life_sprite.center_x = SCREEN_WIDTH - 30*h - 25
            life_sprite.center_y = SCREEN_HEIGHT - 21
            self.life_list.append(life_sprite)

        # Create as many asteroids as is stored in ASTEROID_COUNT.
        for i in range(ASTEROID_COUNT):
            astrdType = random.randrange(4)
            asteroid = None # Needs to be declared before the if block so that it is not local to the if statement.

            """Uses the randomly generated number to create asteroids of many different types. Some of them 
            are larger and easier to hit, while others are smaller. As a way to add difficulty with levels 
            more of the smaller types of asteroids could be used and less of the bigger types."""
            if astrdType == 1:
                asteroid = Asteroid(":resources:images/space_shooter/meteorGrey_big1.png", ASTEROID_SCALING)
            elif astrdType == 2:
                asteroid = Asteroid(":resources:images/space_shooter/meteorGrey_big2.png", ASTEROID_SCALING)
            elif astrdType == 3:
                asteroid = Asteroid(":resources:images/space_shooter/meteorGrey_big3.png", ASTEROID_SCALING)
            else:
                asteroid = Asteroid(":resources:images/space_shooter/meteorGrey_big4.png", ASTEROID_SCALING)
            # Within the size of the screen randomly place the asteroid.
            asteroid.center_x = random.randrange(SCREEN_WIDTH)
            asteroid.center_y = random.randrange(SCREEN_HEIGHT)
            # Also randomly choose the direction and speed of the asteroid. Sometimes this will end up with them not moving either, since 0 is included.
            asteroid.change_x = random.randrange(-3, 4)
            asteroid.change_y = random.randrange(-3, 4)
            self.asteroid_list.append(asteroid) # Add the asteroid to the list

    """
    This function will draw all of the items added from setup into different sprite lists.
    """
    def on_draw(self):
        # Creates the window and adds the background.
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draws all of the sprites added to these sprite lists.
        self.player_list.draw()
        self.asteroid_list.draw()
        self.explosions_list.draw()
        self.life_list.draw()
        self.fall_life_list.draw()

        # Draw the score onto the screen. In the draw_text, it reminds me of css.
        score_text = "Score: {}".format(self.score)
        arcade.draw_text(score_text, 10 + self.view_left, SCREEN_HEIGHT - 28, arcade.csscolor.WHITE, 18)

    """
    This function will move the cross hairs or "Player Sprite" with the curser, to allow the functionality of the game. 
    """
    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y
    
    """
    Since most of the interactions with the game are done through the mouse this is a little bit of a larger function.
    It has to test if the player missed or hit an asteroid sprite. When there is an asteroid that is hit, there needs
    to be several test conditions met as well.
    """
    def on_mouse_press(self, x, y, button, modifiers):
        #Checks for any asteroid sprites that are underneath the player sprite. If there are, they are added to the asteroid_hit_list.
        asteroid_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)

        #When there are no asteroids hit, remove a life, and play a miss sound. Otherwise play a hit sound.
        if len(asteroid_hit_list) <= 0:
            arcade.play_sound(self.gun_sound)
            if len(self.life_list) > 0:
                self.life_list.pop()
        else:
            arcade.play_sound(self.hit_sound)

        """With each asteroid there is a test for how many points to add, another if a heart should drop, 
        and lastly generate the explosion particles."""
        for asteroid in asteroid_hit_list:
            if len(asteroid_hit_list) > 4:
                self.score += 5
            elif len(asteroid_hit_list) > 2:
                self.score += 2
            else:
                self.score += 1
            # Random number used to create, currently a one in 5 chance of a life drop.
            drop = random.randrange(0, LIFE_RARITY)
            if drop == 1:
                lives = Lives(HEART, LIFE_SCALING)
                lives.position = asteroid.position # Make the life drop right from where the asteroid was.
                self.fall_life_list.append(lives) # Add them all to a Sprite List that can be added in the on_update function.
            # This will create the particles for each asteroid destroyed.
            for i in range(PARTICLE_COUNT):
                particle = Particle(self.explosions_list)
                particle.position = asteroid.position # Just like the hearts, create it where the asteroid was.
                self.explosions_list.append(particle) # Also like the hearts, add this to a list that can be updated.
            asteroid.remove_from_sprite_lists() # Lastly don't forget to remove the asteroid after all the processing is done!

    """
    on_update will update everything about every 0.016 seconds. This allows for the sprites to move fairly seamlessly to the player's eye.
    """
    def on_update(self, delta_time):
        # Make sure the sprites are updated so that they move.
        self.asteroid_list.update()
        self.fall_life_list.update()
        self.explosions_list.update()
        # This is some functional code below too. It makes the asteroids bounce off of each other.
        # When used, it looks a little more glitchy, but also makes for a harder game. This also 
        # could be implemented with levels to increase the difficulty. 
        """for asteroid in self.asteroid_list:
            asteroid.center_x += asteroid.change_x
            asteroid_hit = arcade.check_for_collision_with_list(asteroid, self.asteroid_list)
            for item in asteroid_hit:
                if asteroid.change_x > 0:
                    asteroid.right = item.left
                elif asteroid.change_x < 0:
                    asteroid.left = item.right
            if len(asteroid_hit) > 0:
                asteroid.change_x *= -1

            asteroid.center_y += asteroid.change_y
            asteroid_hit = arcade.check_for_collision_with_list(asteroid, self.asteroid_list)
            for item in asteroid_hit:
                if asteroid.change_y > 0:
                    asteroid.top = item.bottom
                elif asteroid.change_y < 0:
                    asteroid.bottom = item.top
            if len(asteroid_hit) > 0:
                asteroid.change_y *= -1"""

        # This loops through all of the lives that are falling down. It will either add it to the heart count or add a bonus score.
        for life in self.fall_life_list:
            #Checks to make sure that they are below the bottom of the screen before doing anything to them.
            if life.top < 0:
                if len(self.life_list) < START_LIFE:
                    life_sprite = arcade.Sprite(HEART, LIFE_SCALING)
                    h = len(self.life_list)
                    life_sprite.center_x = SCREEN_WIDTH - 30*h - 25
                    life_sprite.center_y = SCREEN_HEIGHT - 21
                    self.life_list.append(life_sprite)
                else:
                    self.score += 2
                life.remove_from_sprite_lists() # Make sure to remove them from this list too, otherwise a whole lot of points are going to be added.

        # Displays the game over screen if the player runs out of lives.
        if len(self.life_list) == 0:
            view = GameOverView()
            self.window.show_view(view)

"""
A little class to create the hearts on the screen, so that these properties apply to each sprite.
"""
class Lives(arcade.Sprite):
    # Sets up the sprite
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.change_x = SCREEN_WIDTH
        self.change_y = SCREEN_HEIGHT
    # Move the sprite down to the bottom of the screen.

    def update(self):
        self.center_y -= 2 # This number determines how fast the Sprite will fall down. 


"""
Another smaller class for creating each asteroid on the screen. 
It will also implement the asteroids bouncing off of the sides of the screen.
"""
class Asteroid(arcade.Sprite):
    # Sets up the sprite
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.change_x = 0
        self.change_y = SCREEN_HEIGHT

    def update(self):
        # Move the asteroid
        self.center_x += self.change_x
        self.center_y += self.change_y

        # When the asteroid starts to move off of the screen it will bounce back.
        if self.left < 0:
            self.change_x *= -1 # Opposite direction
            """
            This code that is commented out, on each bounce check, could be used in the future for creating a harder level.
            It makes the asteroids slowly speed up over time, and if you take too long to hit them, they start going a little crazy fast.
            """
            #self.change_y -= 1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1
            #self.change_y -= 1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1
            #self.change_y -= 1

"""
This will create the particles with the global variables. It uses just two basic functions of init, and update.
"""
class Particle(arcade.SpriteCircle):
    def __init__(self, my_list):
        # Takes a random color, based off of the list of colors we declared.
        color = random.choice(PARTICLE_COLORS)
        super().__init__(PARTICLE_RADIUS, color)

        # Keeps track of the normal color of the particle. This is needed so it can switch back and forth between the white sparkle color.
        self.normal_texture = self.texture

        # Uses Random, and Math libraries to generate a random speed and direction of the particles.
        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed

        # Keeps track of the original alpha. This is necessary for our implementation of the sparkle effect. 
        self.my_alpha = 255

    def update(self):
        # First check that the particle isn't faded out. It is not necessary to continue if it is. 
        if self.my_alpha <= PARTICLE_FADE_RATE:
            self.remove_from_sprite_lists()
        # Otherwise we need to do some math with the particle
        else:
            # Changes the positition of the particle for when update is called.
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= PARTICLE_GRAVITY

            # Gives a random chance for the sparkle effect on the particle.
            if random.random() <= PARTICLE_SPARKLE_CHANCE:
                self.alpha = 255 # Change the alpha
                self.texture = arcade.make_circle_texture(self.width, arcade.color.WHITE)
            else:
                self.texture = self.normal_texture

"""
This will take care of putting another image over the screen, for when the player runs out of lives, and thus it is game over.
"""
class GameOverView(arcade.View):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(":resources:images/backgrounds/game_over.png") # The image I created for the game over screen.

    # Just like the normal game needs an on_draw method so does this, so that we can display the new image on the screen.
    def on_draw(self):
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT) # Make sure we use the same dimensions as the original screen.

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        arcade.close_window() # This will simply close out of the window if the user clicks with the mouse after it pops up.

# The main method used to set up and run the game. For future development, I want to see if it could be used to restart the game after the game over screen.
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MyGame()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()

# Calls the main function to start the game.
if __name__ == "__main__":
    main()