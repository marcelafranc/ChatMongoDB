from database.entities import User, Message
from database.mongohandler import MongoHandler
#from aes_pkcs5.algorithms.aes_cbc_pkcs5_padding import AESCBCPKCS5Padding
from aes_pkcs5.algorithms.aes_cbc_pkcs5_padding import AESCBCPKCS5Padding


if __name__ == '__main__':

    handler = MongoHandler()
    auth = handler.authenticate('mateus@gmail.com', '123456qwerty')
    # TESTE - REMOVER *APENAS* NA ENTREGA FINAL
    # VERIFICA RAPIDAMENTE SE A CONEXAO COM O BANCO ESTA FUNCIONANDO
    print(auth)

    # Funcao Menu Inicial
    def mostrar_menu():
        print ("----------------------------------------------------")
        print ("            Bem-vindo(a) ao ChatMongoDB!            ")
        print("\n            1. Entrar")
        print("            2. Cadastrar")
        print("            3. Sair\n")

    # Funcao Escolher Opcao do Menu Inicial
    def escolher_opcao():
        while True:
            escolha = input("       >>> Escolha uma opção: ")

            if escolha == "1":
                login()
                break
            elif escolha == "2":
                cadastrarUsuario()
                break
            elif escolha == "3":
                print("----------------------------------------------------")
                print("\nVocê escolheu 'Sair'.")
                print("Até a próxima!")
                exit()
            else:
                print("Opção inválida! Tente novamente.")

    # Funcao Cadastrar Usuario
    def cadastrarUsuario(): 
        print("\n----------------------------------------------------")
        print("                       CADASTRO                      ")
        nickname = input("Apelido: ")
        email = input("Email: ")
        password = input("Senha: ")

        # Criando o objeto User
        novo_usuario = User(nickname, email, password)

        # Verifica se o usuário já existe no banco
        if handler.validarApelido(nickname):
            print("\nUsuário já cadastrado com esse Apelido.")
        elif handler.validarEmail(email):
            print("\nUsuário já cadastrado com esse email.")
        else:
            # Insere o usuário no banco de dados
            handler.adicionar_usuario(novo_usuario)
            print(f"\nUsuário {nickname} cadastrado com sucesso!")
            mostrar_menu()
            escolher_opcao()  # Retorna ao menu principal após cadastro
    
    # Funcao Logar no Sistema
    def login():
        global nickname_logado #testando
        while True:
            print("\n----------------------------------------------------")
            print("                       LOGIN                        ")
            email = input("\n >> Digite seu email: ")
            senha = input("\n >> Digite sua senha: ")
            entrar = handler.login(email, senha)
            print(entrar)
            if entrar == True:
                user = handler.connect("chat").users.find_one({"email": email})
                nickname_logado = user.get("nickname")  # Armazenar o nickname
                opcoes()
                break
            else:
                print("Credenciais incorretas. Tente novamente.")

    # Funcao Menu de Opcoes do Usuario (Logado)
    def opcoes():
        while True:
            print("\n----------------------------------------------------")
            print("               O que você deseja fazer?               \n")
            print("               1. Enviar mensagem")
            print("               2. Ler mensagem")
            print("               3. Sair\n")
            escolha = input("       >>> Escolha uma opção: ")
            if escolha == "1":
                viewlist()
                break
            elif escolha == "2":
                inbox()
                break
            elif escolha == "3":
                mostrar_menu()
                escolher_opcao()

            else:
                print("Opção inválida! Tente novamente.")

    # Funcao para o usuario visualizar a lista de usuarios cadastrados no sistema
    def viewlist():
        print("\n----------------------------------------------------")
        print("     Escolha um usuário para enviar uma mensagem!     \n")

        usersColl = handler.users_list()

        # Remove o usuário logado da lista de usuários
        usersColl = [user for user in usersColl if user != nickname_logado]

        if not usersColl:
            print("Nenhum usuário encontrado.")
            return

        # Exibe a lista de usuários
        for index, user in enumerate(usersColl, start=1):
            print(f"{index}. {user}")

        while True:
            escolha = input("\nDigite o número do usuário escolhido: ")
            if escolha.isdigit():
                escolha = int(escolha) - 1

                if 0 <= escolha < len(usersColl):
                    usuario_escolhido = usersColl[escolha]
                    print("\n----------------------------------------------------")
                    print(f"  Você escolheu enviar uma mensagem para: {usuario_escolhido}")

                    key = input("Digite a chave (16 caracteres): ")
                    while len(key) != 16:
                        print("A chave precisa ter exatamente 16 caracteres.")
                        key = input("Digite a chave (16 caracteres): ")

                    print("\n----------------------------------------------------")
                    print(f"Enviando uma mensagem para: {usuario_escolhido} \n")
                    msg = input("Digite sua mensagem: ")
                    encrypted = encrypt(key, msg)
                    sendmessage(nickname_logado, usuario_escolhido, encrypted, handler)
                    break
                else:
                    print("Escolha inválida. O número não corresponde a nenhum usuário. Tente novamente.")
            else:
                print("Entrada inválida. Digite um número correspondente a um usuário.")

    # Funcao para enviar a mensagem ao usuario escolhido
    def sendmessage(nickname_from, nickname_to, content, handler):
        message = Message(nickname_from, nickname_to, content)
        message_id = handler.add_new_message(message)

        print(f"\nMensagem enviada para {nickname_to}!")
        opcoes()

    # Funcao para visualizar as mensagens que o usuario logado recebeu
    def inbox():
        print("\n----------------------------------------------------")
        print(f"        Caixa de entrada de {nickname_logado}    \n")
        my_inbox = handler.my_chats(nickname_logado)
        for index, message in enumerate(my_inbox, start=1):
            print(f"{index}. {message}")

        escolha = int(input("\nDigite o número do usuário para ler a mensagem: ")) - 1

        if 0 <= escolha < len(my_inbox):
            usuario_escolhido = my_inbox[escolha]
            print("\n----------------------------------------------------")
            key = input("Digite a chave (16 caracteres): ")
            while len(key) != 16:
                print("A chave precisa ter exatamente 16 caracteres.")
                key = input("Digite a chave (16 caracteres): ")

            content = getmessage(usuario_escolhido, nickname_logado)

            retorno = escolher_mensagem_para_visualizar(usuario_escolhido, nickname_logado)
            decryptedmessage = decrypting(key, retorno)
            print("\n----------------------------------------------------")
            print(f"              MENSAGEM ESCOLHIDA")
            print(f"\n {decryptedmessage}")
            print("\n")
            opcoes()


    # DEU CERTO
    def getmessage(usuario_escolhido, nickname_logado):
        contents = handler.read_a_message(usuario_escolhido, nickname_logado)
        messages = [message['content'] for message in contents]
        return messages


    def escolher_mensagem_para_visualizar(usuario_escolhido, nickname_logado):
        messages = getmessage(usuario_escolhido, nickname_logado)
        if not messages:
            print("Não há mensagens para exibir.")
            return
        print("Mensagens disponíveis:")
        for i, message in enumerate(messages, start=1):
            print(f"Mensagem {i}")

        while True:
            try:
                escolha = int(input(f"Escolha o número da mensagem que deseja visualizar (1-{len(messages)}): "))
                if 1 <= escolha <= len(messages):
                    break
                else:
                    print(f"Escolha inválida. Digite um número entre 1 e {len(messages)}.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")

        # RETORNO DA FUNCAO
        return messages[escolha - 1]  # -1 para ajustar ao índice da lista


    # PARTE DA CRIPTOGRAFIA!!!!!!!!!!!!!!!!!!
    def encrypt(key, message):
        iv_parameter = "0011223344556677"  # 16 bytes de IV
        output_format = "b64"
        cipher = AESCBCPKCS5Padding(key, output_format, iv_parameter)
        encryptedcontent = cipher.encrypt(message)
        print(f"Mensagem criptografada (b64): {encryptedcontent}")
        return encryptedcontent

    def decrypting(key, message):
        iv_parameter = "0011223344556677"  # 16 bytes de IV
        output_format = "b64"
        cipher = AESCBCPKCS5Padding(key, output_format, iv_parameter)
        encrypted = cipher.encrypt(message)
        descriptografia = (cipher.decrypt(message))
        return descriptografia



    ## MAIN
    # RODA O PROGRAMA INTEIRO!
    mostrar_menu()
    escolher_opcao()
