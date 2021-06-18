import os
import socket
import BG
import bcrypt
import timeit

path_output=os.path.join(os.getcwd(),'outputCrackedHash')
path_hashcat= os.path.join(os.getcwd(),'hashcat-6.2.1')
path_hashes=os.path.join(os.getcwd(),'Hashes')
path_dict=os.path.join(os.getcwd(),'diccionarios')
path_bcrypt = os.path.join(os.getcwd(),'bcryptOutput')

def menu():
    print("1.- Crackear archivos Hash")
    print("2.- Hashear con un algoritmo mas seguro")
    print("3.- Obtener Llave publica y encriptar")
    print("4.- Enviar Archivo encriptado Asimetrico al servidor")
    print("5.- Salir")
    opcion = input("Selección: ")
    os.system('cls')
    return opcion

def crackearHash():
    print("Puedes arrastrar los archivos a esta ventana para obtener su ruta facilmente")
    archivoHash1 = input("Ingresa la ruta del archivo: ")
    modo = input('Ingresa el modo: ')
    diccionario1 = input('Ingresa el primer diccionario: ')
    diccionario2 = input('Ingresa el segundo diciconario: ')
    targetName = input('Ingresa el nombre con el que se guardara el archivo (./outputCrackedHash): ')
    os.chdir(path_hashcat)
    try:
        os.remove('hashcat.potfile')
        output=str(os.path.join(path_output,targetName))
        os.system(f"hashcat.exe -m {modo} -a 0 {archivoHash1} {diccionario1} {diccionario2} --outfile={output}.txt --force")
    except:
         pass

def hashSeguro():
    mySalt = bcrypt.gensalt()
    print(f"salt utilizado: {mySalt.decode()}")
    print("Puedes arrastrar los archivos a esta ventana para obtener su ruta facilmente")
    archivo = input('Ingresa el archivo para realizar el Hash: ')
    targetName = input('Ingresa el nombre con el que se guardara el archivo (./bcryptOutput): ')
    print("Realizando Hash con Bcrypt...")
    saveHash = open(f'./bcryptOutput/{targetName}.txt','w')
    archivo = open(archivo, 'r').readlines()
    first=timeit.default_timer()
    for line in archivo:
        encrypted = bcrypt.hashpw(line.strip().rsplit(':',1)[1].encode(encoding='utf-8'), mySalt)
        saveHash.write(encrypted.decode()+'\n')
    second=timeit.default_timer()
    print("tiempo total al realizar el nuevo hash: " + str(second-first) + " Seg")

def conectarSocket():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((socket.gethostname(),3000))
    server.sendall(bytes("publica", encoding = 'utf-8'))
    public_key = server.recv(1024).decode('ascii')
    print(f'LLave publica recibida: {public_key}')
    print("Puedes arrastrar los archivos a esta ventana para obtener su ruta facilmente")
    archivo = input('Ingresa el archivo para realizar el Hash: ')
    archivo = open(archivo, 'r').readlines()
    targetName = input ('Ingresa el nombre con el cual guardar el archivo: ')
    saveFile= open(f"./outputAsimetrico/{targetName}.txt", 'w')
    for line in archivo:
        encrypted=BG.encrypt(line.strip(),159201,int(public_key))
        saveFile.write(str(encrypted)+"\n")
    saveFile.close()

def enviarAsim():
    archivo = input('Ingresa el archivo a enviar: ')
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((socket.gethostname(),3000))
    server.sendall(bytes("no-publica", encoding = 'utf-8'))
    f = open(archivo, 'rb')
    l = f.read(1024)
    while l:
        server.send(l)
        l = f.read(1024)
    server.close()

while True:
    opcion = menu()
    if(opcion == '1'):
        crackearHash()
    if(opcion == '2'):
        hashSeguro()
    if(opcion == '3'):
        conectarSocket()
    if(opcion == '4'):
        enviarAsim()
    if(opcion == '5'):
        break




