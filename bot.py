import telebot
import time

# Этап 2: Создать класс Player для хранения информации об игроках
class Player:
    def __init__(self, name):
        self.name = name
        self.attempts = 3
        self.hints = 3
        self.start_time = None
        self.room_code = None

    def start_game(self):
        self.start_time = time.time()

    def end_game(self):
        return time.time() - self.start_time

# Этап 3: Создать класс Room для хранения информации о комнатах
class Room:
    def __init__(self, code, secret_word, teacher):
        self.code = code
        self.secret_word = secret_word
        self.teacher = teacher
        self.players = []

    def add_player(self, player):
        self.players.append(player)
        player.room_code = self.code

    def remove_player(self, player):
        self.players.remove(player)
        player.room_code = None
# Python

# Этап 4: Создать класс Game для управления игровым процессом
class Game:
    def __init__(self, bot_token):
        self.bot = telebot.TeleBot(bot_token)
        self.rooms = {}

    def create_room(self, code, secret_word, teacher):
        if code in self.rooms:
            return False
        self.rooms[code] = Room(code, secret_word, teacher)
        return True

    def register_player(self, name, room_code):
        if room_code not in self.rooms:
            return False
        player = Player(name)
        self.rooms[room_code].add_player(player)
        return True

    def start_game(self, room_code):
        if room_code not in self.rooms:
            return False
        for player in self.rooms[room_code].players:
            player.start_game()
        return True

    def end_game(self, room_code):
        if room_code not in self.rooms:
            return False
        for player in self.rooms[room_code].players:
            player.end_game()
        del self.rooms[room_code]
        return True

# Python

# Этап 5: Создать функции для обработки команд от игроков
game = Game("6826640406:AAFa6aBqzg2jyoGRwmAWBvnGHbCIyIC2jIY")
# Функция для регистрации игрока
@game.bot.message_handler(commands=['register'])
def register_player(message):
    name, room_code = message.text.split()[1:]
    if game.register_player(name, room_code):
        game.bot.reply_to(message, f"Player {name} registered successfully in room {room_code}")
    else:
        game.bot.reply_to(message, "Failed to register player. Check the room code and try again.")

# Функция для задания вопроса
@game.bot.message_handler(commands=['ask'])
def ask_question(message):
    room_code, question = message.text.split()[1], ' '.join(message.text.split()[2:])
    room = game.rooms.get(room_code)
    if room:
        game.bot.send_message(room.teacher, f"Question from {message.from_user.username}: {question}")
    else:
        game.bot.reply_to(message, "Failed to ask question. Check the room code and try again.")

# Функция для написания ответа
@game.bot.message_handler(commands=['answer'])
def write_answer(message):
    room_code, answer = message.text.split()[1], ' '.join(message.text.split()[2:])
    room = game.rooms.get(room_code)
    if room:
        for player in room.players:
            if player.name == message.from_user.username:
                if room.secret_word == answer:
                    game.bot.reply_to(message, "Congratulations! Your answer is correct.")
                    player.attempts = 0
                else:
                    player.attempts -= 1
                    print(player.attempts)
                    if player.attempts > 0:
                        game.bot.reply_to(message, f"Wrong answer. You have {player.attempts} attempts left.")
                    else:
                        game.bot.reply_to(message, "Game over. You have no attempts left.")
                break
    else:
        game.bot.reply_to(message, "Failed to submit answer. Check the room code and try again.")

# Функция для запроса подсказки
@game.bot.message_handler(commands=['hint'])
def request_hint(message):
    room_code = message.text.split()[1]
    room = game.rooms.get(room_code)
    if room:
        for player in room.players:
            if player.name == message.from_user.username:
                if player.hints > 0:
                    game.bot.send_message(room.teacher, f"Hint request from {message.from_user.username}")
                    player.hints -= 1
                else:
                    game.bot.reply_to(message, "You have no hints left.")
                break
    else:
        game.bot.reply_to(message, "Failed to request hint. Check the room code and try again.")

# Python

# Этап 6: Создать функции для обработки команд от учителя

# Функция для создания комнаты
@game.bot.message_handler(commands=['create_room'])
def create_room(message):
    code, secret_word = message.text.split()[1:]
    if game.create_room(code, secret_word, message.from_user.id):
        game.bot.reply_to(message, f"Room {code} created successfully with secret word {secret_word}")
    else:
        game.bot.reply_to(message, "Failed to create room. Check the room code and try again.")

# Функция для начала игры
@game.bot.message_handler(commands=['start_game'])
def start_game(message):
    room_code = message.text.split()[1]
    if game.start_game(room_code):
        game.bot.reply_to(message, f"Game started in room {room_code}")
    else:
        game.bot.reply_to(message, "Failed to start game. Check the room code and try again.")

# Функция для ответа на вопросы
@game.bot.message_handler(func=lambda message: True)
def answer_question(message):
    for room in game.rooms.values():
        if room.teacher == message.from_user.id:
            game.bot.send_message(room.players[0].id, message.text)
            break

# Функция для написания подсказок
@game.bot.message_handler(commands=['hint'])
def write_hint(message):
    room_code, hint = message.text.split()[1], ' '.join(message.text.split()[2:])
    room = game.rooms.get(room_code)
    if room:
        game.bot.send_message(room.players[0].id, f"Hint: {hint}")
    else:
        game.bot.reply_to(message, "Failed to send hint. Check the room code and try again.")

# Python

# Этап 7: Создать функцию для сравнения ответа игрока и секретного слова

# Функция уже была создана в этапе 5 внутри функции write_answer.
# Она сравнивает ответ игрока с секретным словом и в зависимости от результата отправляет соответствующее сообщение.

# Ниже представлен код этой функции для удобства:

@game.bot.message_handler(commands=['answer'])
def write_answer(message):
    room_code, answer = message.text.split()[1], ' '.join(message.text.split()[2:])
    room = game.rooms.get(room_code)
    if room:
        for player in room.players:
            if player.name == message.from_user.username:
                if room.secret_word == answer:
                    game.bot.reply_to(message, "Congratulations! Your answer is correct.")
                    player.attempts = 0
                else:
                    player.attempts -= 1
                    if player.attempts > 0:
                        game.bot.reply_to(message, f"Wrong answer. You have {player.attempts} attempts left.")
                    else:
                        game.bot.reply_to(message, "Game over. You have no attempts left.")
                break
    else:
        game.bot.reply_to(message, "Failed to submit answer. Check the room code and try again.")

if __name__ == "__main__":
    
    game.bot.polling()