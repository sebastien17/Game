import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, initial_position ,*groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('player.png')
        self.initial_x, self.initial_y =  initial_position
        self.rect = pygame.rect.Rect(initial_position , self.image.get_size())
        self.speed = 300
        self.vertical_speed = 0
        self.resting = False
    def update(self, dt, collide_ref):
        last = self.rect.copy() #la copie est importante sinon on a juste une référence sur un objet qui va être modifié
        new = self.rect # Ici c'est bien une référence
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            new.x -= self.speed * dt
        if key[pygame.K_RIGHT]:
            new.x += self.speed * dt
        if self.resting and key[pygame.K_SPACE] :
            self.vertical_speed = -500
            
        #On applique la gravitée
        self.vertical_speed = min(400, self.vertical_speed + 40)
        new.y += self.vertical_speed * dt
        
        self.resting = False
        for cell in  pygame.sprite.spritecollide(self,collide_ref, False):
            cell = cell.rect #On ne conserve que la donnée importante
            if last.right <= cell.left and new.right >= cell.left:
                new.right = cell.left 
            if last.left >= cell.right and new.left <= cell.right:
                new.left = cell.right 
            if last.bottom <= cell.top and new.bottom >= cell.top:
                new.bottom = cell.top 
                self.resting = True
                self.vertical_speed = 0
            if last.top >= cell.bottom and new.top <= cell.bottom:
                new.top = cell.bottom
                self.vertical_speed = 0
        
class Background(pygame.sprite.Sprite):
    def __init__(self,image_file, *groups):
        super(Background, self).__init__(*groups)
        self.image = pygame.image.load(image_file)
        self.rect = pygame.rect.Rect((0,0), self.image.get_size())

class ScrolledGroup(pygame.sprite.Group):
    def __init__(self,*sprites):
        super(ScrolledGroup, self).__init__(*sprites)
        self.camera_x = 0
    def draw(self,surface, x_translate):
        for sprite in self.sprites():
            surface.blit(sprite.image,(sprite.rect.x - x_translate, sprite.rect.y))

class Game(object):
    def __init__(self, screen_mode, title):
        "Constructor method"
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(screen_mode)
        self.width, self.height = screen_mode
    
    def main(self):
        clock = pygame.time.Clock()        
        #Definition des Groupes de sprite
        players_sprites = ScrolledGroup()
        obstacle = ScrolledGroup()
        background_sprites = pygame.sprite.Group()
        #Assignation des entitées à leur groupes respectifs
        player = Player((640,600),players_sprites)
        background = Background('night-bkg.png',background_sprites)
        #Creation des murs + assignation
        block = pygame.image.load('block.png')
        for i in range(0,self.width*2,64):
            for j in range(0,self.height,64):
                if i in (0, self.width*2 - 64) or j in (0, self.height - 64): #Le monde fait 2 fois l'écran
                    wall = pygame.sprite.Sprite(obstacle)
                    wall.image = block
                    wall.rect = pygame.rect.Rect((i,j), block.get_size())
        #Blocs de test
        wall = pygame.sprite.Sprite(obstacle)
        wall.image = block
        wall.rect = pygame.rect.Rect((640,960-3*64), block.get_size())
        wall = pygame.sprite.Sprite(obstacle)
        wall.image = block
        wall.rect = pygame.rect.Rect((640-64,960-2*64), block.get_size())
        while True:
            dt = clock.tick(30) # dt en milliéme de seconde
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            #Mise à jour des groupes de sprites pour lequel cela est nécessaire
            players_sprites.update(dt /1000., obstacle)   #Passage de paramètre en seconde
            #Ecriture des groupes de sprites
            background_sprites.draw(self.screen)
            obstacle.draw(self.screen, player.rect.x - player.initial_x) #Scrolled sprite group
            players_sprites.draw(self.screen,  player.rect.x - player.initial_x)#Scrolled sprite group
            #Affichage (swap buffer)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    
    Game((1280,960),'Game test').main() 