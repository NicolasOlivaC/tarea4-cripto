#function for checking if a number is prime
def is_prime_number(x):
    if x >= 2:
        for y in range(2,x):
            if not ( x % y ):
                return False
    else:
	    return False
    return True

#function for XORing two strings
def XOR(a,b):
    a,b = str(a),str(b)
    assert(len(a) <= len(b))
    result = ""
    for i in range(len(a)):
        result += str(int(a[i]) ^ int(b[i]))
    return result

#function for finding the modular inverse
def modInverse(a, m) : 
    a = a % m
    for x in range(1, m) : 
        if ((a * x) % m == 1) : 
            return x 
    return 1

#######################################################
###########         Key Generation          ###########
#######################################################

def key_generation(p,q):
    try:
        #making sure p and q are congruent to 
        assert(is_prime_number(p))
        assert(is_prime_number(q))
        assert(p % 4 == 3)
        assert(q % 4 == 3)
        #creating N, public key
        N = p * q
        #print("Public Key =", N)

        #split_string_m = str(m)
        print(f'Llave generada: {N}')
        return N

    except AssertionError as e:
        print('Error con los numeros elegidos: ', str(e))

#######################################################
###########            Encryption           ###########
#######################################################

def encrypt(msg,X0,key):
    X = []
    X.append(X0)    
    hash_bytes=''
    for char in msg:
        bin_text=str(bin(ord(char))).replace('0b','')
        while len(bin_text)<7:
            bin_text= '0'+bin_text
        hash_bytes+=bin_text
    b = ""
    L = len(str(hash_bytes))
    for i in range(L):
        string_x = bin(X[-1])[2:]
        size = len(string_x)
        b_i = string_x[size-1]
        b = b_i + b
        new_x = (X[i] ** 2) % key
        X.append(new_x)
    str_m = str(hash_bytes)
    ciphertext = XOR(str_m, b)
    XL = X[-1]
    X0 = X[0]
    XL_check = pow(X0,pow(2,L),key)
    assert (XL == XL_check)
    sent_message = (ciphertext, XL)
    return sent_message

#######################################################
###########            Decryption           ###########
#######################################################

def decrypt(p,q,encrypted):

    ciphertext,XL=encrypted
    XL=int(XL)
    L = len(str(ciphertext))
    N=p*q
    firstExponent = (((p+1)//4)**L) % (p-1)
    firstPhrase = "({}^{}) mod {}".format(XL,firstExponent,p)
    r_p = pow(XL,firstExponent,p)
    secondExponent = (((q+1)//4)**L) % (q-1)
    secondPhrase = "({}^{}) mod {}".format(XL,secondExponent,q)
    r_q = pow(XL,secondExponent,q)
    NEWX0 = (q*modInverse(q,p)*r_p + p*modInverse(p,q)*r_q)%N
    NEWX = []
    NEWX.append(NEWX0)
    b = ""
    for i in range(L):
        string_x = bin(NEWX[-1])[2:]
        size = len(string_x)
        b_i = string_x[size-1]
        b = b_i + b
        new_x = (NEWX[i] ** 2) % N
        NEWX.append(new_x)
    plaintext = XOR(ciphertext,b)
    return plaintext

def bin_toAscii(msg):
    msg_split=[msg[i:i+7] for i in range(0,len(msg),7)]
    salida=''
    for msg in msg_split:
        while len(msg) < 7:
            msg='0'+msg
        salida+=chr(int(msg,base=2))
    return salida