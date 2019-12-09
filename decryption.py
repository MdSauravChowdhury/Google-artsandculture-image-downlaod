#!/usr/bin/env python3
# coding: utf-8
import struct
from Crypto.Cipher import AES

aes_key = bytes.fromhex('5b63db113b7af3e0b1435556c8f9530c')
aes_iv = bytes.fromhex('71e70405353a778bfa6fbc30321b9592')


def aes_decrypt_buffer(buffer):
    """
    >>> aes_decrypt_buffer(b"0123456789abcdef"*2).hex()
    'a35fd5bfdb47815bcbe4b39e596a9358e289e389da48c0e709b26ecc081563ac'
    """
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_iv)
    return cipher.decrypt(buffer)


def split_buffer_in_3(buf, idx1, idx2):
    return buf[:idx1], buf[idx1:idx2], buf[idx2:]


def decrypt(image):
    """
    >>> x = "0A0A0A0A BABAC0C0 10000000 01010101 01010101 01010101 01010101 DEADBEAF 04000000"
    >>> decrypt(bytes.fromhex(x)).hex()
    'babac0c0ca251118030ff9aff186bdccbce26a4cdeadbeaf'
    """
    # The file is composed of a constant header, a body,
    # and a last 4-byte word indicating the start of the encrypted part
    encryption_marker, body, index_bytes = split_buffer_in_3(image, 4, -4)

    # return if the encryption marker isn't present at the start of the file
    if encryption_marker != b"\x0A\x0A\x0A\x0A":
        return image

    # Use the last 4 bytes to get the index of the bytes to be replaced
    (index,) = struct.unpack("<i", index_bytes)

    clear_prefix, replace_count_bytes, rest = split_buffer_in_3(body, index, index + 4)

    # How many bytes to replace
    (replace_count,) = struct.unpack("<i", replace_count_bytes)

    _, encrypted, clear_suffix = split_buffer_in_3(rest, 0, replace_count)

    # Convert back into bytes
    return b"".join((clear_prefix, aes_decrypt_buffer(encrypted), clear_suffix))
