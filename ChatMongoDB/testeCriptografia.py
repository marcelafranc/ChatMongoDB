from aes_pkcs5.algorithms.aes_cbc_pkcs5_padding import AESCBCPKCS5Padding

# Solicitando a chave, mensagem e definindo o IV
key = input("Digite a chave de 16 caracteres para AES-128: ")
while len(key) != 16:
    print("A chave precisa ter exatamente 16 caracteres.")
    key = input("Digite a chave de 16 caracteres para AES-128: ")

iv_parameter = "0011223344556677"  # 16 bytes de IV

# Solicitando a mensagem ao usuário
message = input("Digite a mensagem que deseja criptografar: ")

# Criptografia Base64
output_format = "b64"
cipher = AESCBCPKCS5Padding(key, output_format, iv_parameter)
encrypted = cipher.encrypt(message)
print(f"Mensagem criptografada (b64): {encrypted}")
print(f"Mensagem descriptografada: {cipher.decrypt(encrypted)}")

# Criptografia Hexadecimal
output_format = "hex"
cipher = AESCBCPKCS5Padding(key, output_format, iv_parameter)
encrypted = cipher.encrypt(message)
print(f"Mensagem criptografada (hex): {encrypted}")
print(f"Mensagem descriptografada: {cipher.decrypt(encrypted)}")
