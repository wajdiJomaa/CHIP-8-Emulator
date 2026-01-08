from enum import Enum, auto

class Instruction:
    def __init__(self, b1, b2):
        self.b1 = b1
        self.b2 = b2
    
        self.upper_b1 = (b1 & 0xF0) >> 4
        self.lower_b1 = b1 & 0x0F 
        
        self.upper_b2 = (b2 & 0xF0) >> 4
        self.lower_b2 = b2 & 0x0F
        
        self.t = None
        
class InstructionType(Enum):
    CLEAR = auto()
    JUMP = auto()
    SET_REGISTER = auto()
    ADD_REGISTER = auto()
    SET_INDEX_REGISTER = auto()
    DISPLAY = auto()
    UNKNOWN = auto()
    CALL = auto()
    RETURN = auto()
    JUMP_EQ_NN = auto()
    JUMP_NEQ_NN = auto()
    JUMP_EQ = auto()
    JUMP_NEQ = auto()
    COPY = auto()
    BINARY_OR = auto()
    BINARY_AND = auto()
    LOGICAL_XOR = auto()
    ADD = auto()
    SUBTRACT = auto()
    SHIFT = auto()