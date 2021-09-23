import encryptionSystem as es
import argparse

parser = argparse.ArgumentParser(description='Check the encrypted data of the Hand Tracking Software')
parser.add_argument("-file", "--print_string", help="Data file to read and print", default="accounts")
args = parser.parse_args()

File = open("data\\{}".format(args.print_string), "r")
Contents = File.readlines()
Lines = []
for line in Contents:
    Lines.append(es.decrypt_message(line))
Contents = "\n".join(Lines)
print("\n{}\n".format(Contents))
