import random


class HuntTheWumpus:
    def __init__(self):
        # Карта печер (20 вершин додекаедра).
        # Кожна печера (ключ словника) має список суміжних печер.
        self.cave_map = {
            1: [2, 5, 8],
            2: [1, 3, 10],
            3: [2, 4, 12],
            4: [3, 5, 14],
            5: [1, 4, 6],
            6: [5, 7, 15],
            7: [16, 8, 17],
            8: [1, 7, 9],
            9: [8, 10, 18],
            10: [2, 9, 11],
            11: [10, 12, 19],
            12: [3, 11, 13],
            13: [12, 14, 20],
            14: [4, 13, 15],
            15: [6, 14, 16],
            16: [15, 17, 20],
            17: [7, 16, 18],
            18: [9, 17, 19],
            19: [11, 18, 20],
            20: [13, 16, 19]
        }

        # Визначаємо позиції небезпек.
        # Створюємо список печер, перемішуємо і розподіляємо.
        caves = list(self.cave_map.keys())
        random.shuffle(caves)
        self.wumpus = caves.pop()  # Вампус займає одну печеру.
        # Дві ями (bottomless pits)
        self.pits = [caves.pop(), caves.pop()]
        # Дві печери з супер кажанами
        self.bats = [caves.pop(), caves.pop()]

        # Початкова позиція гравця: вибираємо випадкову печеру, що не містить небезпек.
        while True:
            start = random.choice(list(self.cave_map.keys()))
            if start != self.wumpus and start not in self.pits and start not in self.bats:
                self.player = start
                break

        self.arrows = 5  # Кількість стріл
        self.game_over = False  # Прапорець завершення гри

    def show_status(self):
        """Виводить інформацію про поточну печеру, суміжні печери та дає підказки про небезпеки."""
        print("\nВи зараз у печері", self.player)
        print("Тунелі ведуть до: " + ", ".join(str(cave) for cave in self.cave_map[self.player]))

        # Підказки, якщо в суміжних печерах є небезпеки.
        warnings = []
        for adj in self.cave_map[self.player]:
            if adj == self.wumpus:
                warnings.append("Ви відчуваєте страшний запах!")
            if adj in self.pits:
                warnings.append("Відчувається протяг холодного повітря (підказка про яму)!")
            if adj in self.bats:
                warnings.append("Чуєте швидкий шелест крил (можливо, кажани поряд)!")
        # Вивід підказок без повторень.
        for warn in set(warnings):
            print(warn)

    def move_player(self, destination):
        """Обробка пересування гравця у вибрану печеру."""
        if destination not in self.cave_map[self.player]:
            print("Ви не можете безпосередньо потрапити до печери", destination)
            return

        self.player = destination

        # Перевіряємо, чи не потрапив гравець у печеру з небезпекою.
        if self.player == self.wumpus:
            print("Ви натрапили на Вампуса!")
            print("Вампус напав на вас – ви програли!")
            self.game_over = True
            return

        if self.player in self.pits:
            print("Ви впали в бездонну яму – гра завершена!")
            self.game_over = True
            return

        if self.player in self.bats:
            print("Супер кажани зловили вас і перенесли у випадкову печеру!")
            # Переносимо гравця у випадкову печеру.
            self.player = random.choice(list(self.cave_map.keys()))
            print("Вас випустили у печері", self.player)
            # Після перенесення перевіряємо повторно:
            if self.player == self.wumpus:
                print("На жаль, у цій печері чекає Вампус – ви програли!")
                self.game_over = True
                return
            if self.player in self.pits:
                print("Ви опинилися у ямі після перенесення – гра завершена!")
                self.game_over = True
                return

    def shoot_arrow(self, path):
        """
        Обробка пострілу стрілою.
        path - список печер, через які має пройти стріла.
        Якщо на якомусь відрізку стріла летить не за напрямком із підключених,
        вона перенаправляється у випадкову суміжну печеру.
        """
        current = self.player
        for next_cave in path:
            # Якщо задана печера не суміжна з поточною,
            # вибираємо випадкову суміжну печеру.
            if next_cave not in self.cave_map[current]:
                print(f"Стріла не може прямувати до печери {next_cave} з печери {current}.")
                next_cave = random.choice(self.cave_map[current])
                print(f"Стріла була відхилена до печери {next_cave}.")
            current = next_cave

            # Перевірка чи влучила стріла:
            if current == self.wumpus:
                print("Ваша стріла влучила у Вампуса! Ви перемогли!")
                self.game_over = True
                return
            if current == self.player:
                print("Стріла повернулася і влучила у вас – гра завершена!")
                self.game_over = True
                return

        # Якщо стріла не влучила у нічого.
        print("Стріла промахнулася!")

        # Вампус може пересунутися після пострілу (з ймовірністю 75%).
        if random.random() < 0.75:
            new_wumpus = random.choice(self.cave_map[self.wumpus])
            print(f"Вампус несподівано перемістився з печери {self.wumpus} до печери {new_wumpus}!")
            self.wumpus = new_wumpus
            if self.wumpus == self.player:
                print("Вампус перемістився безпосередньо у вашу печеру і напав – гра завершена!")
                self.game_over = True

        self.arrows -= 1
        if self.arrows <= 0:
            print("Ви витратили всі стріли – гра завершена!")
            self.game_over = True

    def play(self):
        """Основний ігровий цикл."""
        print("Вітаємо у грі «Світ Вампусу»!\n")
        while not self.game_over:
            self.show_status()
            print(f"У вас залишилося {self.arrows} стріл(и).")
            action = input("Що робити? (m – рух, s – постріл): ").lower().strip()
            if action.startswith("m"):
                try:
                    dest = int(input("Введіть номер печери, куди рухатись: "))
                except ValueError:
                    print("Невірне значення. Спробуйте ще раз.")
                    continue
                self.move_player(dest)
            elif action.startswith("s"):
                if self.arrows <= 0:
                    print("Стріл більше немає!")
                    continue
                try:
                    num_path = int(input("Введіть кількість печер, через які має пройти стріла (від 1 до 5): "))
                except ValueError:
                    print("Невірне значення.")
                    continue
                if num_path < 1 or num_path > 5:
                    print("Кількість печер має бути від 1 до 5.")
                    continue
                arrow_path = []
                print("Введіть послідовність номерів печер (через Enter):")
                for i in range(num_path):
                    try:
                        cave = int(input(f"Печера {i + 1}: "))
                    except ValueError:
                        print("Невірний номер, виберемо випадкове значення.")
                        cave = random.choice(self.cave_map[self.player])
                    arrow_path.append(cave)
                self.shoot_arrow(arrow_path)
            else:
                print("Невідома дія. Оберіть 'm' для руху або 's' для пострілу.")

        print("\nДякуємо за гру!")


def main():
    game = HuntTheWumpus()
    game.play()


if __name__ == '__main__':
    main()
