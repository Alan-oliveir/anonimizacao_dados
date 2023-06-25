import pyodbc
import hashlib
import random
import string

# Função para gerar uma string aleatória
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

# Função para criptografar um valor usando SHA256
def encrypt_value(value):
    hashed_value = hashlib.sha256(value.encode('utf-8')).hexdigest()
    return hashed_value

# Função para mascarar um valor trocando caracteres por asteriscos
def mask_value(value):
    masked_value = '*' * len(value)
    return masked_value

# Função para generalizar um valor trocando letras por X e números por 0
def generalize_value(value):
    generalized_value = ''
    for char in value:
        if char.isalpha():
            generalized_value += 'X'
        elif char.isdigit():
            generalized_value += '0'
        else:
            generalized_value += char
    return generalized_value


def anonimizar_dados():
    # Conectar ao banco de dados
    conn = pyodbc.connect('DRIVER={SQL SERVER}; SERVER=ALAN_PC\SQLEXPRESS; DATABASE=PYSQL')
    cursor = conn.cursor()
    # Selecionar todos os registros da tabela que deseja anonimizar
    cursor.execute("SELECT * FROM Clientes")
    registros = cursor.fetchall()

    # Anonimizar cada registro
    for registro in registros:
        # Aplicar a técnica de anonimização desejada:
        #campo_anonimizado = encrypt_value(registro.campo) # Criptografia não foi utilizada
        nome_anonimizado = mask_value(registro.Nome) # Mascaramento
        telefone_anonimizado = generalize_value(registro.Telefone) # Generalização
        # Atualizar o registro anonimizado na tabela
        cursor.execute("UPDATE Clientes SET Nome = ? WHERE ID_Cliente = ?", (nome_anonimizado, registro.ID_Cliente))
        cursor.execute("UPDATE Clientes SET Telefone = ? WHERE ID_Cliente = ?", (telefone_anonimizado, registro.ID_Cliente))
        # Confirmar as alterações no banco de dados
        cursor.commit()

    # Fechar a conexão com o banco de dados
    conn.close()

# Chamada da função para anonimizar os dados
anonimizar_dados()