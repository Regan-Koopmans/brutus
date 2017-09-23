#!/bin/python

import argparse
from colorama import init, Fore, Style

def decrypt():
    pass

def main():
    init()
    args = []
    mode = ""
    output = "decrypt.out"
    parser = argparse.ArgumentParser(description="A Caesar Encryption Suite.")
    parser.add_argument('file', metavar='file', help='The file to run brutus on.')
    parser.add_argument('-d', dest='decrypt', action='store_const', const="decrypt", help='decrypt the file.')
    parser.add_argument('-e', dest='encrypt', action='store_const', const="encrypt", help='encrypt the file.')
    parser.add_argument('-nlp', dest='nlp', action='store_const', const="nlp", help='use natural language processing.')
    parser.add_argument('-o', dest='output', help='location to store decryption output.')
    args = parser.parse_args()
    output = args.output if args.output is not None else output
    mode = "Decrypting " if args.encrypt == None else "Encrypting "
    print(Fore.GREEN + mode + args.file + Style.RESET_ALL)
    log = decrypt()
    print(Fore.GREEN + "Writing results to "+ output + Style.RESET_ALL)


if __name__ == "__main__":
    main()