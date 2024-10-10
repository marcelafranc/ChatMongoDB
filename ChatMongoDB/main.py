from database.entities import User
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
                #print("Você escolheu 'Entrar'.")
                login()
                # Aqui você pode adicionar o código que executa a ação de entrar.
                break
            elif escolha == "2":
                print("----------------------------------------------------")
                print("\nVocê escolheu 'Sair'.")
                print("Até a próxima!")

                # Aqui você pode adicionar o código que executa a ação de sair.
                break
            else:
                print("Opção inválida! Tente novamente.")

    def login():
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
                opcoes()
                break
            else:
                print("Credenciais incorretas. Tente novamente.")


    def opcoes():
        while True:
            print("\n----------------------------------------------------")
            print("\n               O que você deseja fazer?               ")
            print("               1. Enviar mensagem")
            print("               2. Ler mensagem\n")
            escolha = input("       >>> Escolha uma opção: ")
            if escolha == "1":
                viewlist()
                break
            elif escolha == "2":
                readMessages()
                break
            else:
                print("Opção inválida! Tente novamente.")

    def viewlist():
        print("\n----------------------------------------------------")
        print("     Escolha um usuário para enviar uma mensagem!     \n")

        userscoll = handler.users_list()

        if not userscoll:
            print("Nenhum usuário encontrado.")
            return

        for index, user in enumerate(userscoll, start=1):
            print(f"{index}. {user}")

        # escolha = int(input("\nDigite o número do usuário escolhido: ")) - 1
        #
        # if 0 <= escolha < len(userscoll):
        #     usuario_escolhido = userscoll[escolha]
        #     print(f"\nVocê escolheu o usuário: {usuario_escolhido}")
        #     print("cheguei aquiii ")
        # else:
        #     print("Escolha inválida. Tente novamente.")




    def readMessages():
        print("ENVIAR msg")

    # RODAR FUNCOES
    escolher_opcao()

    # testando se o github está funcionando