# Rice Rocks!
# Working Version not Final
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
SAFE_RADIUS = 150
score = 0
lives = 3
time = 0
normal_score = 500
combo_score = 100
text_loc_1 = 650
text_loc_2 = 50
text_loc_3 = 40
text_loc_4 = 80

# Combo Text Location
text_loc_5 = 250

# Bomb Text Location
text_loc_6 = 400

combo = 0
bomb = 3
timers = 0
bomb_threshold_level = 1
bomb_threshold_score = 200000
threshold_level = 1
threshold_score = 50000
started = False
rock_group = set()
missile_group = set()
explosion_group = set()

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.shoot_timer = False
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + 90, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def thrust_on(self):
        self.thrust = True
        ship_thrust_sound.play()
    
    def thrust_off(self):
        self.thrust = False
        ship_thrust_sound.rewind()
    
    def turn_clockwise(self):
        self.angle_vel = 0.1
    
    def turn_counter_clockwise(self):
        self.angle_vel = -0.1
        
    def turn_stop(self):
        self.angle_vel = 0
        
    def get_angle(self):
        return self.angle
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def get_vel(self):
        return self.vel
    
    def shoot(self):
        self.shoot_timer = True
    
    def stop_shoot(self):
        self.shoot_timer = False
    
    def reset_pos(self):
        self.pos = [WIDTH / 2, HEIGHT / 2]
        self.angle = 0
        self.vel = [0, 0]
        self.angle_vel = 0
        self.thrust = False
        ship_thrust_sound.rewind()
    
    def get_shoot_timer(self):
        return self.shoot_timer
    
    def update(self):
        self.angle += self.angle_vel
        if self.thrust:
            acceleration = 0.5
        else:
            acceleration = 0
        self.vel[0] = acceleration * angle_to_vector(self.angle)[0] + 0.95 * self.vel[0]
        self.vel[1] = acceleration * angle_to_vector(self.angle)[1] + 0.95 * self.vel[1]
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            image = self.image_center[0] + self.age * self.image_size[0]
            canvas.draw_image(self.image, [image, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        if self.age > self.lifespan:
            return True
    
    def collide(self, other_object):
        if dist(self.pos, other_object.get_pos()) <= self.radius + other_object.get_radius():
            return True
        else:
            return False
    
    def get_radius(self):
        return self.radius
    
    def get_pos(self):
        return self.pos

def draw(canvas):
    global time, lives, score, started, rock_group, combo
    global explosion_group, threshold_level, bomb_threshold_level
    global bomb_threshold_score, bomb
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # Prevent the game from updating if it isn't started
    if started:
        soundtrack.play()
        
        # update the rock, missle, and expolsion groups
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
    
        # draw and update ship
        my_ship.draw(canvas)
        my_ship.update()
        
        canvas.draw_text('Score', [text_loc_1, text_loc_2], 36, 'White', 'serif')
        canvas.draw_text('Lives', [text_loc_3, text_loc_2], 36, 'White', 'serif')
        canvas.draw_text('Combo', [text_loc_5, text_loc_2], 36, 'White', 'serif')
        canvas.draw_text('Bomb', [text_loc_6, text_loc_2], 36, 'White', 'serif')
        canvas.draw_text(str(score), [text_loc_1, text_loc_4 + 10], 36, 'White', 'serif')
        canvas.draw_text(str(combo), [text_loc_5, text_loc_4 + 10], 36, 'White', 'serif')
        canvas.draw_text('Time Elapsed: ' + str(timers) + ' second(s)', [30, 590], 20, 'White', 'serif')
        
        if bomb > 5:
            bomb_appearance = [explosion_info.get_center()[0] + 4 * explosion_info.get_size()[0], explosion_info.get_center()[1]]
            canvas.draw_image(explosion_image, bomb_appearance,\
                          explosion_info.get_size(), [text_loc_6, 80],\
                          [explosion_info.get_size()[0] // 2, explosion_info.get_size()[1] // 2])
            canvas.draw_text(' x ' + str(bomb), [text_loc_6 + 20, text_loc_4 + 10], 36, 'White', 'serif')
        else:
            for bombs in range(0, bomb):
                bomb_appearance = [explosion_info.get_center()[0] + 4 * explosion_info.get_size()[0], explosion_info.get_center()[1]]
                canvas.draw_image(explosion_image, bomb_appearance,\
                          explosion_info.get_size(), [text_loc_6 + 40 * bombs, 80],\
                          [explosion_info.get_size()[0] // 2, explosion_info.get_size()[1] // 2])
        
        if lives > 5:
            canvas.draw_image(ship_image, ship_info.get_center(),\
                          ship_info.get_size(), [text_loc_3, text_loc_4],
                          [ship_info.get_size()[0] // 2, ship_info.get_size()[1] // 2], -math.pi / 2)
            canvas.draw_text(' x ' + str(lives), [text_loc_3 + 20, text_loc_4 + 10], 36, 'White', 'serif')
        else:
            for life in range(0, lives):
                canvas.draw_image(ship_image, ship_info.get_center(),\
                          ship_info.get_size(), [40 + 40 * life, 80],
                          [ship_info.get_size()[0] // 2, ship_info.get_size()[1] // 2], -math.pi / 2)

        if lives <= 0:
            started = False
            rock_group = set()
            explosion_group = set()
            soundtrack.rewind()
    
    # check for collision between ship and rocks
    if group_collide(rock_group, my_ship):
        lives -= 1
        my_ship.reset_pos()
        combo = 0
        
        # Destroy nearby rocks on re-spawn
        rocks = set(rock_group)
        for close_rock in rocks:
            if (dist(close_rock.get_pos(), my_ship.get_pos())) <= 1.5 * (my_ship.get_radius() + close_rock.get_radius()):
                rock_group.remove(close_rock)
                explosion_group.add(Sprite(close_rock.get_pos(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
    
    # check for collision between missiles and rocks and
    # increment score
    if group_group_collide(rock_group, missile_group):
        score += (normal_score + combo * combo_score)
        combo += 1
        
        # If score is at a certain threshold, increase
        # the number of lives
        if (score >= threshold_level * threshold_score):
            lives += 1
            threshold_level += 1
            
        if (score >= bomb_threshold_level * bomb_threshold_score):
            bomb += 1
            bomb_threshold_level += 1
    
    # flash the splash screen if game over or not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),\
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],\
                          splash_info.get_size())
# Bomb
def release_bomb():
    global bomb, score, combo, threshold_level, lives
    global bomb_threshold_level
    if bomb > 0:
        bomb -= 1
        rocks = set(rock_group)
        for rock in rocks:
            rock_group.discard(rock)
            explosion_group.add(Sprite(rock.get_pos(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
            score += (normal_score + combo * combo_score)
            combo += 1
        
        # If score is at a certain threshold, increase
        # the number of lives
        if (score >= threshold_level * threshold_score):
            lives += 1
            threshold_level += 1
            
        if (score >= bomb_threshold_level * bomb_threshold_score):
            bomb += 1
            bomb_threshold_level += 1

def stop_release_bomb():
    pass

def shoot_missile():
    if my_ship.get_shoot_timer() and started:
        missile_group.add(Sprite([my_ship.get_pos()[0] + 35 * angle_to_vector(my_ship.get_angle())[0], my_ship.get_pos()[1] + 35 * angle_to_vector(my_ship.get_angle())[1]], [my_ship.get_vel()[0] + 7 * angle_to_vector(my_ship.get_angle())[0], my_ship.get_vel()[1] + 7 * angle_to_vector(my_ship.get_angle())[1]], 0, 0, missile_image, missile_info, missile_sound))
            
# Initializes ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# Inputs for dictionaries
inputs = { 'up': my_ship.thrust_on, 'left': my_ship.turn_counter_clockwise, 'right': my_ship.turn_clockwise, 'space': my_ship.shoot, 'e': release_bomb }
key_up_inputs = { 'up': my_ship.thrust_off, 'left': my_ship.turn_stop, 'right': my_ship.turn_stop, 'space': my_ship.stop_shoot, 'e': stop_release_bomb }

# helper function for drawing the sprites
def process_sprite_group(sprite_group, canvas):
    group_set = set(sprite_group)
    for sprite in group_set:
        sprite.draw(canvas)
        if sprite.update():
            sprite_group.remove(sprite)

# helper function for detecting collision between sprites
def group_collide(group, other_object):
    group_set = set(group)
    collision = False
    for individual in group_set:
        if individual.collide(other_object):
            group.remove(individual)
            collision = True
            explosion_group.add(Sprite(other_object.get_pos(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
    return collision

# helper function for detecting collision between groups
# of sprites
def group_group_collide(group, other_group):
    group_set = set(group)
    collision = False
    for individual in group_set:
        if group_collide(other_group, individual):
            group.discard(individual)
            collision = True
    return collision

# timer handler that spawns a rock    
def rock_spawner():
    global timers
    # Makes the speed of the new rocks faster with score
    speed_multiplier = 1 + (score // 10000) * 0.05
    timers += 1
    
    # Spawn rocks
    spawn_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    spawn_vel = [(random.randrange(-2, 2) + 0.01) * speed_multiplier , (random.randrange(-2, 2) + 0.01) * speed_multiplier]
    spawn_ang_vel = float(random.randrange(-20,20)) / 100
    in_safe_zone = (dist(my_ship.get_pos(), spawn_pos) > asteroid_info.get_radius() + SAFE_RADIUS)
    if (len(rock_group) < 12) and started and in_safe_zone:
        rock_group.add(Sprite(spawn_pos, spawn_vel, 0, spawn_ang_vel, asteroid_image, asteroid_info))
        
# Mouseclick and keyboard handlers
def mouse_click(pos):
    global started, lives, score, bomb, bomb_threshold_level
    global threshold_level, timers
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    in_width = (center[0] - size[0] < pos[0]) and (center[0] + size[0] > pos[0])
    in_height = (center[1] - size[1] < pos[1]) and (center[1] + size[1] > pos[1])
    if (not started) and (in_width and in_height):
        started = True
        lives = 3
        score = 0
        bomb = 3
        threshold_level = 1
        bomb_threshold_level = 1
        timers = 0

def key_down(key):
    for i in inputs:
        if key == simplegui.KEY_MAP[i]:
            inputs[i]()

def key_up(key):
    for i in inputs:
        if key == simplegui.KEY_MAP[i]:
            key_up_inputs[i]()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_click)
timer = simplegui.create_timer(1000.0, rock_spawner)
shoot_timer_handler = simplegui.create_timer(250.0, shoot_missile)
label_main = frame.add_label('Welcome to Rice Rocks!')
label_space0 = frame.add_label('')
label0 = frame.add_label('Instructions:')
label2 = frame.add_label('1. Press Up for thrust')
label3 = frame.add_label('2. Press Left or Right to turn')
label4 = frame.add_label('3. Press Space to shoot')
label5 = frame.add_label('4. Press E for bomb')
label_space1 = frame.add_label('')
label6 = frame.add_label('Hints:')
label7 = frame.add_label('1. Gain a life every 50000 pts')
label8 = frame.add_label('2. Gain a bomb every 200000 pts')
label9 = frame.add_label('3. Combo adds to score and it resets when your ship gets destroyed')
label10 = frame.add_label('4. Helpful to conserve your bomb')
label11 = frame.add_label('')
label12 = frame.add_label('Enjoy your play!')
label13 = frame.add_label('-F.S.')

# get things rolling
timer.start()
shoot_timer_handler.start()
frame.start()
