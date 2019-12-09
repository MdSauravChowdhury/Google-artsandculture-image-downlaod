from decryption import decrypt
import sys
import os

input = sys.argv[1]
output = sys.argv[2]

image = open(input, "rb").read()

image = decrypt(image)

open(output, "wb").write(image)

print(f"Decrypted {os.path.basename(input)} to {os.path.basename(output)}.")
