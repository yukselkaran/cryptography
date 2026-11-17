def pad(message: bytes) -> bytes:
    msg_bit_length = len(message) * 8
    padded = message + b"\x80"
    while len(padded) % 64 != 56:
        padded += b"\x00"
    padded += msg_bit_length.to_bytes(8, "big")
    return padded
