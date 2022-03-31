from dataclasses import dataclass
from colorama import Back, Fore, Style
from operator import attrgetter
import random
from typing import List

PROTECT = (1, 2, 3, 4, 5, 6, 7, 8, 9, 1)
ATTACK_PW = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
HEAL = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
PROTECTION = 50
POWER = 30
HEALTH = 100


@dataclass
class Thing:
    """Снаряжение игрока."""
    name: str
    PROTECT: float
    ATTACK_PW: float
    HEAL: float


@dataclass
class Person:
    """Базовый класс игрока."""
    name: str
    HEALTH: float
    POWER: float
    PROTECTION: float
    equips: list = None

    def set_things(self, equips: List[Thing]) -> None:
        """Экипировка игрока снаряжением."""
        self.equips = equips

    def get_damage(self, attack: float) -> None:
        """Механика получения урона."""
        final_PROTECTION = self.get_final_PROTECTION()
        self.HEALTH = self.HEALTH - (attack - attack * final_PROTECTION)

    def get_final_PROTECTION(self) -> float:
        """Общий процент защиты."""
        start_PROTECTION = 0
        for article in self.equips:
            sum_PROTECTION = start_PROTECTION + article.PROTECT
            final_PROTECTION = (sum_PROTECTION + self.PROTECTION) / 100
        return final_PROTECTION

    def get_final_HEALTH(self) -> float:
        """Общая величина здоровья."""
        start_HEALTH = 0
        for article in self.equips:
            sum_HEALTH = start_HEALTH + article.HEAL
            final_HEALTH = sum_HEALTH + self.HEALTH
        return final_HEALTH

    def get_final_POWER(self) -> float:
        """Общая величина силы атаки."""
        start_POWER = 0
        for article in self.equips:
            sum_POWER = start_POWER + article.ATTACK_PW
            final_POWER = sum_POWER + self.POWER
        return final_POWER


class Paladin(Person):
    """Класс наследуется от персонажа, количество  жизней
            и процент защиты умножается на 2."""
    def __init__(self, name, PROTECTION, POWER, HEALTH) -> None:
        super().__init__(name, PROTECTION, POWER, HEALTH)
        self.PROTECTION = self.PROTECTION * 2
        self.HEALTH = self.HEALTH * 2


class Warrior(Person):
    """Класс наследуется от персонажа,
    при этом атака умножается на 2 в конструкторе."""
    def __init__(self, name, PROTECTION, POWER, HEALTH) -> None:
        super().__init__(name, PROTECTION, POWER, HEALTH)
        self.POWER = self.POWER * 2


def create_equips() -> List[Thing]:
    """Создание набора экипировки."""
    equip = []
    article = ['Меч', 'Кольцо', 'Книга', 'Шлем', 'Поножи', 'Сапоги',
               'Топор', 'Посох', 'Кираса', 'Лук', 'Арбалет',
               'Кольчуга', 'Доспех']
    i = 0
    while i <= 9:
        equip.append(Thing(
                           article[i], 0,
                           random.randrange(0, 150, 1),
                           random.randrange(0, 10, 1)))
        i += 1
    equip = sorted(equip, key=attrgetter('PROTECT'))
    return equip


def generate_heroes(number_of_heroes: int) -> list:
    """Распределение по классам."""
    heroes = []
    names = [
        'Терминатор', 'Халк', 'Человек-паук', 'Рыцарь', 'Солдат',
        'Студент', 'Железный человек', 'Сокол', 'Боец', 'Охотник',
        'Росомаха', 'Капитан Америка', 'Тор', 'Дэдпул', 'Сорвиголова',
        'Блэйд', 'Человек-муравей', 'Оса', 'Веном', 'Хоукай']

    i = 0
    while i <= number_of_heroes:
        class_hero = random.choice([1, 2])
        if class_hero == 1:
            heroes.append(Paladin(names[i], HEALTH, PROTECTION, POWER))
        elif class_hero == 2:
            heroes.append(Warrior(names[i], HEALTH, PROTECTION, POWER))
        else:
            pass
        i += 1
    return heroes


def generate_attack(actor1, actor2) -> None:
    """Механика атаки."""
    attacking = actor1.POWER + actor1.get_final_POWER()
    damaging = attacking - attacking * actor2.get_final_PROTECTION()
    message = (f'{Fore.GREEN}{type(actor1).__name__} {actor1.name}'
               f'{Style.RESET_ALL} наносит удар по'
               f'{Fore.BLUE}{type(actor2).__name__}'
               f'{actor2.name}{Style.RESET_ALL} на {Fore.RED}'
               f'{str(round(damaging,1))}{Style.RESET_ALL} урона')
    actor2.get_damage(attacking)
    print(message)


def main(self) -> None:
    heroes = generate_heroes(number_of_heroes)
    equips = create_equips()

    for hero in heroes:
        number_equips = random.randrange(1, 4, 1)
        equips_set = []
        i = 0
        while i <= (number_equips):
            equips_number = random.randrange(0, 10, 1)
            equips_set.append(equips[equips_number])
            i += 1

        hero.set_things(equips_set)
    i = 0
    while not len(heroes) == 1:
        if len(heroes) == 2:
            attacker = heroes[0]
            defender = heroes[1]
        else:
            attacker = heroes[random.randrange(0, (number_of_heroes - i), 1)]
            defender = heroes[random.randrange(0, (number_of_heroes - i), 1)]
        turn = 1

        while (attacker.HEALTH > 0 and defender.HEALTH > 0
               and (not attacker == defender)):
            if turn % 2 != 0:
                generate_attack(attacker, defender)
            else:
                generate_attack(defender, attacker)
            turn += 1
        if attacker.HEALTH < 0 and turn > 1:
            print(f'    {Fore.RED}{attacker.name} погибает в бою и'
                  f'выбывает с арены {Style.RESET_ALL}')
            heroes.remove(attacker)
            i += 1
        elif defender.HEALTH < 0 and turn > 1:
            print(f'    {Fore.RED}{defender.name}  погибает в бою'
                  f'и выбывает с арены  {Style.RESET_ALL}')
            heroes.remove(defender)
            i += 1
        else:
            pass
    print(f'{Style.BRIGHT}{Back.GREEN}{Fore.BLUE}{heroes[0].name} побеждает!'
          f'Толпа ликует!{Style.RESET_ALL}')


if __name__ == '__main__':
    number_of_heroes = 19
    main(number_of_heroes)
