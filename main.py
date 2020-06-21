import pygame as pg
import random
from sprites import *
from Plist import *
from os import path

img = path.join(path.dirname(__file__), 'Mario_graphics')


class Game:
    def __init__(self):

        self.running = True
        pg.init()
        self.screen = pg.display.set_mode((800, 500))
        pg.display.set_caption("Mario Lite")
        icon = pg.image.load(path.join(img, "mario_icon.png")).convert()
        pg.display.set_icon(icon)
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.background = pg.image.load(path.join(img, "back.jpg")).convert()
        self.MR_jump = pg.image.load(path.join(img, "R_jump.png")).convert()
        self.MR_move1 = pg.image.load(path.join(img, "R_move1.png")).convert()
        self.MR_move2 = pg.image.load(path.join(img, "R_move2.png")).convert()
        self.MR_move3 = pg.image.load(path.join(img, "R_move3.png")).convert()
        self.ML_jump = pg.image.load(path.join(img, "L_jump.png")).convert()
        self.ML_move1 = pg.image.load(path.join(img, "L_move1.png")).convert()
        self.ML_move2 = pg.image.load(path.join(img, "L_move2.png")).convert()
        self.ML_move3 = pg.image.load(path.join(img, "L_move3.png")).convert()
        self.platformimg = pg.image.load(path.join(img, "platform.png")).convert()
        self.groundimg = pg.image.load(path.join(img, "ground.png")).convert()
        self.flagimg = pg.image.load(path.join(img, "flag.png")).convert()
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, h_score), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.snd_dir = path.join(self.dir, 'Mario_sound')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'smb_jump-super.wav'))
        self.go_sound = pg.mixer.Sound(path.join(self.snd_dir, 'smb_gameover.wav'))
        self.win_sound = pg.mixer.Sound(path.join(self.snd_dir, 'smb_stage_clear.wav'))

    def new(self):
        self.score_value = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.mario = Mario(self)
        self.all_sprites.add(self.mario)
        self.flag_v = M_Flag(self)
        self.all_sprites.add(self.flag_v)
        self.ground = Ground(self)
        self.all_sprites.add(self.ground)
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        pg.mixer.music.load(path.join(self.snd_dir, 'background.ogg'))
        self.run()

    def run(self):
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(120)
            self.update()
            self.events()
            self.draw()
        pg.mixer.music.fadeout(100)

    def update(self):
        self.all_sprites.update()
        # check if player hits platform only if falling

        if self.mario.vel.y > 0:
            hits = pg.sprite.spritecollide(self.mario, self.platforms, False)
            if hits:
                self.mario.pos.y = hits[0].rect.top
                self.mario.vel.y = 0

            coll = pg.sprite.collide_rect(self.mario, self.ground)
            if coll:
                self.mario.pos.y = self.ground.rect.top
                self.mario.vel.y = 0

            coll_flag = pg.sprite.collide_rect(self.mario, self.flag_v)
            if coll_flag:
                self.playing = False
                self.win_screen()

        for plat in self.platforms:
            plat.rect.x -= 1
        self.flag_v.rect.x -= 1
        self.ground.rect.x -= 1

        if self.mario.rect.right >= 400:
            self.mario.pos.x -= max(abs(int(self.mario.vel.x)), 2)
            for plat in self.platforms:
                plat.rect.x -= max(abs(int(self.mario.vel.x)), 2)
                if plat.rect.right <= 0:
                    plat.kill()
                    self.score_value += 10
            self.flag_v.rect.x -= max(abs(int(self.mario.vel.x)), 2)
            self.ground.rect.x -= max(abs(int(self.mario.vel.x)), 2)

        if self.mario.rect.left < 0:
            self.playing = False
        if self.mario.rect.top > 500:
            self.playing = False

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.mario.jump()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.mario.image, self.mario.rect)
        self.draw_text("Score: " + str(self.score_value), 22, (255, 0, 0), 400, 10)
        pg.display.flip()

    def show_start_screen(self):

        self.screen.fill((0, 155, 155))
        self.draw_text("MARIO LITE", 80, (255, 255, 255), 400, 150)
        self.draw_text("High Score:" + str(self.highscore), 30, (255, 255, 255), 400, 260)
        self.draw_text("Press ARROWS to move, Press SPACE to jump", 20, (255, 255, 255), 400, 400)
        self.draw_text("Press RSHIFT to play", 30, (255, 255, 255), 400, 355)
        pg.display.flip()
        self.wait_for_Enter()

    def wait_for_Enter(self):
        waiting = True
        while waiting:
            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_RSHIFT:
                        waiting = False

    def show_go_screen(self):
        if not self.running:
            return
        self.go_sound.play()
        self.screen.fill((0, 155, 155))
        self.draw_text("Game Over", 70, (255, 255, 255), 400, 150)
        self.draw_text("Score:" + str(self.score_value), 30, (255, 255, 255), 400, 250)
        self.draw_text("Press RSHIFT to play again", 20, (255, 255, 255), 400, 450)
        if self.score_value > self.highscore:
            self.highscore = self.score_value
            self.draw_text("Congratulations !!  New High Score", 30, (255, 255, 255), 400, 300)
            with open(path.join(self.dir, h_score), 'w') as f:
                f.write(str(self.score_value))
        else:
            self.draw_text("High Score:" + str(self.highscore), 30, (255, 255, 255), 400, 300)
        pg.display.flip()
        self.wait_for_Enter()
        self.go_sound.fadeout(100)

    def win_screen(self):

        pg.mixer.music.fadeout(50)
        self.win_sound.play()
        self.screen.fill((0, 155, 155))
        self.draw_text("YOU WIN", 70, (255, 255, 255), 400, 150)
        self.draw_text("Score:" + str(self.score_value), 30, (255, 255, 255), 400, 250)
        self.draw_text("Press RSHIFT to play again", 20, (255, 255, 255), 400, 450)
        if self.score_value > self.highscore:
            self.highscore = self.score_value
            self.draw_text("Congratulations !!  New High Score", 30, (255, 255, 255), 400, 300)
            with open(path.join(self.dir, h_score), 'w') as f:
                f.write(str(self.score_value))
        else:
            self.draw_text("High Score:" + str(self.highscore), 30, (255, 255, 255), 400, 300)
        pg.display.flip()
        self.wait_for_Enter()
        self.win_sound.fadeout(100)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font('freesansbold.ttf', size)
        text = font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
