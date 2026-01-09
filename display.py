import sdl2.ext as se
import sdl2 as s
import pygame.mixer
class Display:
    def __init__(self):
        self.scale = 10
        self.width = 64 * self.scale
        self.reg_width = self.width / self.scale
        self.height = 32 * self.scale
        self.reg_height = self.height / self.scale
        
        self.running = True
        se.init()
        self.window = se.Window("CHIP-8", size=(self.width, self.height))
        self.surface = s.SDL_GetWindowSurface(self.window.window)
        self.pixels = se.pixels2d(self.surface.contents)

        pygame.mixer.init()
        self.beep_sound = pygame.mixer.Sound("beep.wav")
        self.beep_channel = None

        self.window.show()
        self.KEYMAP = {
            s.SDLK_1: 0x1,
            s.SDLK_2: 0x2,
            s.SDLK_3: 0x3,
            s.SDLK_4: 0xC,
            s.SDLK_q: 0x4,
            s.SDLK_w: 0x5,
            s.SDLK_e: 0x6,
            s.SDLK_r: 0xD,
            s.SDLK_a: 0x7,
            s.SDLK_s: 0x8,
            s.SDLK_d: 0x9,
            s.SDLK_f: 0xE,
            s.SDLK_z: 0xA,
            s.SDLK_x: 0x0,
            s.SDLK_c: 0xB,
            s.SDLK_v: 0xF,
        }
        
    def flip_pixel(self, x, y):
        turned_off = False
        # print(x,y)
        for i in range(self.scale):
            for j in range(self.scale):
                if x*self.scale + i >= self.width or y*self.scale + j >= self.height:
                    continue
                if self.pixels[x*self.scale + i, y*self.scale + j] == 0xFFFFFFFF:         
                    self.pixels[x*self.scale + i, y*self.scale + j] = 0x00000000
                    turned_off = True
                else:
                    self.pixels[x*self.scale + i, y*self.scale + j] = 0xFFFFFFFF
                    
        s.SDL_UpdateWindowSurface(self.window.window)
        # self.window.refresh()
        # print(turned_off)
        return turned_off
                        
    def clear(self):
        for row in self.pixels:
             row[:] = 0x00000000
        s.SDL_UpdateWindowSurface(self.window.window)
        # self.window.refresh()
    
    def destroy(self):
        se.quit()
        
    def play_sound(self):
        if self.beep_channel is None or not self.beep_channel.get_busy():
            self.beep_channel = self.beep_sound.play()

    def get_key(self, k):
        if k not in self.KEYMAP:
            return None
        return self.KEYMAP[k]   