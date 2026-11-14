def xor_bytes(data: bytes, key: bytes) -> bytes:
    if len(key) == 0:
        raise ValueError("Key can not be empty")
    
    result = []
    for i,byte in enumerate(data): # gives both i.th and byte of 
        key_byte = key[i % len(key)]
        new_byte = byte ^ key_byte
        result.append(new_byte)
    return bytes(result)
"""
to decrypt this data we just need to xor
encrypted data with the key.
according to xor rules: 
a ^ a = 0 
a ^ 0 = a
(a ^ k) ^ k = a ^ (k ^ k) = a ^ 0 = a
"""

