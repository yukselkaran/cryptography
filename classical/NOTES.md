# Classical Ciphers: Caesar, Frequency Analysis, Vigenère, XOR

> I implemented every algorithm in this folder from scratch and they pass the tests (`pytest tests/test_classical.py` → 17 passed).
> These are my notes from writing them.

## Table of Contents

- [Basics: letters are numbers](#basics-letters-are-numbers)
- [Caesar cipher](#caesar-cipher)
- [Frequency analysis and chi-squared](#frequency-analysis-and-chi-squared)
- [Vigenère cipher](#vigenère-cipher)
- [XOR cipher](#xor-cipher)
- [Comparison](#comparison)
- [References](#references)

---

## Basics: letters are numbers

Computers store every letter as a number (its ASCII value). In Python, `ord()` gives the ASCII value of a letter and `chr()` turns it back into a letter. Uppercase letters start at 65, lowercase letters start at 97.

If we subtract the starting value from the ASCII value, we get the letter's **index** in the alphabet (0–25). All shifting is done on this index:

```python
index  = ord(letter) - ord('A')    # uppercase: -65
index  = ord(letter) - ord('a')    # lowercase: -97
letter = chr(index + ord('A'))     # back to a letter
```

| Letter | Index | ASCII upper | ASCII lower | | Letter | Index | ASCII upper | ASCII lower |
|:---:|:---:|:---:|:---:|---|:---:|:---:|:---:|:---:|
| A | 0 | 65 | 97 | | N | 13 | 78 | 110 |
| B | 1 | 66 | 98 | | O | 14 | 79 | 111 |
| C | 2 | 67 | 99 | | P | 15 | 80 | 112 |
| D | 3 | 68 | 100 | | Q | 16 | 81 | 113 |
| E | 4 | 69 | 101 | | R | 17 | 82 | 114 |
| F | 5 | 70 | 102 | | S | 18 | 83 | 115 |
| G | 6 | 71 | 103 | | T | 19 | 84 | 116 |
| H | 7 | 72 | 104 | | U | 20 | 85 | 117 |
| I | 8 | 73 | 105 | | V | 21 | 86 | 118 |
| J | 9 | 74 | 106 | | W | 22 | 87 | 119 |
| K | 10 | 75 | 107 | | X | 23 | 88 | 120 |
| L | 11 | 76 | 108 | | Y | 24 | 89 | 121 |
| M | 12 | 77 | 109 | | Z | 25 | 90 | 122 |

---

## Caesar cipher

### What is it?

It shifts every letter by a fixed amount (`shift`) in the alphabet. It is one of the oldest known ciphers and is named after Julius Caesar.

### How does it work?

```
encrypt:  E(x) = (x + k) mod 26
decrypt:  D(x) = (x − k) mod 26
```

`x` is the letter's index, `k` is the key (the shift amount). Non-letter characters (spaces, digits, punctuation) stay the same, and upper/lower case is kept.

**Example: `encrypt("Hello, World!", 3)`**

| Letter | H | e | l | l | o | , | ␣ | W | o | r | l | d | ! |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Index | 7 | 4 | 11 | 11 | 14 | – | – | 22 | 14 | 17 | 11 | 3 | – |
| + 3 | 10 | 7 | 14 | 14 | 17 | – | – | 25 | 17 | 20 | 14 | 6 | – |
| Result | **K** | **h** | **o** | **o** | **r** | , | ␣ | **Z** | **r** | **u** | **o** | **g** | ! |

**Example: `encrypt("allign", 5)`**

| Letter | a | l | l | i | g | n |
|---|---|---|---|---|---|---|
| ASCII (`ord()`) | 97 | 108 | 108 | 105 | 103 | 110 |
| Index (− 97) | 0 | 11 | 11 | 8 | 6 | 13 |
| (index + 5) % 26 | 5 | 16 | 16 | 13 | 11 | 18 |
| `chr(… + 97)` | **f** | **q** | **q** | **n** | **l** | **s** |

### Weaknesses

| Weakness | Explanation |
|---|---|
| **Key space is 26** | There are only 26 possible keys. `brute_force` tries all of them instantly. (For comparison, AES-128 has 2¹²⁸ keys.) |
| **Keeps letter frequencies** | Every `e` turns into the same letter. The shape of the distribution doesn't change, it only shifts. The key can be found with frequency analysis, even without trying keys. |
| **Deterministic** | The same letter always becomes the same letter. Patterns in the text (double letters, common words) are also visible in the ciphertext. |
| **One letter reveals the key** | Anyone who knows (or guesses) one letter of the plaintext can calculate the key: `k = cipher − plain (mod 26)`. |
| **No integrity** | If the ciphertext is changed on the way, there is no way to notice it. |

---

## Frequency analysis and chi-squared

### Idea

Every language has a **letter fingerprint**. Caesar changes the letters, but it doesn't change this fingerprint. It only shifts it along the alphabet.

The `ENGLISH_FREQ` table in my code comes from Robert Lewand's *Cryptological Mathematics* (2000). Sorted by frequency:

| # | Letter | % | | # | Letter | % | | # | Letter | % |
|:---:|:---:|:---:|---|:---:|:---:|:---:|---|:---:|:---:|:---:|
| 1 | **e** | 12.70 | | 10 | d | 4.25 | | 19 | p | 1.93 |
| 2 | **t** | 9.06 | | 11 | l | 4.03 | | 20 | b | 1.49 |
| 3 | **a** | 8.17 | | 12 | c | 2.78 | | 21 | v | 0.98 |
| 4 | o | 7.51 | | 13 | u | 2.76 | | 22 | k | 0.77 |
| 5 | i | 6.97 | | 14 | m | 2.41 | | 23 | j | 0.15 |
| 6 | n | 6.75 | | 15 | w | 2.36 | | 24 | x | 0.15 |
| 7 | s | 6.33 | | 16 | f | 2.23 | | 25 | q | 0.10 |
| 8 | h | 6.09 | | 17 | g | 2.02 | | 26 | z | 0.07 |
| 9 | r | 5.99 | | 18 | y | 1.97 | | | | |

Different sources give slightly different values (`e` is 12.58% in Project Gutenberg and 12.49% in Peter Norvig's Google Books analysis), because it depends on which texts were counted. The order is almost the same: **e t a o i n …**

### Simplest method: the most common letter

I encrypted a paragraph with shift 7. The most common letters in the ciphertext were exactly 7 letters after the original ones:

| Common in original | → shift 7 → | In ciphertext |
|:---:|:---:|:---:|
| e | → | **l** (most common) |
| t | → | **a** |
| r | → | **y** |
| i | → | **p** |

`l` (11) − `e` (4) = **7** → the key. But trusting a single letter is risky: in short texts, the most common letter might not be `e`. That's why we use **chi-squared**, which looks at all 26 letters at once.

### Chi-squared (χ²)

```
χ² = Σ (observed − expected)² / expected
```

**Example: `chi_squared("hello world")`** (10 letters, some rows)

| Letter | O | E | (O − E)² / E | Note |
|:---:|:---:|:---:|:---:|---|
| a | 0 | 0.817 | 0.82 | missing but expected |
| d | 1 | 0.425 | 0.78 | |
| e | 1 | 1.270 | 0.06 | almost as expected |
| h | 1 | 0.609 | 0.25 | |
| **l** | **3** | **0.403** | **16.74** | biggest penalty |
| o | 2 | 0.751 | 2.08 | |
| t | 0 | 0.906 | 0.91 | missing but expected |
| w | 1 | 0.236 | 2.47 | rare letter, even 1 is too many |
| z | 0 | 0.007 | 0.01 | missing is normal |
| | | | **Total: 28.35** | |

| Text | χ² | Letter that adds the most | Note |
|---|:---:|---|---|
| `hello world` | 28.35 | `l`: 3 found, 0.40 expected → penalty 16.74 | Letter distribution is close to normal English |
| `olssv dvysk` (same sentence, shifted by 7) | 69.27 | `v`: 2 found, 0.10 expected → penalty 36.91 | The shift created rare letters (`v`, `k`) |
| `jazz quiz` | 1815.33 | `z`: 3 found, 0.006 expected → penalty 1601 | Real English, but almost the whole score comes from one letter (`z`). The score looks at letter distribution, not meaning. |

### `crack_caesar`: breaking it without the key

`crack_caesar` tries all 26 keys, calculates the χ² score of each result and picks the smallest one.

Ciphertext: `Haahjr ha khdu, aol lultf pz jvtpun myvt aol uvyao`

| Key | χ² | Decrypted text |
|:---:|:---:|---|
| **7** | **15.6** | **Attack at dawn, the enemy is coming from the north** |
| 9 | 109.4 | Yrryai yr byul, rfc clckw gq amkgle dpmk rfc lmprf |
| 13 | 133.8 | Unnuwe un xuqh, nby yhygs cm wigcha zlig nby hilnb |
| 0 | 149.9 | Haahjr ha khdu, aol lultf pz jvtpun myvt aol uvyao |
| … | … | … |
| 10 | 1517.8 | Xqqxzh xq axtk, qeb bkbjv fp zljfkd colj qeb kloqe (worst) |

The correct key wins with a score about 7 times lower than the next best one.

### Limits of the method

| Limit | Explanation |
|---|---|
| **Short text** | With 10–20 letters the statistics are unstable, and a wrong key can win. |
| **Unusual text** | Texts full of rare letters like `jazz quiz`, or technical texts (`x-ray`), break the distribution. |
| **The language must be known** | A Turkish text needs a Turkish frequency table. |
| **Only works if the cipher keeps frequencies** | It doesn't work directly on Vigenère (we first need the key length). It doesn't work at all on modern ciphers. |

---

## Vigenère cipher

### Idea

**A Caesar cipher that shifts each letter by a different amount.** A keyword decides the shifts: the index of the key letter in the alphabet (starting from 0) is how much the text letter is shifted.

| Key letter | L | E | M | O | N |
|---|:---:|:---:|:---:|:---:|:---:|
| Shift | 11 | 4 | 12 | 14 | 13 |

### Example: `encrypt("ATTACKATDAWN", "LEMON")`

| Text | A | T | T | A | C | K | A | T | D | A | W | N |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Index | 0 | 19 | 19 | 0 | 2 | 10 | 0 | 19 | 3 | 0 | 22 | 13 |
| Key | L | E | M | O | N | L | E | M | O | N | L | E |
| Shift | 11 | 4 | 12 | 14 | 13 | 11 | 4 | 12 | 14 | 13 | 11 | 4 |
| (index + shift) % 26 | 11 | 23 | 5 | 14 | 15 | 21 | 4 | 5 | 17 | 13 | 7 | 17 |
| Result | **L** | **X** | **F** | **O** | **P** | **V** | **E** | **F** | **R** | **N** | **H** | **R** |

The first `T` became `X`, the second `T` became `F`. **The same letter turns into different letters.** This is the difference from Caesar.

### Why is it stronger than Caesar?

- The same letter turns into different letters, so the **frequency distribution gets flatter**. Simple frequency analysis doesn't work directly.
- **The key space grows:** 26ⁿ for an n-letter key. For `LEMON` it is 26⁵ = **11,881,376**. Much more than Caesar's 26, but still small for a computer.

### Weaknesses

| Weakness | Explanation |
|---|---|
| **The key repeats** | This is the main weakness. If the key length is found, the cipher falls apart. |
| **Kasiski test** | If a repeated part of the plaintext lines up with the same part of the key, it also repeats in the ciphertext. Example: `encrypt("the the the", "KEY")` → `"dlc dlc dlc"`. The distances between the repeats are multiples of the key length. |
| **Friedman test (index of coincidence)** | The probability that two randomly picked letters are the same. About 0.065 in normal English (0.0655 using `ENGLISH_FREQ`), and 1/26 ≈ 0.0385 in fully random text. The value of the ciphertext helps estimate the key length. |
| **Known key length = n Caesar ciphers** | If the key has 5 letters, the 1st, 6th, 11th… letters are all encrypted with the same Caesar shift. If I split the text into 5 columns and run my `crack_caesar` on each column, I find each letter of the key one by one. |
| **Short key** | The shorter the key, the more it repeats and the easier it is to break. |
| **Known plaintext** | If part of the plaintext is known, that part of the key comes out directly: `key = cipher − plain (mod 26)`. |

---

## XOR cipher

### Idea

We XOR the data with a repeating key, character by character. The ASCII value of each character is used as an 8-bit binary number. XOR compares two bits: **1 if they are different, 0 if they are the same.** XORing again with the same key gives back the data, so encryption and decryption are the same function.

### Example: `xor_bytes(b"Burning", b"ICE")`

The key repeats with `key[i % len(key)]`: I, C, E, I, C, E, I…

| i | Data | ASCII (decimal) | Binary | Key | ASCII (decimal) | Binary | XOR (binary) | Result (decimal) | Result (hex) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | B | 66 | `01000010` | I | 73 | `01001001` | `00001011` | 11 | **0b** |
| 1 | u | 117 | `01110101` | C | 67 | `01000011` | `00110110` | 54 | **36** |
| 2 | r | 114 | `01110010` | E | 69 | `01000101` | `00110111` | 55 | **37** |
| 3 | n | 110 | `01101110` | I | 73 | `01001001` | `00100111` | 39 | **27** |
| 4 | i | 105 | `01101001` | C | 67 | `01000011` | `00101010` | 42 | **2a** |
| 5 | n | 110 | `01101110` | E | 69 | `01000101` | `00101011` | 43 | **2b** |
| 6 | g | 103 | `01100111` | I | 73 | `01001001` | `00101110` | 46 | **2e** |

Result: `0b3637272a2b2e`. This matches the first 7 values of the Cryptopals test vector in the tests.

### One-Time Pad: the unbreakable version of XOR

If the key meets these four rules, the XOR cipher is **theoretically unbreakable** (Vernam built his machine in 1917, and Shannon proved mathematically in 1949 that it can't be broken):

1. Completely **random**
2. At least **as long as the message**
3. Used **only once**
4. Kept **secret**

In practice it is hard: safely sending a random key as long as the message to the other side is as hard as sending the message itself.

### Weaknesses (repeating-key XOR)

| Weakness | Explanation | Example |
|---|---|---|
| **The key repeats** | It is the binary version of Vigenère. The key length can be found (with Hamming distance), and then each position can be broken separately as XOR with a one-character key. For each column we try all 256 possible key characters and pick the best one with `chi_squared`. | Cryptopals 3 and 6 |
| **Reusing the key** | If two messages are encrypted with the same key, the key cancels out: `c1 ^ c2 = p1 ^ p2`. Information about both plaintexts leaks without knowing the key. | I tested it with `"attack at dawn"` and `"defend at dusk"`: `c1 ^ c2 == p1 ^ p2` → `True` |
| **Known plaintext** | If part of the plaintext is known, the key comes out directly: `p ^ c = key`. | XOR of `b"Burn"` and the first 4 characters of the ciphertext → `b"ICEI"` |
| **No integrity (bit flipping)** | Flipping a bit in the ciphertext flips the same bit in the plaintext. An attacker can change the message without knowing the key. | Changing the value of one character in the encrypted `"PAY 100 TL"` → it decrypts as `"PAY 900 TL"` |
| **Key distribution** | One-Time Pad is secure, but sharing a long key is not practical. | |

### Where it is used in modern cryptography

XOR is everywhere in modern cryptography. The difference is that the key is not short and repeating. It is a **random-looking key stream produced by a good algorithm**:

- **AES:** The `AddRoundKey` step XORs the state with the round key.
- **CTR mode and ChaCha20:** They XOR the generated key stream with the data. It is the same thing we do here, but the key never repeats.
- **GCM and Poly1305:** They add an authentication tag to the encryption to close the bit flipping weakness.

---

## Comparison

| | Caesar | Vigenère | Repeating-key XOR | One-Time Pad |
|---|---|---|---|---|
| **Unit** | Letter (A–Z) | Letter (A–Z) | 8-bit value of a character (0–255) | 8-bit value of a character (0–255) |
| **Operation** | Fixed shift | Changing shift | Bitwise XOR | Bitwise XOR |
| **Key** | 1 number (0–25) | Word | Short string (e.g. `ICE` = 73, 67, 69) | Random values as long as the message |
| **Key space** | 26 | 26ⁿ | 256ⁿ | 256^(message length) |
| **Same input → same output?** | Yes, everywhere | Only at the same position | Only at the same position | No |
| **Keeps frequencies?** | Yes (shifted) | Partly (per column) | Partly (per column) | No |
| **How to break it?** | Brute force / frequency analysis | Kasiski + Friedman + frequency analysis per column | Hamming distance + frequency analysis per column | Can't be broken (if the rules are followed) |
| **Integrity?** | None | None | None | None |

---

## References

- Robert Lewand, *Cryptological Mathematics* (2000): English letter frequency table
- [Lewand's frequency tables (HKUST)](https://cse.hkust.edu.hk/emb/itepc2006/itepc04/Presentations/freq_table.pdf)
- [Peter Norvig, English Letter Frequency Counts: Mayzner Revisited](https://norvig.com/mayzner.html)
- [Frequency analysis (Wikipedia)](https://en.wikipedia.org/wiki/Frequency_analysis)
- [Simon Singh, Arab Code Breakers](https://simonsingh.net/media/articles/maths-and-science/arab-code-breakers)
- Simon Singh, *The Code Book*: history from Caesar to Vigenère
- [Cryptopals Set 1](https://cryptopals.com/sets/1): especially 3 (single-character XOR), 5 (repeating-key XOR) and 6 (breaking repeating-key XOR)
