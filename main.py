import chip8
import display
import instrucionExecutor
import sys
chip = chip8.Chip8()
disp = display.Display()

chip.load_program(sys.argv[1])
executor = instrucionExecutor.InstructionExecutor(chip, disp)
executor.run()