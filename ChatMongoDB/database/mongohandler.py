from database.entities import Message
from database.entities import User
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

    # Funcao cadastrar Usuario
    def adicionar_usuario(self, u: User):
        db = self.connect("chat")
        coll = db.users
        return coll.insert_one(u.__dict__).inserted_id
    
    # Funcao para validar se email já existe no banco
    def validarEmail(self, email: str) -> bool:
        db = self.connect("chat")
        coll = db.users
        usuario = coll.find_one({"email": email})
        return usuario is not None
    
    # Funcao para validar se apelido já existe no banco
    def validarApelido(self, nickname: str) -> bool:
        db = self.connect("chat")
        coll = db.users
        usuario = coll.find_one({"nickname": nickname})
        return usuario is not None

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
            if nickname:
                lista_nicknames.append(nickname) 

        return lista_nicknames


    # Funcao Enviar uma Nova Mensagem a um Usuario
    def add_new_message (self, m: Message):
        db = self.connect("chat")
        coll = db.messages
        return coll.insert_one(m.__dict__).inserted_id

    # Funcao para visualizar quais usuarios mandaram mensagem para o usuario logado
    def my_chats(self, nickname_logado):
        db = self.connect("chat")
        usuarios_distintos = db.messages.distinct("nickname_from", {"nickname_to": nickname_logado})
        return usuarios_distintos

    # Funcao para filtrar todas as mensagens de um usuario especifico (usuario logado)
    def read_a_message(self, usuario_escolhido, nickname_logado):
        db = self.connect("chat")
        mensagens_do_usuario = []
        messages = db.messages.find({"nickname_to": nickname_logado, "nickname_from": usuario_escolhido})
        for message in messages:
            mensagens_do_usuario.append(message)
        return mensagens_do_usuario

    # Funcao para agrupar todas as mensagens de um usuario especifico
    def getmanymsgs(self, usuario_escolhido, nickname_logado):
        db = self.connect("chat")
        messages = db.messages.find({"nickname_to": nickname_logado, "nickname_from": usuario_escolhido})
        all_messages = {usuario_escolhido: []}
        for message in messages:
            all_messages[usuario_escolhido].append(message['content'])

        return all_messages



