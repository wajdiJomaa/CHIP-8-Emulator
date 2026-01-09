import chip8
import display
import instrucionExecutor

chip = chip8.Chip8()
disp = display.Display()

chip.load_program("roms/7-beep.ch8")
executor = instrucionExecutor.InstructionExecutor(chip, disp)
executor.run()