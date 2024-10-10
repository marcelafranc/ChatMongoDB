from database.entities import Message
from pymongo import MongoClient

class MongoHandler:
    # Definindo client e string de conexao
    def __init__(self):
        self.connection_string = "mongodb+srv://marcela:123456qwerty@samples.dpnaz.mongodb.net/?retryWrites=true&w=majority&appName=Samples"
        self.client = MongoClient(self.connection_string)

    # Conectando a database
    def connect(self, database_name):
        return self.client[database_name]

    # Autenticacao de usuario (verifica se um usuario existe no banco)
    def authenticate(self, email, password) -> bool:
        db = self.connect("chat")
        user = db.users.find_one({"email": email, "password": password})
        if user:
            return True
        else:
            return False

    # ANOTACOES
    # retorna o banco (db) para vc
    # conect tarara db tal e faz a operacao
    # precisa fazer disconnect

    # Funcao de Login de Usuario
    def login(self, email, senha) -> bool:
        db = self.connect("chat")
        user = db.users.find_one({"email": email, "password": senha})
        if user:
            return True
        else:
            return False

    # Funcao de Visualizar a Lista de Usuarios no Sistema
    def users_list(self):
        db = self.connect("chat")
        users_collection = db["users"]
        users = users_collection.find({}, {"_id": 0, "nickname": 1})

        lista_nicknames = []

        for user in users:
            nickname = user.get("nickname")
            if nickname:  # Verifica se o nickname não é None
                lista_nicknames.append(nickname)  # Adiciona o nickname à lista

        return lista_nicknames


    # Funcao Enviar uma Nova Mensagem a um Usuario
    def add_new_message (self, m: Message):
        db = self.connect("chat")
        coll = db.messages
        return coll.insert_one(m.__dict__).inserted_id

    # Funcao para visualizar quais usuarios mandaram mensagem para o usuario logado
    def my_chats(self, nickname_logado):
        db = self.connect("chat")
        msg = db.messages.find({"nickname_to": nickname_logado}, {"nickname_from": 1, "_id": 0})
        ret = [m['nickname_from'] for m in msg]
        return ret
