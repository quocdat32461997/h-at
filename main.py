# import dependencies
import os
import argparse

def get_args():
    #initialize argument parser
    parser = argparse.ArgumentParser('Argument Paser for h-at, an Information Extraction tool')

    # add arguments
    parser.add_argument('--input', type = str, help = 'Text input')

    return parser.parse_args()

def main(args):
    return None

if __name__ == '__main__':
    # get args
    args = get_args()

    # execution
    main(args)
