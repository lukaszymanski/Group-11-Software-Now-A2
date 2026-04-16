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

def decrypt_text(text, shift1, shift2):
    '''
    full text decryption
    '''
    decrypted_text = ""

    for char in text: 
        decrypted_text += decrypt_char(char, shift1, shift2)

    return decrypted_text


def read_text_from_file():
    """
    Reads text from file
    """
    try:
        file = open("raw_text.txt", "r")
        text = file.read()
        file.close()
        return text
    except:
        print("file not found, please add 'raw_text.txt' to the master folder")
        return ""
    

def write_text_to_file(file_name, text):
    """
    writes text to file
    """
    try:
        file = open(file_name, "w")
        file.write(text)
        file.close()
    except:
        print("error writing to file")


# Verify files match
def verify_files():
    original_text = read_text_from_file()

    try:
        file = open("decrypted_text.txt", "r")
        decrypted_text = file.read()
        file.close()
    except:
        print("Decrypted file not found")
        return
    if original_text == decrypted_text:
        print("Decryption Successful")
    else:
        print("Decryption Failed")


# main program

def main():

    text = read_text_from_file()

    if text != "":

        #encrypt
        encrypted_text = encrypt_text(text, shift1, shift2)
        write_text_to_file("encrypted_text.txt", encrypted_text)

        # read encrypted file
        file = open("encrypted_text.txt", "r")
        encrypted_text = file.read()
        file.close()

        #decrypt
        decrypted_text = decrypt_text(encrypted_text, shift1, shift2)
        write_text_to_file("decrypted_text.txt", decrypted_text)

        #verify
        verify_files()

if __name__ == "__main__":
    main()






    

              

 











    