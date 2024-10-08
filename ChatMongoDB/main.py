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


    # testando se o github está funcionando