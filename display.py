import sdl2.ext as se
import sdl2 as s

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
        self.clear()
        self.window.show()
    
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