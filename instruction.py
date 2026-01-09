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
    ISUBTRACT = auto()
    LSHIFT = auto()
    RSHIFT = auto()
    RANDOM = auto()
    JUMP_OFFSET = auto()
    ADD_INDEX = auto()
    GET_KEY = auto()
    SKIP_IF_KEY = auto()
    SKIP_IF_NOT_KEY = auto()
    BINARY_CODED_DECIMAL = auto()
    FONT = auto()
    STORE = auto()
    LOAD = auto()
    SET_DELAY_TIMER = auto()
    READ_DELAY_TIMER = auto()
    SET_BEAP_TIMER = auto()