# from secrets import SystemRandom

# secretsGenerator = SystemRandom()
# random_number = secretsGenerator.randbits(128)
# print(random_number)
# print(secrets.SystemRandom.getrandbits(128))
# secrets.token_urlsafe()

# Complete the function scramble(str1, str2) that returns true 
# if a portion of str1 characters can be rearranged to match str2,
# otherwise returns false.

# Notes:

# Only lower case letters will be used (a-z)
# No punctuation or digits will be included.

# scramble('rkqodlw', 'world') ==> True
# scramble('cedewaraaossoqqyt', 'codewars') ==> True
# scramble('katas', 'steak') ==> False

stri1 = 'rkqodlw'
stri2 = 'world'
stri3 = 'cedewaraaossoqqyt'
stri4 = 'codewars'
stri5 = 'katas'
stri6 = 'steak'

def scramble(str1, str2):
    letter_dict = {}
    for letter in str2:
        letter_dict[letter] = 1
    for letter in str1:
        if letter in letter_dict.keys():
            letter_dict[letter] = 2
    for v in letter_dict.values():
        if v != 2:
            print(letter_dict)
            return False
        else:
            return True
    # print (letter_dict)

print(scramble(stri5, stri6))