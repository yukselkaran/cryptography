import pytest

from classical import caesar, vigenere, xor_cipher, frequency_analysis


# ---------- Caesar ----------

def test_caesar_encrypt():
    assert caesar.encrypt("Hello, World!", 3) == "Khoor, Zruog!"


def test_caesar_wraps_around():
    assert caesar.encrypt("xyz XYZ", 3) == "abc ABC"


def test_caesar_large_and_negative_shift():
    assert caesar.encrypt("abc", 29) == caesar.encrypt("abc", 3)
    assert caesar.encrypt("abc", -1) == "zab"


def test_caesar_roundtrip():
    msg = "Saldiri safakta baslayacak! 123"
    for s in range(26):
        assert caesar.decrypt(caesar.encrypt(msg, s), s) == msg


def test_caesar_brute_force():
    results = caesar.brute_force("Khoor, Zruog!")
    assert len(results) == 26
    assert results[3] == (3, "Hello, World!")


# ---------- Vigenère ----------

def test_vigenere_classic():
    assert vigenere.encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"


def test_vigenere_keeps_case_and_skips_non_letters():
    assert vigenere.encrypt("Attack at dawn!", "lemon") == "Lxfopv ef rnhr!"


def test_vigenere_roundtrip():
    msg = "The quick brown fox jumps over the lazy dog."
    assert vigenere.decrypt(vigenere.encrypt(msg, "Secret"), "Secret") == msg


# ---------- XOR ----------

def test_xor_cryptopals_challenge_5():
    pt = (b"Burning 'em, if you ain't quick and nimble\n"
          b"I go crazy when I hear a cymbal")
    expected = ("0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20"
                "430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")
    assert xor_cipher.xor_bytes(pt, b"ICE").hex() == expected


def test_xor_is_its_own_inverse():
    data = bytes(range(100))
    key = b"\x13\x37\xbe\xef"
    assert xor_cipher.xor_bytes(xor_cipher.xor_bytes(data, key), key) == data


def test_xor_empty_key():
    with pytest.raises(ValueError):
        xor_cipher.xor_bytes(b"abc", b"")


# ---------- Frequency Analysis ----------

SAMPLE = (
    "Cryptography is the practice and study of techniques for secure communication "
    "in the presence of adversarial behavior. More generally, cryptography is about "
    "constructing and analyzing protocols that prevent third parties or the public "
    "from reading private messages. Modern cryptography exists at the intersection "
    "of the disciplines of mathematics, computer science, and electrical engineering."
)


def test_letter_frequencies_simple():
    f = frequency_analysis.letter_frequencies("aAb!")
    assert set(f) == {"a", "b"}
    assert f["a"] == pytest.approx(2 / 3)
    assert f["b"] == pytest.approx(1 / 3)


def test_chi_squared_prefers_english():
    english = frequency_analysis.chi_squared(SAMPLE)
    gibberish = frequency_analysis.chi_squared(caesar.encrypt(SAMPLE, 11))
    assert english < gibberish


@pytest.mark.parametrize("shift", [1, 7, 13, 25])
def test_crack_caesar(shift):
    assert frequency_analysis.crack_caesar(caesar.encrypt(SAMPLE, shift)) == shift
