from database.entities import Message
from pymongo import MongoClient

# aaa
# class Operations:
#     def __init__(self,
#                  username: str,
#                  password:str,
#                  primary_node: str):
#         #self.connection_string = 'mongo+srv://{}:{}@{}?retryWrites=true'.format(username, password, primary_node)
#         self.connection_string = 'mongodb+srv://marcela:<db_password>@samples.dpnaz.mongodb.net/?retryWrites=true&w=majority&appName=Samples'
#         # url da conexao --


class MongoHandler:
    def __init__(self):
        self.connection_string = "mongodb+srv://marcela:123456qwerty@samples.dpnaz.mongodb.net/?retryWrites=true&w=majority&appName=Samples"
        #self.client = MongoClient("mongodb+srv://marcela:123456qwerty@samples.dpnaz.mongodb.net/?retryWrites=true&w=majority&appName=Samples")
        self.client = MongoClient(self.connection_string)


    def connect(self, database_name):
        return self.client[database_name]

    def authenticate(self, email, password) -> bool:
        db = self.connect("chat")
        user = db.users.find_one({"email": email, "password": password})
        if user:
            return True
        else:
            return False

    # retorna o banco (db) para vc
    # conect tarara db tal e faz a operacao
    # precisa fazer disconnect


    def login(self, email, senha) -> bool:
        db = self.connect("chat")
        user = db.users.find_one({"email": email, "password": senha})
        if user:
            return True
        else:
            return False

    def users_list(self):
        db = self.connect("chat")
        users_collection = db["users"]
        users = users_collection.find({}, {"_id": 0, "nickname": 1})
        # for user in users:
        #     print(user.get("nickname"))

        lista_nicknames = []

        for user in users:
            nickname = user.get("nickname")
            if nickname:  # Verifica se o nickname não é None
                lista_nicknames.append(nickname)  # Adiciona o nickname à lista

        return lista_nicknames



    def add_new_message (self, m: Message):
        db = self.connect("chat")
        coll = db.messages
        return coll.insert_one(m.__dict__).inserted_id


    def my_chats(self, nickname_logado):
        # pegar: usuario logado para ver nickname_to -- verificar se há mensagens para mim
        # pegar nickname_from para ver QUAIS (QUEM) usuarios me mandaram mensagem
        db = self.connect("chat")
        #coll = db.messages
        #db.messages.find({"nickname_to": "nih"})
        # msg = db.messages.find({"nickname_to": nickname_logado})
        # ret = msg.nickname_from
        # return ret
        msg = db.messages.find({"nickname_to": nickname_logado}, {"nickname_from": 1, "_id": 0})
        ret = [m['nickname_from'] for m in msg]
        return ret
