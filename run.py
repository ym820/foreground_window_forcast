import sys
import os

def main(args):
    mode = args[0]
    model = args[1].upper()
    if mode == 'test':
        os.system(f"cd src/model/{model}; python3 run.py -td True")
    else:
        os.system(f'cd src/model/{model}; python3 run.py')

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)