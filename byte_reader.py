'''
Byte reader module

FUNCTIONS OFFERED:
1. Read bytes depending on input endian
2. Convert little endian bytearray to big_endian bytearray
3. Convert bytearray to INT
'''
from mathematics import *

'''
read_byte(file_desc , num_of_bytes, endian)
Read num_of_bytes bytes from file_desc depending on big or small endian
endian = 1 for BIG ENDIAN
'''
def read_byte (file_desc, num_of_bytes, endian):
    BIG = 1
    bytes = file_desc.read(num_of_bytes)
    if endian != BIG:
        bytes = to_big_endian(bytes)
    return bytes

# Helper function to reverse order of bytearray
def to_big_endian (byte_arr):
    to_return = list(byte_arr)
    to_return.reverse()
    return(bytes(to_return))

# Helper function to convert bytearray and return an INT
def bytearr_to_int (byte_arr):
    ret_int = 0
    for thing in byte_arr:
        ret_int = ret_int * 256 + thing
    return(ret_int)
