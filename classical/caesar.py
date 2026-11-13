def encrypt(text,shift):
    result = []
    for letter in text:
        if 'A' <= letter <= 'Z':
            order = ord(letter) - ord('A')
            shifted_order = (order + shift) % 26
            result.append(chr(shifted_order + ord('A')))

        elif 'a' <= letter <= 'z':
            order = ord(letter) - ord('a')
            shifted_order = (order + shift) % 26
            result.append(chr(shifted_order + ord('a')))

        else: 
            result.append(letter)
            
    return "".join(result)   


def decrypt(text,shift):
    return encrypt(text,-shift)


def brute_force(ciphertext):
    results = []
    for shift in range(26):
        results.append((shift,decrypt(ciphertext,shift))) # adding a tuple element to the list.
    return results