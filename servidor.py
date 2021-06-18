import BG
import socket
import os

servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servidor.bind((socket.gethostname(),3000))
servidor.listen(20)
p = 499
q = 547
llavePublica = BG.key_generation(p,q)
path_output=os.path.join(os.getcwd(),'outputCrackedHash')

def recibir(nombre):
    archivo = open(f'./recibido/{nombre}.txt','wb')
    while True:
        data = cliente.recv(1024)
        if data:
            while data:
                archivo.write(data)
                data = cliente.recv(1024)
            archivo.close()
        else:
            break

def desencriptar(nombre):
    archivo = open(f'./recibido/{nombre}.txt', 'r').readlines()
    archivo2 = open(f'./recibido/{nombre}Decrypted.txt', 'w')
    for lines in archivo:
        linea = lines.replace("(","").replace(")","").replace("'","")
        linea = linea.split(',')
        linea[1] = int(linea[1])
        linea = tuple(linea)
        decrypted = BG.decrypt(p,q, linea)
        decrypted=BG.bin_toAscii(decrypted)
        archivo2.write(decrypted+"\n")
    archivo2.close()
    print("Archivo desencriptado exitosamente!")

while True:
    cliente,direccion = servidor.accept()
    data=cliente.recv(4096).decode()
    if (data == "publica"):
        cliente.sendall(bytes(str(llavePublica),'utf-8'))
        print(f'Se envia la llave publica: {llavePublica}')
    else:
        targetName = input("Ingresa el nombre con el cual guardar el archivo recibido (./recibido): ")
        recibir(targetName)
        desencriptar(targetName)
    cliente.close()