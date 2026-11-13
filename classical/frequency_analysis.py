from classical.caesar import decrypt

ENGLISH_FREQ = {
    "a": 8.17, "b": 1.49, "c": 2.78, "d": 4.25, "e": 12.70, "f": 2.23,
    "g": 2.02, "h": 6.09, "i": 6.97, "j": 0.15, "k": 0.77, "l": 4.03,
    "m": 2.41, "n": 6.75, "o": 7.51, "p": 1.93, "q": 0.10, "r": 5.99,
    "s": 6.33, "t": 9.06, "u": 2.76, "v": 0.98, "w": 2.36, "x": 0.15,
    "y": 1.97, "z": 0.07,
}


def letter_frequencies(text):
    letters = {}
    for letter in text: 
        if letter.isalpha():
            letter = letter.lower()
            if letter in letters:
                letters[letter] += 1
            else:
                letters[letter] = 1
        else: 
            continue
    total = sum(letters.values())
    if total == 0:
        return {}
    frequencies = {}
    for letter in letters:
        frequencies[letter] = letters[letter] / total
    return frequencies


def chi_squared(text):
    letters = {}
    for letter in text: 
        if letter.isalpha():
            letter = letter.lower()
            if letter in letters:
                letters[letter] += 1
            else:
                letters[letter] = 1
        else: 
            continue

    total = sum(letters.values())
    if total == 0:
        return float("inf")
    
    score = 0
    for letter in ENGLISH_FREQ:
        observed = letters.get(letter,0)
        expected = total * ENGLISH_FREQ[letter] / 100
        penalty = (observed - expected) ** 2 / expected
        score += penalty
    return score


def crack_caesar(ciphertext):
    best_shift = 0
    best_score = float("inf")
    for shift in range(26):
        candidate = decrypt(ciphertext,shift)
        score = chi_squared(candidate)
        if score < best_score:
            best_score = score
            best_shift = shift
    return best_shift
