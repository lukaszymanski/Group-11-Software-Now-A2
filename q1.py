#user input
shift1 = int(input("Enter shift1: "))
shift2 = int(input("Enter shift2: "))

# 2 encrpyt character
def ecrypt_text(text, shift1, shift2):
    result = ""

    for char in text:

        #lowercase letters
        if char.islower():

            #a-m forward rule
            if char >= 'a' and char <= 'm':
                shift = shift1 * shift2
                new_pos = (ord(char) - ord('a') + shift) % 26
                return chr(new_pos + ord('a'))
                
            # n-z backward rule
            else:
                shift = shift1 + shift2
                new_pos = (ord(char) - ord('a') - shift) % 26
                return chr(new_pos + ord('a'))
       
        #uppercase letters
        elif char.isupper():

            # A-M backward rule
            if 'A' <= char <= 'M':
                shift = shift1
                new_pos = (ord(char) - ord('A') - shift) % 26
                return chr(new_pos + ord('A'))
            # N-Z forward rule
            else:
                shift = shift2*shift2
                new_pos = (ord(char) - ord('A') + shift) % 26
                return chr(new_pos + ord('A'))
        else: 
            return char
        

# 3 full text encryption
# 4 decrypy character
# 5 decrypt text
# verify results
# file read program