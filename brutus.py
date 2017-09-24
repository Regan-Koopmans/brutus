#!/bin/python

import string
import time
import argparse
from random import randint
from nltk import ngrams
from itertools import permutations
from colorama import init, Fore, Style

# This is a list in which the decryption candidates are stored.
# Global variables are generally considered bad, but this may
# allow us to parallelise the code at a later stage.
decryption_candidates = []
output = ""
english_ngrams = []

def populate_english_ngrams(filename):
    global english_ngrams
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            english_ngrams += ngramize(line, 2)
            english_ngrams += ngramize(line, 3)
    english_ngrams = set(english_ngrams)

def encrypt(input):
    permutation_number = randint(0,5)
    permutation = ''.join([p for p in permutations([string.ascii_lowercase,string.ascii_uppercase,'0123456789'])][permutation_number])
    offset = randint(1,62)
    encrypted = ''.join([permutation[(permutation.index(letter) + offset) % 62] for letter in input])
    print(encrypted)
    print("Encryption key : [" + str(permutation_number) + ";" + str(offset) + "]")
    write_encrypted(encrypted)
    print(Fore.GREEN + "Wrote encryption results to " + output + Style.RESET_ALL)

def decrypt(input):
    global output
    global decryption_candidates
    largest_trigram_candidate = None
    largest_trigram_count = 0
    decryption_candidates = []
    for domain in permutations([string.ascii_lowercase,string.ascii_uppercase,'0123456789']):
        domain = ''.join(domain)
        for offset in range(62):
            candidate = ''.join([domain[(domain.index(letter) + offset) % 62] for letter in input])
            decryption_candidates.append(candidate)
            trigram_count = count_trigram_match(candidate)
            if trigram_count > largest_trigram_count:
                largest_trigram_candidate = candidate
                largest_trigram_count = trigram_count
                print(end="\r")
                print(candidate, end="")

    print("")
    print("I believe it is the following message:")
    print(largest_trigram_candidate)
    write_log(output)
    print(Fore.GREEN + "Wrote decryption results to " + output + Style.RESET_ALL)

def write_encrypted(input):
    global output
    with open(output, 'w') as f:
        f.write(input)

def write_log(filename):
    with open(filename, 'w') as f:
        for x in range(len(decryption_candidates)):
            f.write(str(x) + " : " + decryption_candidates[x] + "\n\n")

def count_trigram_match(text):
    count = 0
    trigrams = ngramize(text.lower(), 3) + \
               ngramize(text.lower(), 2)
    for trigram in english_ngrams:
        count += trigrams.count(trigram)
    return count

def ngramize(text, n):
    output = []
    output += ngrams(text, n)
    return output

def main():
    global output
    init()
    populate_english_ngrams("dictionaries/wordsEn.txt")
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
    file = open(args.file, "r")
    if mode == "Decrypting ":
        decrypt(file.read())
        write_log(output)
    else:
        output = args.file + ".caesar"
        encrypt(file.read())


if __name__ == "__main__":
    main()