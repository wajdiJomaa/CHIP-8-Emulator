from chip8 import Chip8
from instruction import Instruction, InstructionType
from display import Display
import sdl2
import random
import time

class InstructionExecutor:
    def __init__(self, chip8: Chip8, display: Display):
        self.chip8 : Chip8 = chip8
        self.display : Display = display
        self.current_instruction : Instruction = None
        self.is_key_pressed = False
        self.key = None
        self.delay_timer_interval = 0
        self.sound_timer_interval = 0
        self.clear_key = time.perf_counter()
    
    def fetch(self):
        byte1 = self.chip8.memory[self.chip8.pc]
        byte2 = self.chip8.memory[self.chip8.pc + 1]
        # print("byte1:"  + str(byte1), "byte 2:" + str(byte2))
        
        self.chip8.pc += 2
        self.current_instruction = Instruction(byte1, byte2)
        
    
    def dispatch(self):
        self.current_instruction.t = InstructionType.UNKNOWN
        match self.current_instruction.upper_b1:
            case 0x0:
                if self.current_instruction.lower_b2 == 0x0:
                    self.current_instruction.t = InstructionType.CLEAR
                
                elif self.current_instruction.lower_b2 == 0xE:
                    self.current_instruction.t = InstructionType.RETURN
            case 0x2:
                self.current_instruction.t = InstructionType.CALL
            case 0x1:
                self.current_instruction.t = InstructionType.JUMP
            case 0x3:
                self.current_instruction.t = InstructionType.JUMP_EQ_NN
            case 0x4:
                self.current_instruction.t = InstructionType.JUMP_NEQ_NN
            case 0x5:
                self.current_instruction.t = InstructionType.JUMP_EQ
            case 0x6:
                self.current_instruction.t = InstructionType.SET_REGISTER
            case 0x7:
                self.current_instruction.t = InstructionType.ADD_REGISTER
            case 0x8:
                if self.current_instruction.lower_b2 == 0x0:
                    self.current_instruction.t = InstructionType.COPY
                elif self.current_instruction.lower_b2 == 0x1:
                    self.current_instruction.t = InstructionType.BINARY_OR
                elif self.current_instruction.lower_b2 == 0x2:
                    self.current_instruction.t = InstructionType.BINARY_AND
                if self.current_instruction.lower_b2 == 0x3:
                    self.current_instruction.t = InstructionType.LOGICAL_XOR
                if self.current_instruction.lower_b2 == 0x4:
                    self.current_instruction.t = InstructionType.ADD
                if self.current_instruction.lower_b2 == 0x5:
                    self.current_instruction.t = InstructionType.SUBTRACT    
                if self.current_instruction.lower_b2 == 0x7:
                    self.current_instruction.t = InstructionType.ISUBTRACT
                if self.current_instruction.lower_b2 == 0x6:
                    self.current_instruction.t = InstructionType.RSHIFT 
                if self.current_instruction.lower_b2 == 0x9:
                    self.current_instruction.t = InstructionType.LSHIFT
            case 0x9:
                self.current_instruction.t = InstructionType.JUMP_NEQ
            case 0xA:
                self.current_instruction.t = InstructionType.SET_INDEX_REGISTER
            case 0xB:
                self.current_instruction.t = InstructionType.JUMP_OFFSET
            case 0xD:
                self.current_instruction.t = InstructionType.DISPLAY
            case 0xE:
                if self.current_instruction.upper_b2 == 0x9 and self.current_instruction.lower_b2 == 0xE:
                    self.current_instruction.t = InstructionType.SKIP_IF_KEY
                elif self.current_instruction.upper_b2 == 0xA and self.current_instruction.lower_b2 == 0x1:
                    self.current_instruction.t = InstructionType.SKIP_IF_NOT_KEY
            case 0xF:
                if self.current_instruction.upper_b2 == 0x1 and self.current_instruction.lower_b2 == 0xE:
                    self.current_instruction.t = InstructionType.ADD_INDEX
                elif self.current_instruction.upper_b2 == 0x0 and self.current_instruction.lower_b2 == 0xA:
                    self.current_instruction.t = InstructionType.GET_KEY
                elif self.current_instruction.upper_b2 == 0x2 and self.current_instruction.lower_b2 == 0x9:
                    self.current_instruction.t = InstructionType.FONT
                elif self.current_instruction.upper_b2 == 0x3 and self.current_instruction.lower_b2 == 0x3:
                    self.current_instruction.t = InstructionType.BINARY_CODED_DECIMAL
                elif self.current_instruction.upper_b2 == 0x5 and self.current_instruction.lower_b2 == 0x5:
                    self.current_instruction.t = InstructionType.STORE
                elif self.current_instruction.upper_b2 == 0x6 and self.current_instruction.lower_b2 == 0x5:
                    self.current_instruction.t = InstructionType.LOAD
                elif self.current_instruction.upper_b2 == 0x0 and self.current_instruction.lower_b2 == 0x7:
                    self.current_instruction.t = InstructionType.READ_DELAY_TIMER
                elif self.current_instruction.upper_b2 == 0x1 and self.current_instruction.lower_b2 == 0x5:
                    self.current_instruction.t = InstructionType.SET_DELAY_TIMER
                elif self.current_instruction.upper_b2 == 0x1 and self.current_instruction.lower_b2 == 0x8:
                    self.current_instruction.t = InstructionType.SET_BEAP_TIMER
            case _:
                self.current_instruction.t = InstructionType.UNKNOWN
    
    def execute(self):
        match self.current_instruction.t:
            case InstructionType.JUMP:
                self.execute_jump()
            
            case InstructionType.SET_REGISTER:
                self.execute_set_register()    
            
            case InstructionType.ADD_REGISTER:
                self.execute_add_register()    
                
            case InstructionType.SET_INDEX_REGISTER:
                self.execute_set_index_register()    
                
            case InstructionType.CLEAR:
                self.execute_clear()

            case InstructionType.DISPLAY:
                self.execute_display()
            
            case InstructionType.RETURN:
                self.execute_return()
                
            case InstructionType.CALL:
                self.execute_call()
                
            case InstructionType.JUMP_EQ_NN:
                self.execute_jump_eq_nn()
            case InstructionType.JUMP_NEQ_NN:
                self.execute_jump_neq_nn()
            case InstructionType.JUMP_NEQ:
                self.execute_jump_neq()
            case InstructionType.JUMP_EQ:
                self.execute_jump_eq()
            case InstructionType.COPY:
                self.execute_copy()
            case InstructionType.BINARY_OR:
                self.execute_or()
            case InstructionType.BINARY_AND:
                self.execute_and()
            case InstructionType.LOGICAL_XOR:
                self.execute_xor()
            case InstructionType.ADD:
                self.execute_add()
            case InstructionType.SUBTRACT:
                self.execute_substract()
            case InstructionType.ISUBTRACT:
                self.execute_isubstract()
            case InstructionType.LSHIFT:
                self.execute_shift_left()
            case InstructionType.RSHIFT:
                self.execute_shift_right()
            case InstructionType.RANDOM:
                self.execute_random()
            case InstructionType.JUMP_OFFSET:
                self.execute_jump_with_offset()
            case InstructionType.ADD_INDEX:
                self.execute_add_index()
            case InstructionType.GET_KEY:
                self.execute_get_key()
            case InstructionType.SKIP_IF_KEY:
                self.execute_skip_if_key()
            case InstructionType.SKIP_IF_NOT_KEY:
                self.execute_skip_if_not_key()
            case InstructionType.FONT:
                self.execute_font()
            case InstructionType.BINARY_CODED_DECIMAL:
                self.execute_binary_coded_decimal()
            case InstructionType.STORE:
                self.execute_store()
            case InstructionType.LOAD:
                self.execute_load()
            case InstructionType.SET_BEAP_TIMER:
                self.execute_beap_timer()
            case InstructionType.SET_DELAY_TIMER:
                self.execute_set_delay_timer()
            case InstructionType.READ_DELAY_TIMER:
                self.execute_read_delay_timer()
            case InstructionType.UNKNOWN:
                print("UNKNOWN Instruction")
            case _:
                print("should not happen: " + str(self.current_instruction.t))
    
    def execute_jump(self):
        # print("JUMP:" + str((self.current_instruction.lower_b1 << 8) | self.current_instruction.b2))
        self.chip8.pc = (self.current_instruction.lower_b1 << 8) | self.current_instruction.b2
    
    def execute_set_register(self):
        # print("SET REGISTER: " + str(self.current_instruction.lower_b1))
        self.chip8.registers[self.current_instruction.lower_b1] = self.current_instruction.b2
    
    def execute_add_register(self):
        # print("Add Register: " + str(self.current_instruction.lower_b1))
        res = (self.chip8.registers[self.current_instruction.lower_b1] + self.current_instruction.b2) & 0xFF        
        self.chip8.registers[self.current_instruction.lower_b1] = res
        
    def execute_set_index_register(self):
        # print("SET Index REGISTER" + str ((self.current_instruction.lower_b1 << 8) | self.current_instruction.b2))
        self.chip8.index_register = (self.current_instruction.lower_b1 << 8) | self.current_instruction.b2
        
    
    def execute_clear(self):
        # print("CLEAR")
        self.display.clear()
        
    def execute_display(self):
        # print("DISPLAY")
        x = self.chip8.registers[self.current_instruction.lower_b1] % self.display.reg_width
        y = self.chip8.registers[self.current_instruction.upper_b2] % self.display.reg_height
        n = self.current_instruction.lower_b2
        
        ir = self.chip8.index_register

        self.chip8.registers[0xf] = 0x0
        for j in range(n):
            sprite = self.chip8.memory[ir + j]
            for i in range(8):
                bit = (sprite >> 7-i) & 1
                if bit == 1:
                    if x + i >= self.display.reg_width:
                        break
                    if self.display.flip_pixel(int(x) + i, int(y)):
                        self.chip8.registers[0xf] = 0x1
                
            y+=1
            offset = 0
            if y >= self.display.reg_height:
                break
            # print(offset)
            
        
    def execute_return(self):
        if self.chip8.stack != []:
            self.chip8.pc = self.chip8.stack.pop()
    
    def execute_call(self):
        self.chip8.stack.append(self.chip8.pc)
        self.chip8.pc = (self.current_instruction.lower_b1 << 8) | self.current_instruction.b2
        
    def execute_jump_eq_nn(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        n = self.current_instruction.b2
        
        if x == n:
            self.chip8.pc += 2 
            
    def execute_jump_neq_nn(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        n = self.current_instruction.b2
        
        if x != n:
            self.chip8.pc += 2 
    
    def execute_jump_eq(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        y = self.chip8.registers[self.current_instruction.upper_b2]
        
        if x == y:
            self.chip8.pc += 2 
    
    def execute_jump_neq(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        y = self.chip8.registers[self.current_instruction.upper_b2]
        
        if x != y:
            self.chip8.pc += 2 
    
    def execute_copy(self):
        self.chip8.registers[self.current_instruction.lower_b1] = self.chip8.registers[self.current_instruction.upper_b2]
    
    def execute_or(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        y = self.chip8.registers[self.current_instruction.upper_b2]
        
        self.chip8.registers[self.current_instruction.lower_b1] = x | y
    
    def execute_and(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        y = self.chip8.registers[self.current_instruction.upper_b2]
        
        self.chip8.registers[self.current_instruction.lower_b1] = x & y 

    def execute_xor(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        y = self.chip8.registers[self.current_instruction.upper_b2]
        
        self.chip8.registers[self.current_instruction.lower_b1] = x ^ y
        
    def execute_add(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        y = self.chip8.registers[self.current_instruction.upper_b2]
        z = x + y
        
        if z > 255:
            self.chip8.registers[0xf] = 1
        else:
            self.chip8.registers[0xf] = 0
            
        self.chip8.registers[self.current_instruction.lower_b1] = z & 0xFF
    
    def execute_substract(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        y = self.chip8.registers[self.current_instruction.upper_b2]
        
        if x > y:
            self.chip8.registers[0xf] = 1
        else:
            self.chip8.registers[0xf] = 0
        
        self.chip8.registers[self.current_instruction.lower_b1] = (x - y) & 0xFF
    
    def execute_isubstract(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        y = self.chip8.registers[self.current_instruction.upper_b2]
        
        if y > x:
            self.chip8.registers[0xf] = 1
        else:
            self.chip8.registers[0xf] = 0
        
        self.chip8.registers[self.current_instruction.lower_b1] = (y - x) & 0xFF
    
    def execute_shift_right(self):
        self.chip8.registers[0xf] = self.chip8.registers[self.current_instruction.lower_b1] & 0x1
        self.chip8.registers[self.current_instruction.lower_b1] >>= 1
    
    def execute_shift_left(self):
        self.chip8.registers[0xf] = (self.chip8.registers[self.current_instruction.lower_b1] >> 7) & 0x1
        self.chip8.registers[self.current_instruction.lower_b1] <<= 1 & 0xFF
        
    def execute_jump_with_offset(self):
        self.chip8.pc = (self.current_instruction.lower_b1 << 8) | self.current_instruction.b2
        self.chip8.pc += self.chip8.registers[0x0]
        
    def execute_random(self):
        ran = random.random() * self.current_instruction.b2
        self.chip8.registers[self.current_instruction.lower_b1] = ran & self.current_instruction.b2
    
    def execute_add_index(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        self.chip8.index_register += x
        
        self.chip8.registers[0xF] = 1 if self.chip8.index_register > 0x0FFF else 0
        self.chip8.index_register &= 0x0FFF
        
    def execute_get_key(self):
        # print(self.is_key_pressed)
        # print(self.key)
        if self.is_key_pressed and self.key is not None:
            self.chip8.registers[self.current_instruction.lower_b1] = self.key
        else:
            self.chip8.pc -= 2
    
    def execute_skip_if_key(self):
        if self.is_key_pressed and self.key is not None:
            x = self.chip8.registers[self.current_instruction.lower_b1]
            print(self.is_key_pressed)
            if x == self.key:
                self.chip8.pc += 2    
    
    def execute_skip_if_not_key(self):
        if self.is_key_pressed and self.key is not None:
            x = self.chip8.registers[self.current_instruction.lower_b1]
            if x == self.key:
                return
            
        self.chip8.pc += 2
    
    
    def execute_font(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        char = x & 0x0F
        self.chip8.index_register = (char * 5) + self.chip8.font_offset
    
    def execute_binary_coded_decimal(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        d3 = x % 10
        d2 = (x // 10) % 10
        d1 = (x // 100) % 10
        self.chip8.memory[self.chip8.index_register] = d1
        self.chip8.memory[self.chip8.index_register + 1] = d2
        self.chip8.memory[self.chip8.index_register + 2] = d3
    
    def execute_load(self):
        for i in range(self.current_instruction.lower_b1 + 1):
            self.chip8.registers[i] = self.chip8.memory[self.chip8.index_register + i]

    def execute_store(self):
        for i in range(self.current_instruction.lower_b1 + 1):
            self.chip8.memory[self.chip8.index_register + i] = self.chip8.registers[i]
    
    def execute_set_delay_timer(self):
        self.delay_timer_interval = time.perf_counter()
        self.chip8.delay_timer = self.chip8.registers[self.current_instruction.lower_b1]

    def execute_beap_timer(self):
        self.sound_timer_interval = time.perf_counter()
        self.chip8.sound_timer = self.chip8.registers[self.current_instruction.lower_b1]
    
    def execute_read_delay_timer(self):
        self.chip8.registers[self.current_instruction.lower_b1] = self.chip8.delay_timer
    
    def run(self):
        while True:
            event = sdl2.SDL_Event()
            while sdl2.SDL_PollEvent(event):
                if event.type == sdl2.SDL_QUIT:
                    return
                
                elif event.type == sdl2.SDL_KEYDOWN:
                    self.is_key_pressed = True
                    self.key = self.display.get_key(event.key.keysym.sym)
                    print("Key down:", self.key)
            
            self.fetch()
            self.dispatch()
            self.execute()
            
            
            t = time.perf_counter()
            
            if self.chip8.delay_timer > 0:
                if t - self.delay_timer_interval >= (1/60):
                    self.delay_timer_interval += 1/60
                    self.chip8.delay_timer -= 1
            
            if self.chip8.sound_timer > 0:
                self.display.play_sound()
                if t - self.sound_timer_interval >= (1/60):
                    self.sound_timer_interval += 1/60
                    self.chip8.sound_timer -= 1
            
            
            if t - self.clear_key >= (1/60):
                self.key = None
                self.is_key_pressed = False
                self.clear_key = t