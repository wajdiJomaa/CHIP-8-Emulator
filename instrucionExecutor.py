from chip8 import Chip8
from instruction import Instruction, InstructionType
from display import Display
import sdl2
import sdl2.ext
import random

class InstructionExecutor:
    def __init__(self, chip8: Chip8, display: Display):
        self.chip8 : Chip8 = chip8
        self.display : Display = display
        self.current_instruction : Instruction = None

    def fetch(self):
        byte1 = self.chip8.memory[self.chip8.pc]
        byte2 = self.chip8.memory[self.chip8.pc + 1]
        # print("byte1:"  + str(byte1), "byte 2:" + str(byte2))
        
        self.chip8.pc += 2
        if self.chip8.pc < 540:
            print(self.chip8.pc)
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
                if self.current_instruction.lower_b2 == 0x1:
                    self.current_instruction.t = InstructionType.BINARY_OR
            case 0x9:
                self.current_instruction.t = InstructionType.JUMP_NEQ
            case 0xA:
                self.current_instruction.t = InstructionType.SET_INDEX_REGISTER
            case 0xD:
                self.current_instruction.t = InstructionType.DISPLAY
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
            case InstructionType.UNKNOWN:
                print("UNKNOWN Instruction")
    
    def execute_jump(self):
        # print("JUMP:" + str((self.current_instruction.lower_b1 << 8) | self.current_instruction.b2))
        self.chip8.pc = (self.current_instruction.lower_b1 << 8) | self.current_instruction.b2
    
    def execute_set_register(self):
        print("SET REGISTER: " + str(self.current_instruction.lower_b1))
        self.chip8.registers[self.current_instruction.lower_b1] = self.current_instruction.b2
    
    def execute_add_register(self):
        print("Add Register: " + str(self.current_instruction.lower_b1))
        self.chip8.registers[self.current_instruction.lower_b1] += self.current_instruction.b2
        self.chip8.registers[self.current_instruction.lower_b1] &= 0xFF 
        
    def execute_set_index_register(self):
        print("SET Index REGISTER" + str ((self.current_instruction.lower_b1 << 8) | self.current_instruction.b2))
        self.chip8.index_register = (self.current_instruction.lower_b1 << 8) | self.current_instruction.b2
        
    
    def execute_clear(self):
        print("CLEAR")
        self.display.clear()
        
    def execute_display(self):
        print("DISPLAY")
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
            
        self.chip8.registers[self.current_instruction.lower_b1] = z
        self.chip8.registers[self.current_instruction.lower_b1] &= 0xFF 
    
    def execute_substract(self):
        x = self.chip8.registers[self.current_instruction.lower_b1]
        y = self.chip8.registers[self.current_instruction.upper_b2]
        
        if x > y:
            self.chip8.registers[0xf] = 1
        else:
            self.chip8.registers[0xf] = 0
        
        self.chip8.registers[self.current_instruction.lower_b1] = x - y
        self.chip8.registers[self.current_instruction.lower_b1] &= 0xFF 
    
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
    def run(self):
        while True:
            self.fetch()
            self.dispatch()
            self.execute()
            event = sdl2.SDL_Event()  
            while sdl2.SDL_PollEvent(event):
                if event.type == sdl2.SDL_QUIT:
                    return