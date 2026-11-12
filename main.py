import random

# ==================== КЛАССЫ ====================

class Card:
    """Класс, описывающий одну карту бункера."""
    def __init__(self, card_type, name, value):
        self.card_type = card_type  # Тип карты (Профессия, Здоровье и т.д.)
        self.name = name            # Название карты
        self.value = value          # Значение/описание эффекта карты

    def __str__(self):
        return f"[{self.card_type}] {self.name}: {self.value}"


class Player:
    """Класс, описывающий игрока (человека или бота)."""
    def __init__(self, name, is_bot=False):
        self.name = name
        self.is_bot = is_bot
        self.cards = []             # Карты на руке
        self.revealed_cards = []    # Карты, которые игрок уже открыл
        self.is_alive = True        # Флаг «жив» (находится в бункере)

    def open_card(self):
        """Метод открыть_карту(): берет первую карту из руки и переносит в открытые."""
        if self.cards:
            card = self.cards.pop(0)
            self.revealed_cards.append(card)
            return card
        return None

    def get_alive_status(self):
        return "Жив" if self.is_alive else "Покинул бункер"


class Game:
    """Класс, управляющий логикой и состоянием игры."""
    def __init__(self):
        self.players = []
        self.round_number = 1
        self.phase = "MENU"  # MENU, SETUP, OPENING, DISCUSSION, VOTING, GAME_OVER
        self.deck = []
        self.bunker_condition = "ЯДЕРНАЯ ЗИМА. Запасы еды и места в бункере ограничены. Выжить смогут только двое."
        self.init_deck()

    def init_deck(self):
        """Инициализация колоды карт."""
        cards_data = [
            ("Профессия", "Хирург", "Может проводить сложные операции и спасать жизни"),
            ("Профессия", "Сантехник", "Умеет чинить трубы и обеспечивать воду"),
            ("Профессия", "Аграрий", "Знает, как выращивать еду в замкнутом пространстве"),
            ("Профессия", "Психолог", "Может предотвращать конфликты и депрессии"),
            ("Здоровье", "Абсолютно здоров", "Нет хронических заболеваний"),
            ("Здоровье", "Астма", "Нуждается в постоянном доступе к ингалятору"),
            ("Здоровье", "Отличная физ. форма", "Может таскать тяжести и работать на износ"),
            ("Биография", "Бывалый турист", "Выживал в дикой природе, знает узлы"),
            ("Биография", "Домосед", "Предпочитает сидеть на одном месте"),
            ("Биография", "Многодетный отец", "Привык заботиться о других"),
            ("Фобия", "Клаустрофобия", "Панически боится замкнутых пространств бункера"),
            ("Фобия", "Нет фобий", "Уравновешенная психика"),
            ("Фобия", "Боязнь темноты", "Тратит лишние ресурсы на освещение"),
            ("Спецфакт", "Знает 5 языков", "Может общаться с иностранными выжившими"),
            ("Спецфакт", "Умеет играть на гитаре", "Развлекает и поднимает моральный дух"),
            ("Спецфакт", "Скрытный вор", "Может красть ресурсы у других обитателей"),
            ("Багаж", "Семена растений", "Может организовать ферму в бункере"),
            ("Багаж", "Аптечка", "Запас редких лекарств"),
            ("Багаж", "Огнестрельное оружие", "Может защитить бункер, но опасно внутри"),
            ("Багаж", "Коллекция книг", "Занимает место, но сохраняет знания"),
        ]
        # Перемешиваем и создаем объекты карт
        random.shuffle(cards_data)
        self.deck = [Card(c_type, name, value) for c_type, name, value in cards_data]

    def show_menu(self):
        """Главное меню."""
        self.phase = "MENU"
        while True:
            print("\n" + "="*40)
            print("       КОНСОЛЬНАЯ ИГРА «БУНКЕР»")
            print("="*40)
            print("1. Начать игру")
            print("2. Правила")
            print("3. Выход")
            print("="*40)
            
            choice = input("Выберите действие (1-3): ").strip()
            
            if choice == '1':
                self.setup_game()
                self.play()
                break
            elif choice == '2':
                self.show_rules()
            elif choice == '3':
                print("Спасибо за игру! До свидания.")
                exit()
            else:
                print("Неверный ввод. Пожалуйста, введите 1, 2 или 3.")

    def show_rules(self):
        """Вывод правил игры."""
        print("\n--- ПРАВИЛА ИГРЫ ---")
        print("В мире произошла катастрофа. Место в бункере ограничено.")
        print("В игре участвуют 4 игрока (2 живых и 2 бота).")
        print("Каждому выдается по 3 карты (Профессия, Здоровье, Фобия и т.д.).")
        print("Каждый раунд вы открываете по одной карте и обсуждаете,")
        print("кто достоин остаться. Затем происходит голосование.")
        print("Игрок, набравший больше всех голосов, покидает бункер.")
        print("Игра идет до тех пор, пока не останется половина игроков (2 человека).")
        input("\nНажмите Enter, чтобы вернуться в меню...")

    def setup_game(self):
        """Настройка игры: создание игроков и раздача карт."""
        self.phase = "SETUP"
        print("\n--- НАЧАЛО ИГРЫ ---")
        print(f"Условие в бункере: {self.bunker_condition}")
        
        # Создание живых игроков
        name1 = input("Введите имя первого живого игрока: ").strip() or "Игрок 1"
        name2 = input("Введите имя второго живого игрока: ").strip() or "Игрок 2"
        
        self.players = [
            Player(name1, is_bot=False),
            Player(name2, is_bot=False),
            Player("Бот-Альфа", is_bot=True),
            Player("Бот-Бета", is_bot=True)
        ]
        
        # Раздача карт (по 3 карты каждому)
        for player in self.players:
            player.cards = [self.deck.pop() for _ in range(3)]
            
        print(f"\nИгроки {name1} и {name2} готовы. Боты подключены.")
        input("Нажмите Enter, чтобы начать 1-й раунд...")

    def play(self):
        """Основной игровой цикл."""
        while not self.check_win_condition():
            self.round_loop()
        self.announce_winners()

    def round_loop(self):
        """Логика одного раунда."""
        print(f"\n{'='*20} РАУНД {self.round_number} {'='*20}")
        
        self.opening_phase()
        self.discussion_phase()
        self.voting_phase()
        
        self.round_number += 1

    def opening_phase(self):
        """Фаза открытия карт."""
        self.phase = "OPENING"
        print("\n--- ФАЗА ОТКРЫТИЯ КАРТ ---")
        
        alive_players = [p for p in self.players if p.is_alive]
        
        for player in alive_players:
            if not player.cards:
                continue
                
            if player.is_bot:
                # Боты открывают карты автоматически
                card = player.open_card()
                print(f"{player.name} (Бот) открывает карту: {card}")
            else:
                # Живые игроки открывают карты по нажатию Enter
                input(f"{player.name}, нажмите Enter, чтобы открыть карту...")
                card = player.open_card()
                print(f"{player.name} открывает карту: {card}")
                
        print("\nВсе открытые карты на столе:")
        for player in alive_players:
            if player.revealed_cards:
                print(f"  {player.name}:")
                for card in player.revealed_cards:
                    print(f"    - {card}")

    def discussion_phase(self):
        """Фаза обсуждения."""
        self.phase = "DISCUSSION"
        print("\n--- ФАЗА ОБСУЖДЕНИЯ ---")
        print("Обсудите между собой, кто из игроков наиболее полезен для бункера,")
        print("а кто представляет угрозу или обузу.")
        
        # Имитация реплик ботов
        bot_phrases = [
            "Бот-Альфа: Мне кажется, нам стоит оставить людей с полезными навыками.",
            "Бот-Бета: Я не доверяю тем, у кого плохие карты здоровья.",
            "Бот-Альфа: В бункере нужна дисциплина, а не фобии.",
            "Бот-Бета: Предлагаю выгнать того, кто меньше всего полезен."
        ]
        print(random.choice(bot_phrases))
        
        input("\nКогда закончите обсуждение в реальности, нажмите Enter для перехода к голосованию...")

    def voting_phase(self):
        """Фаза голосования."""
        self.phase = "VOTING"
        print("\n--- ФАЗА ГОЛОСОВАНИЯ ---")
        
        alive_players = [p for p in self.players if p.is_alive]
        votes = {p.name: 0 for p in alive_players}
        
        # Выводим список тех, за кого можно голосовать
        print("Кого вы хотите выгнать из бункера?")
        for i, player in enumerate(alive_players, 1):
            bot_tag = " [БОТ]" if player.is_bot else ""
            print(f"  {i}. {player.name}{bot_tag}")
            
        # Голосование живых игроков
        for human in [p for p in alive_players if not p.is_bot]:
            while True:
                try:
                    choice = int(input(f"\n{human.name}, введите номер игрока для исключения: "))
                    if 1 <= choice <= len(alive_players):
                        target = alive_players[choice - 1]
                        votes[target.name] += 1
                        print(f"Ваш голос отдан за: {target.name}")
                        break
                    else:
                        print("Неверный номер, попробуйте снова.")
                except ValueError:
                    print("Пожалуйста, введите число.")

        # Голосование ботов (выбирают случайную цель)
        for bot in [p for p in alive_players if p.is_bot]:
            target = random.choice(alive_players)
            votes[target.name] += 1
            print(f"{bot.name} (Бот) отдает голос за: {target.name}")

        # Подсчет голосов и исключение
        print("\n--- РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ ---")
        for name, count in votes.items():
            print(f"  {name}: {count} голос(ов)")
            
        max_votes = max(votes.values())
        candidates_to_kick = [name for name, count in votes.items() if count == max_votes]
        
        if len(candidates_to_kick) > 1:
            kicked_name = random.choice(candidates_to_kick)
            print(f"\nНичья! Бункер принимает жестокое решение случайно...")
        else:
            kicked_name = candidates_to_kick[0]
            
        # Исключаем игрока
        for player in self.players:
            if player.name == kicked_name:
                player.is_alive = False
                print(f"Игрок {kicked_name} покидает бункер и отправляется на верную гибель!")
                break
                
        input("\nНажмите Enter, чтобы продолжить...")

    def check_win_condition(self):
        """Проверка условия победы: когда остается половина игроков (2 из 4)."""
        alive_count = sum(1 for p in self.players if p.is_alive)
        return alive_count <= (len(self.players) / 2)

    def announce_winners(self):
        """Объявление победителей."""
        self.phase = "GAME_OVER"
        print("\n" + "="*40)
        print("           ИГРА ОКОНЧЕНА")
        print("="*40)
        print("Двери бункера закрываются. Выживают только сильнейшие!")
        print("\nПобедители, оставшиеся в бункере:")
        for player in self.players:
            if player.is_alive:
                print(f"  - {player.name}")
        print("\nСпасибо за игру!")
        input("Нажмите Enter, чтобы вернуться в главное меню...")


# ==================== ТОЧКА ВХОДА ====================

if __name__ == "__main__":
    game = Game()
    game.show_menu()