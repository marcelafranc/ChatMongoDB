from aes_pkcs5.algorithms.aes_cbc_pkcs5_padding import AESCBCPKCS5Padding
print("Hello, World!")

# Definindo a chave, formato de saída, IV e a mensagem
key = "@NcRfUjXn2r5u8x/"  # 16 caracteres para AES-128
iv_parameter = "0011223344556677"  # 16 bytes de IV
message = "Hello World"

# Criptografia Base64
output_format = "b64"
cipher = AESCBCPKCS5Padding(key, output_format, iv_parameter)
encrypted = cipher.encrypt(message)
print(f"Mensagem criptografada (b64): {encrypted}")
assert encrypted == "MhL/V78kC3rcYlnlPg1L4g=="  # Verificando o valor esperado
print(f"Mensagem descriptografada: {cipher.decrypt(encrypted)}")

# Criptografia Hexadecimal
output_format = "hex"
cipher = AESCBCPKCS5Padding(key, output_format, iv_parameter)
encrypted = cipher.encrypt(message)
print(f"Mensagem criptografada (hex): {encrypted}")
assert encrypted == "3212ff57bf240b7adc6259e53e0d4be2"  # Verificando o valor esperado
print(f"Mensagem descriptografada: {cipher.decrypt(encrypted)}")
