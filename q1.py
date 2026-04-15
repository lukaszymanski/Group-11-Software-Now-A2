#user input
shift1 = int(input("Enter shift1: "))
shift2 = int(input("Enter shift2: "))

def encrypt_char(char, shift1, shift2):
    """
    Encrypts one character
    """
    #lowercase rules
    if char.islower():
        offset = 97
        char_position = ord(char) - offset

        if char_position < 13: # first alphabet half (a-m)
            new_position = (char_position + shift1 * shift2) % 26
        else: #second alphabet half
            new_position = (char_position - (shift1 + shift2)) % 26

        return chr(new_position + offset)
    
    # uppercase rules
    elif char.isupper():
        offset = 65
        char_position = ord(char) - offset

        if char_position < 13: # first alphabet half (A-M)
            new_position = (char_position - shift1) % 26
        else: # sencond alphabet half (N-Z)
            new_position = (char_position + shift2 ** 2) % 26

        return chr(new_position + offset)
    
    else: # other characters
        return char
    

def encrypt_text(text, shift1, shift2):
    '''
    Encrypt full text
    '''
    encrypted_text = ""

    for char in text:
        encrypted_text += encrypt_char(char, shift1, shift2)

    return encrypted_text

def decrypt_char(char, shift1, shift2):
    """
    Decrypts one character
    """
    # other characters
    if not char.isalpha():
        return char
    
    # try lowercase decrypt
    if char.islower():
        for test_char in "abcdefghijklmnopqrstuvwxyz":
            if encrypt_char(test_char, shift1, shift2) == char:
                return test_char
            
    # try uppercase decrypt
    if char.isupper():
        for test_char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if encrypt_char(test_char, shift1, shift2) == char:
                return test_char
            
    return char

"""
full text decryption
"""

 











    