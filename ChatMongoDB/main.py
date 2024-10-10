from database.entities import User, Message
from database.mongohandler import MongoHandler
if __name__ == '__main__':
    #u2 = User('bla')
    #u2.nickname = 'ble'
    #u1 = User('marcela', 'marcela@puc.edu.br','123qwe')

    # handler = MongoHandler
    handler = MongoHandler()
    auth = handler.authenticate('mateus@gmail.com', '123456qwerty')

    # teste
    print(auth)

    # comecando aqui
    def mostrar_menu():
        print ("----------------------------------------------------")
        print ("            Bem-vindo(a) ao ChatMongoDB!            ")
        print("\n            1. Entrar")
        print("            2. Sair\n")

    def escolher_opcao():
        while True:
            mostrar_menu()
            escolha = input("       >>> Escolha uma opção: ")

            if escolha == "1":
                login()
                break
            elif escolha == "2":
                print("----------------------------------------------------")
                print("\nVocê escolheu 'Sair'.")
                print("Até a próxima!")
                break
            else:
                print("Opção inválida! Tente novamente.")

    def login():
        global nickname_logado #testando
        while True:
            print("\n----------------------------------------------------")
            print("                       LOGIN                        ")
            email = input("\n >> Digite seu email: ")
            senha = input("\n >> Digite sua senha: ")
            #print (email)
            #print(senha)
            # auth = handler.authenticate('mateus@gmail.com', '123456qwerty')
            entrar = handler.login(email, senha)
            print(entrar)
            if entrar == True:
                # testandoooo
                user = handler.connect("chat").users.find_one({"email": email})
                nickname_logado = user.get("nickname")  # Armazenar o nickname
                opcoes()
                break
            else:
                print("Credenciais incorretas. Tente novamente.")


    def opcoes():
        while True:
            print("\n----------------------------------------------------")
            print("               O que você deseja fazer?               \n")
            print("               1. Enviar mensagem")
            print("               2. Ler mensagem\n")
            escolha = input("       >>> Escolha uma opção: ")
            if escolha == "1":
                viewlist()
                break
            elif escolha == "2":
                inbox()
                break
            else:
                print("Opção inválida! Tente novamente.")

    def viewlist():
        print("\n----------------------------------------------------")
        print("     Escolha um usuário para enviar uma mensagem!     \n")

        usersColl = handler.users_list()

        if not usersColl:
            print("Nenhum usuário encontrado.")
            return

        for index, user in enumerate(usersColl, start=1):
            print(f"{index}. {user}")

        escolha = int(input("\nDigite o número do usuário escolhido: ")) - 1

        if 0 <= escolha < len(usersColl):
            usuario_escolhido = usersColl[escolha]
            print("\n----------------------------------------------------")
            print(f"Enviando uma mensagem para: {usuario_escolhido} \n")
            msg = input(" Digite sua mensagem: ")
            # print("Usuario logado: ")
            sendMessage(nickname_logado, usuario_escolhido, msg, handler)
            # pegar nickname_from; nickname_to (usuario_escolhido); content (msg)

        else:
            print("Escolha inválida. Tente novamente.")


    def sendMessage(nickname_from, nickname_to, content, handler):
        message = Message(nickname_from, nickname_to, content)
        message_id = handler.add_new_message(message)

        print(f"Mensagem enviada de {nickname_from} para {nickname_to}: {content} (ID: {message_id})")


    def inbox():
        print("LER msg")
        print("\n----------------------------------------------------")
        print(f"        Caixa de entrada de {nickname_logado}    \n")
        #chama
        # sendMessage(nickname_logado, usuario_escolhido, msg, handler)
        #mensagens = handler.my_chats(nickname_logado)
        #print(mensagens)
        my_inbox = handler.my_chats(nickname_logado)
        for index, message in enumerate(my_inbox, start=1):
            print(f"{index}. {message}")

        escolha = int(input("\nDigite o número do usuário para ler a mensagem: ")) - 1

        if 0 <= escolha < len(my_inbox):
            usuario_escolhido = my_inbox[escolha]
            print("\n----------------------------------------------------")
            print(f"             CHAT COM {usuario_escolhido}")
            print("**** chamar funcao pra ler ****")

        else:
            print("Escolha inválida. Tente novamente.")



    # RODAR FUNCOES
    escolher_opcao()

    # testando se o github está funcionando