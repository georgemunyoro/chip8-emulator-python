from math import pi
from random import randrange
import pygame
import sys
import time


class Chip8:

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self) -> None:
        self.memory = [0] * 4096
        self.V = [0] * 16
        self.I = 0
        self.display = [0] * (64 * 32)
        self.screen = [[0] * 64] * 32
        self.dt = 0
        self.st = 0
        self.pc = 0

        self.stack = [0] * 16
        self.sp = 0

        self.kb = [0] * 16

        self.window = None

    @staticmethod
    def msb(n: int) -> int:
        if n == 0:
            return 0
        r = 0
        n = n / 2
        while n != 0:
            n = n / 2
            r += 1

        return 1 << n

    def load_rom(self, rom_filepath: str) -> None:
        with open(rom_filepath, "rb") as rom_file:
            rom_contents = rom_file.read()
            for i, j in enumerate(rom_contents):
                self.memory[0x200 + i] = j

    def run(self):
        self.pc = 0x200

        pygame.init()
        self.window = pygame.display.set_mode((640, 320))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_1:
                        self.kb[0x1] = 1
                    elif event.key == pygame.K_2:
                        self.kb[0x2] = 1
                    elif event.key == pygame.K_3:
                        self.kb[0x3] = 1
                    elif event.key == pygame.K_4:
                        self.kb[0xC] = 1
                    elif event.key == pygame.K_q:
                        self.kb[0x4] = 1
                    elif event.key == pygame.K_w:
                        self.kb[0x5] = 1
                    elif event.key == pygame.K_e:
                        self.kb[0x6] = 1
                    elif event.key == pygame.K_r:
                        self.kb[0xD] = 1
                    elif event.key == pygame.K_a:
                        self.kb[0x7] = 1
                    elif event.key == pygame.K_s:
                        self.kb[0x8] = 1
                    elif event.key == pygame.K_d:
                        self.kb[0x9] = 1
                    elif event.key == pygame.K_f:
                        self.kb[0xE] = 1
                    elif event.key == pygame.K_z:
                        self.kb[0xA] = 1
                    elif event.key == pygame.K_x:
                        self.kb[0x0] = 1
                    elif event.key == pygame.K_c:
                        self.kb[0xB] = 1
                    elif event.key == pygame.K_v:
                        self.kb[0xF] = 1

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_1:
                        self.kb[0x1] = 0
                    elif event.key == pygame.K_2:
                        self.kb[0x2] = 0
                    elif event.key == pygame.K_3:
                        self.kb[0x3] = 0
                    elif event.key == pygame.K_4:
                        self.kb[0xC] = 0
                    elif event.key == pygame.K_q:
                        self.kb[0x4] = 0
                    elif event.key == pygame.K_w:
                        self.kb[0x5] = 0
                    elif event.key == pygame.K_e:
                        self.kb[0x6] = 0
                    elif event.key == pygame.K_r:
                        self.kb[0xD] = 0
                    elif event.key == pygame.K_a:
                        self.kb[0x7] = 0
                    elif event.key == pygame.K_s:
                        self.kb[0x8] = 0
                    elif event.key == pygame.K_d:
                        self.kb[0x9] = 0
                    elif event.key == pygame.K_f:
                        self.kb[0xE] = 0
                    elif event.key == pygame.K_z:
                        self.kb[0xA] = 0
                    elif event.key == pygame.K_x:
                        self.kb[0x0] = 0
                    elif event.key == pygame.K_c:
                        self.kb[0xB] = 0
                    elif event.key == pygame.K_v:
                        self.kb[0xF] = 0

            pygame.display.update()
            self.cycle()
            time.sleep(0.001)

    def render(self):
        self.window.fill(Chip8.BLACK)
        for i in range(32):
            for j in range(64):
                p = self.display[i * 64 + j]
                if p == 1:
                    pygame.draw.rect(
                        self.window,
                        Chip8.WHITE,
                        ((j * 10, i * 10), (10, 10)),
                    )

    def cycle(self):
        opcode = (self.memory[self.pc] << 8) | (self.memory[self.pc + 1])
        self.pc += 2

        if opcode == 0x00E0:
            self.display = [0] * (64 * 32)

        elif opcode == 0x00EE:
            self.pc = self.stack[self.sp]
            self.sp -= 1

        elif (opcode >> 12) == 1:
            self.pc = opcode & 0xFFF

        elif (opcode >> 12) == 2:
            self.sp += 1
            self.stack[self.sp] = self.pc
            self.pc = opcode & 0xFFF

        elif (opcode >> 12) == 3:
            if (self.V[(opcode >> 8) & 0xF]) == (opcode & 0xFF):
                self.pc += 2

        elif (opcode >> 12) == 4:
            if (self.V[(opcode >> 8) & 0xF]) != (opcode & 0xFF):
                self.pc += 2

        elif (opcode >> 12) == 5:
            if (self.V[(opcode >> 8) & 0xF]) == (self.V[(opcode >> 4) & 0xF]):
                self.pc += 2

        elif (opcode >> 12) == 6:
            self.V[(opcode >> 8) & 0xF] = opcode & 0xFF

        elif (opcode >> 12) == 7:
            self.V[(opcode >> 8) & 0xF] += opcode & 0xFF

        elif (opcode >> 12) == 8:
            x = (opcode >> 8) & 0xF
            y = (opcode >> 4) & 0xF

            if (opcode & 0xF) == 0:
                self.V[x] = self.V[y]

            elif (opcode & 0xF) == 1:
                self.V[x] = self.V[x] | self.V[y]

            elif (opcode & 0xF) == 2:
                self.V[x] = self.V[x] & self.V[y]

            elif (opcode & 0xF) == 3:
                self.V[x] = self.V[x] ^ self.V[y]

            elif (opcode & 0xF) == 4:
                if (self.V[x] + self.V[y]) > 0xFF:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0

                self.V[x] = (self.V[x] + self.V[y]) & 0xFF

            elif (opcode & 0xF) == 5:
                if self.V[x] > self.V[y]:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0

                self.V[x] -= self.V[y]

            elif (opcode & 0xF) == 6:
                if self.V[x] & 1 == 1:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0

                self.V[x] /= 2

            elif (opcode & 0xF) == 7:
                if self.V[y] > self.V[x]:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0

                self.V[y] -= self.V[x]

            elif (opcode & 0xF) == 0xE:
                if Chip8.msb(self.V[x]) == 1:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0

                self.V[x] *= 2

        elif (opcode >> 12) == 9:
            if self.V[(opcode >> 8) & 0xF] != self.V[(opcode >> 4) & 0xF]:
                self.pc += 2

        elif (opcode >> 12) == 0xA:
            self.I = opcode & 0xFFF

        elif (opcode >> 12) == 0xB:
            self.pc = (opcode & 0xFFF) + self.V[0]

        elif (opcode >> 12) == 0xC:
            rand_byte = randrange(0, 0xFF)
            self.V[(opcode >> 8) & 0xF] = rand_byte & (opcode & 0xFF)

        elif (opcode >> 12) == 0xD:
            x = (opcode >> 8) & 0xF
            y = (opcode >> 4) & 0xF
            self.V[0xF] = 0

            for i in range(opcode & 0xF):
                sprite_byte = self.memory[self.I + i]
                for j in range(8):

                    x_coord = (self.V[x] + j) % 64
                    y_coord = (self.V[y] + i) % 32
                    pindex = y_coord * 64 + x_coord

                    bit = sprite_byte >> (7 - j) & 1
                    if bit == 1:
                        if self.display[pindex] == 1:
                            self.V[0xF] = 1

                        self.display[pindex] ^= 1
            self.render()

        elif (opcode >> 12) == 0xE:
            x = (opcode >> 8) & 0xF

            if (opcode & 0xFF) == 0x9E:
                if self.kb[self.V[x]] == 1:
                    self.pc += 2

            elif (opcode & 0xFF) == 0xA1:
                try:
                    if self.kb[self.V[x]] == 0:
                        self.pc += 2
                except:
                    pass

        elif (opcode >> 12) == 0xF:
            x = (opcode >> 8) & 0xF

            if (opcode & 0xFF) == 0x07:
                self.V[x] = self.dt

            elif (opcode & 0xFF) == 0x0A:
                while True:
                    for i, j in enumerate(self.kb):
                        if j == 1:
                            self.V[x] = i
                            continue

            elif (opcode & 0xFF) == 0x15:
                self.dt = self.V[x]

            elif (opcode & 0xFF) == 0x18:
                self.st = self.V[x]

            elif (opcode & 0xFF) == 0x1E:
                self.I += self.V[x]

            elif (opcode & 0xFF) == 0x29:
                self.I = self.V[x]

            elif (opcode & 0xFF) == 0x33:
                self.memory[self.I] = int(("00" + str(self.V[x]))[-3])
                self.memory[self.I + 1] = int(("000" + str(self.V[x]))[-2])
                self.memory[self.I + 2] = int(("000" + str(self.V[x]))[-1])

            elif (opcode & 0xFF) == 0x55:
                for i in range(self.I, self.I + x):
                    self.memory[i] = self.V[i - self.I]

            elif (opcode & 0xFF) == 0x65:
                for i in range(self.I, self.I + x):
                    self.V[i - self.I] = self.memory[i]

        if self.dt > 0:
            self.dt -= 1

        if self.st > 0:
            self.st -= 1
            if self.st == 0:
                print("\a")


def main():
    if len(sys.argv) != 2:
        print("\nIncorrect usage.")
        quit()

    chip = Chip8()
    chip.load_rom(sys.argv[1])
    chip.run()


if __name__ == "__main__":
    main()
