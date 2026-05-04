# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 11:21:54 2022

@author: hamidat
"""

#TODO --> Complete the last block



ALPHABET=[ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
			'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


#this method must return the index (place in the ALPHABET) of searched char
def getIndexOfChar(searchedChar):
    #for each possible index of the array

    for i in range(len(ALPHABET)):

			# check if the value at index i is equal to the searchedChar parameter
            if ( ALPHABET[i]==searchedChar):
			#if true, we found the index of searchedChar !
                return i
			 
    raise ValueError("You can not search this char '" + searchedChar + "'");

# this is how you cipher a text
def cipher(plainText,shiftKey):
    cipheredText=""
    #get the position of the char at index i
    for i in range(len(plainText)):
        #get the position of the char at index i
        charPosition=getIndexOfChar(plainText[i])
        #compute the shifted index
        key = charPosition + shiftKey
        
        #if key is too big
        if key>=26:
            key=key-26
        
        #get the char at the specific key
        replaceVal = ALPHABET[key]
        
        #append the char to the returned value
        cipheredText = cipheredText + replaceVal
        
    return cipheredText

#TODO--> try to decypher a text
def decipher(cypheredText,shiftKey):
    plainText=""
    for i in range (len(cypheredText)):
        charPosition=getIndexOfChar(cypheredText[i])
        key = charPosition - shiftKey
        
        if key<0:
            key=key+26
        
        replaceVal = ALPHABET[key]
        
        plainText = plainText + replaceVal

    return plainText

        
plainText = "ftqpdazquenqzqmftftqqurrqxfaiqd" 
print(("I'm trying to cypher the following message : '", plainText, "'")) 
decypheredMessage = decipher(plainText, 1)  
print(("The decyphered message is : '" , decypheredMessage))

#Do it for every shiftKey possible
#Modify inside the print parenthesis.
for i in range(len(ALPHABET)):
    print("ShiftKey =", i, "->", decipher(plainText, i))





   