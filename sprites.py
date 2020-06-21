import pygame as pg

vec = pg.math.Vector2


class Mario(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self)

        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image1 = self.L_walk[0]
        self.image = pg.transform.scale(self.image1, (60, 60))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (40, 250)
        self.pos = vec(40, 250)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):

        self.L_walk = [self.game.ML_move1, self.game.ML_move2, self.game.ML_move3]
        for l in self.L_walk:
            l.set_colorkey((0, 0, 0))
        self.R_walk = [self.game.MR_move1, self.game.MR_move2, self.game.MR_move3]
        for l in self.R_walk:
            l.set_colorkey((0, 0, 0))
        self.L_jump = self.game.ML_jump
        self.L_jump.set_colorkey((0, 0, 0))
        self.R_jump = self.game.MR_jump
        self.R_jump.set_colorkey((0, 0, 0))

    def jump(self):
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits:
            self.game.jump_sound.play()
            self.vel.y = -20

        self.rect.x += 1
        coll = pg.sprite.collide_rect(self, self.game.ground)
        self.rect.x -= 1
        if coll:
            self.game.jump_sound.play()
            self.vel.y = -20

    def update(self):
        self.animate()
        self.acc = vec(0, 1)  # adding gravity as y component
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.acc.x = 0.5
        if keys[pg.K_LEFT]:
            self.acc.x = -0.5

        # apply friction
        self.acc.x += self.vel.x * -0.15
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # set boundaries
        if self.pos.x > 800:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = 800
        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()

        if self.vel.y != 0:
            self.jumping = True
        else:
            self.jumping = False

        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.R_walk)
            bottom = self.rect.bottom
            if self.acc.x >= 0:
                self.image = self.R_walk[self.current_frame]
            else:
                self.image = self.L_walk[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        if self.jumping:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = self.current_frame + 1
                bottom = self.rect.bottom
                if self.vel.x >= 0:
                    self.image = self.R_jump
                else:
                    self.image = self.L_jump
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image1 = self.game.platformimg
        self.image = pg.transform.scale(self.image1, (120, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ground(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.groundimg
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 465


class M_Flag(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.flagimg
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 10250
        self.rect.y = 230
