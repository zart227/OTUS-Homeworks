
import random

class Card:
    def __init__(self):
        self.grid = self.generate_card()
    
    def generate_card(self):
        numbers = random.sample(range(1, 91), 15)
        card = [
            numbers[0:5],
            numbers[5:10],
            numbers[10:15]
        ]
        for row in card:
            row.sort()
            # Добавляем пустые ячейки (заменяем числа на '-'), чтобы каждая строка имела 9 клеток
            while len(row) < 9:
                row.insert(random.randint(0, len(row)), '-')
        return card
    
    def __str__(self):
        return "\n".join(" ".join(str(num).rjust(2) for num in row) for row in self.grid)
    
    def mark_number(self, number):
        for row in self.grid:
            if number in row:
                row[row.index(number)] = '-'
                return True
        return False
    
    def has_won(self):
        for row in self.grid:
            if not all(num == '-' for num in row):
                return False
        return True

class Player:
    def __init__(self, name, is_computer=False):
        self.name = name
        self.is_computer = is_computer
        self.card = Card()
    
    def __str__(self):
        return f"{self.name}{' (Computer)' if self.is_computer else ''}"
    
    def mark_number(self, number):
        return self.card.mark_number(number)
    
    def has_won(self):
        return self.card.has_won()

class Game:
    def __init__(self, player1_name, player2_name):
        self.players = [
            Player(player1_name),
            Player(player2_name, is_computer=True)
        ]
        self.barrels = list(range(1, 91))
        random.shuffle(self.barrels)
        self.called_numbers = []
    
    def play(self):
        print("Let's play Lotto!")
        while True:
            called_number = self.barrels.pop()
            self.called_numbers.append(called_number)
            
            print(f"\nНовый бочонок: {called_number} (осталось {len(self.barrels)})")
            
            for player in self.players:
                print(f"\n------ Карточка {player} ------")
                print(player.card)
                
                if player.is_computer:
                    mark = player.mark_number(called_number)
                    action = "зачеркнул" if mark else "продолжает"
                else:
                    while True:
                        action = input("Зачеркнуть цифру? (y/n): ").lower()
                        if action == 'y' or action == 'n':
                            break
                        else:
                            print("Пожалуйста, введите 'y' или 'n'.")
                    
                    if action == 'y':
                        mark = player.mark_number(called_number)
                        if mark:
                            print(f"Вы зачеркнули цифру {called_number}.")
                        else:
                            print(f"Цифры {called_number} нет на вашей карточке. Вы проиграли!")
                            return
                    else:
                        mark = False
                        print("Вы продолжаете игру.")
                
                if player.has_won():
                    print(f"\nПоздравляем, {player.name} победил!")
                    return
            
            input("\nНажмите Enter для продолжения...")

# Пример использования
if __name__ == "__main__":
    player1_name = input("Введите имя первого игрока: ")
    player2_name = input("Введите имя второго игрока (компьютера): ")
    
    game = Game(player1_name, player2_name)
    game.play()
