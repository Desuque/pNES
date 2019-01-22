import argparse

from cpu import CPU
from rom import ROM
from ram import RAM
from ppu import PPU


def main():
    parser = argparse.ArgumentParser(description='NesEmulator :)')
    parser.add_argument('rom_path',
                        metavar='R',
                        type=str,
                        help='Path to the NES ROM')

    args = parser.parse_args()

    # TODO: Implement drag and drop rom system
    print(args.rom_path)

    with open(args.rom_path, 'rb') as file:
        rom_bytes = file.read()

        rom = ROM(rom_bytes)

        ram = RAM()
        ppu = PPU()

        cpu = CPU(ram, ppu)
        cpu.start_up()
        cpu.run_rom(rom)

        print("Hola mundo!, se viene un emulador interesante :D")
        print("Cambio esta linea solo para ver si GitHub quedo bien configurado")

if __name__ == '__main__':
    main()
