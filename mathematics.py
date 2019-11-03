'''
Data type converter module

Python can have binary/hex/decimal int
Python read in bytes datatype which is basically int array

FUNCTIONS OFFERED:
1. Int to DEC/0xHEX/HEX string
2. 0xHEX/xHex string to int
'''

'''
int_str(input,choice)
Convert non-negative INT input and return STRING
Choice determines what type to convert to:
CHOICE 1 for DEC string
CHOICE 2 for HEX string
CHOICE 3 for HEX string without 0x prefix
'''
def int_str(input ,choice):
    final_string = ''
    value = input

    # Check if input is non-zero
    if (input < 0):
        print('Zero and positive value only')
        return

    # Convert INT to DEC string
    if(choice == 1):
        # Special case when input is 0
        if(input == 0):
            return '0'
        # Iterate over the whole number
        while ( value % 10 != 0 ):
            # Append num from right to left
            final_string += (chr(value % 10 + 48))
            value = value // 10

    #Convert INT to HEX string
    elif(choice == 2):
        # Special case when input is 0
        if(input == 0):
            return '0x00'

        # Iterate over the whole number
        while (((value % 16) != 0) or ((value // 16) != 0)):
            # If digit 0-9 then add 48 to get and append correct ASCII value
            if(value % 16 < 10):
                final_string += (chr(value % 16 + 48))
            # If digit a-f then add 87 to get and append correct ASCII value
            else:
                final_string += (chr(value % 16 + 87))
            value = value // 16
        final_string += 'x0'

    # Convert INT to HEX string without 0x
    elif(choice == 3):
        # Special case when input is 0
        if(input == 0):
            return '00'

        # Iterate over the whole number
        while (((value % 16) != 0) or ((value // 16) != 0)):
            # If digit 0-9 then add 48 to get and append correct ASCII value
            if(value%16 < 10):
                final_string += (chr(value % 16 + 48))
            # If digit 0-9 then add 48 to get and append correct ASCII value
            else:
                final_string += (chr(value % 16 + 87))
            value = value//16
    # Expand more choice here

    # Reverse final_string before returning
    return(reverse_str(final_string))



'''
str_int (input,choice)

Convert STRING input and return INT
Choice determines what to convert from
CHOICE 1 for HEX string
'''
def str_int (input,choice):
    # Convert input to lowercase to generalize
    opt_string = input.lower()
    return_value = 0
    # Convert from HEX string
    if(choice == 1):
        # Input must be at least 3char long : x00 or 0x00
        if len(input) < 3 :
            print('Check input')
            return

        # Find starting hex index Ex: 0xab -> 2, xff -> 1
        starting_index = input.find('x') + 1
        # Find number of hex digits
        bits = len(opt_string) - starting_index
        # Power coressponding to hex bit
        power = bits - 1

        for i in range(starting_index, starting_index + bits):
            # If digits is 0-9
            if (ord(opt_string[i]) < 97):
                return_value += (ord(opt_string[i]) - 48) * (16**power)
            # If digits is a-f
            else:
                return_value += (ord(opt_string[i]) - 87) * (16**power)
            power = power - 1

    ###Expand choice here
    return(return_value)

#Helper function to reverse string
def reverse_str(input_str):
    end = len(input_str)
    return_str = ''
    while(end>0):
        return_str += input_str[end - 1]
        end -= 1
    return return_str
