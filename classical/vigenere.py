from classical.caesar import encrypt as caesar_encrypt
from classical.caesar import decrypt as caesar_decrypt

def encrypt(text,key):
    result = []
    counter = 0
    for letter in text:
        if letter.isalpha():
            key_letter = key[counter % len(key)].lower()
            shift = ord(key_letter) - ord('a')
            result.append(caesar_encrypt(letter,shift))
            counter += 1
        else:
            result.append(letter)
    return "".join(result)
            
        

def decrypt(text, key):
    result = []
    counter = 0
    for letter in text:
        if letter.isalpha():
            key_letter = key[counter % len(key)].lower()
            shift = ord(key_letter) - ord('a')
            result.append(caesar_decrypt(letter,shift))
            counter += 1
        else:
            result.append(letter)
    return "".join(result)
          
