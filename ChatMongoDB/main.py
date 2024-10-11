from database.entities import User, Message
from database.mongohandler import MongoHandler
#from aes_pkcs5.algorithms.aes_cbc_pkcs5_padding import AESCBCPKCS5Padding

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
            mostrar_menu()
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
                break
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
            print("Usuário já cadastrado com esse Apelido.")
        elif handler.validarEmail(email):
            print("Usuário já cadastrado com esse email.")
        else:
            # Insere o usuário no banco de dados
            handler.adicionar_usuario(novo_usuario)
            print(f"Usuário {nickname} cadastrado com sucesso!")
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
                break
            else:
                print("Opção inválida! Tente novamente.")

    # Funcao para o usuario visualizar a lista de usuarios cadastrados no sistema
    def viewlist():
        print("\n----------------------------------------------------")
        print("     Escolha um usuário para enviar uma mensagem!     \n")

        usersColl = handler.users_list()

        usersColl = [user for user in usersColl if user != nickname_logado]

        if not usersColl:
            print("Nenhum usuário encontrado.")
            return

        for index, user in enumerate(usersColl, start=1):
            print(f"{index}. {user}")

        escolha = int(input("\nDigite o número do usuário escolhido: ")) - 1

        if 0 <= escolha < len(usersColl):
            usuario_escolhido = usersColl[escolha]

            # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            print("\n----------------------------------------------------")
            print(f"  Você escolheu enviar uma mensagem para: {usuario_escolhido}")
            key = input("\n Digite a chave secreta: ")
            typeKey(key)

            print("\n----------------------------------------------------")
            print(f"Enviando uma mensagem para: {usuario_escolhido} \n")
            msg = input(" Digite sua mensagem: ")
            sendmessage(nickname_logado, usuario_escolhido, msg, handler)

            # CRIPTOGRAFA A MENSAGEM
        else:
            print("Escolha inválida. Tente novamente.")

    # Funcao para enviar a mensagem ao usuario escolhido
    def sendmessage(nickname_from, nickname_to, content, handler):
        message = Message(nickname_from, nickname_to, content)
        message_id = handler.add_new_message(message)

        print(f"\nMensagem enviada de {nickname_from} para {nickname_to}!")
        opcoes()

    # Funcao para visualizar as mensagens que o usuario logado recebeu
    def inbox():
        print("LER msg")
        print("\n----------------------------------------------------")
        print(f"        Caixa de entrada de {nickname_logado}    \n")
        my_inbox = handler.my_chats(nickname_logado)
        for index, message in enumerate(my_inbox, start=1):
            print(f"{index}. {message}")

        escolha = int(input("\nDigite o número do usuário para ler a mensagem: ")) - 1

        if 0 <= escolha < len(my_inbox):
            usuario_escolhido = my_inbox[escolha]
            print("\n----------------------------------------------------")
            print(f"                CHAT COM {usuario_escolhido}")
            readmessage(usuario_escolhido, nickname_logado)
            #print("**** chamar funcao pra ler a mensagem escolhida ****")
            #TO DO: Criar uma funcao readMessage(usuario_escolhido?)

        else:
            print("Escolha inválida. Tente novamente.")

    # DIGITAR A CHAVE: PARA ENVIAR
    def typeKey(key):
        # chama criptografia
        #digita e envia a mensagem
        print("AAAAAAAAAAA")

    def readmessage(usuario_escolhido, nickname_logado):
        content = handler.read_a_message(usuario_escolhido, nickname_logado)
        if content:
            print(f"\n  {content}")
            print("----------------------------------------------------\n")

    # RODA O PROGRAMA INTEIRO!
    escolher_opcao()
