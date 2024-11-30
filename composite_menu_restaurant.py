"""Задание: Меню ресторана

Создай приложение, которое будет моделировать меню ресторана с помощью паттерна "Компоновщик". В меню ресторана могут быть как отдельные блюда, так и подменю
(например, подменю "Закуски", "Основные блюда" и "Напитки").
Требования
1. Блюдо (Leaf):
◦ Каждый элемент типа "Блюдо" представляет отдельное блюдо с названием, описанием и ценой.
◦ Должен предоставлять метод для получения полной информации о блюде (название, описание и цена).
2. Меню (Composite):
◦ Элемент типа "Меню" представляет собой список блюд и подменю.
◦ Должен поддерживать добавление и удаление других элементов (блюд и подменю).
◦ Должен предоставлять метод для вывода полной информации обо всех блюдах и подменю, которые он содержит.
3. Общий интерфейс:
◦ Создать общий интерфейс, который будут реализовывать и блюда, и меню. Интерфейс должен включать методы для вывода информации и получения общей стоимости.
4. Клиентский код:
◦ Написать пример клиентского кода, который создает меню ресторана, включая подменю и отдельные блюда.
◦ Реализовать метод, который выводит полное меню и рассчитывает общую стоимость блюд в нём. """

from abc import ABC, abstractmethod
from typing import List

# component
class MenuComponent(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def info(self, indent=0):
        pass

# листики - конечное блюдо
class Leaf(MenuComponent):
    def __init__(self, name: str, description: str, cost: int):
        self.name = name
        self.cost = cost
        self.description = description

    def cost(self):
        return self.cost

    def info(self, indent=0):
        return f'*** {self.name} *** \n\tОписание блюда: << {self.description} >> \n\t\tСтоимость: {self.cost} руб.\n'

# composite
class MenuRestaurant(MenuComponent):
    def __init__(self, title: str):
        self.title = title
        self._leafs: List[MenuComponent] = []
        self.summa_cost = 0

    def add_leaf(self, leaf: MenuComponent):
        self._leafs.append(leaf)

    def remove_leaf(self, leaf: MenuComponent):
        self._leafs.remove(leaf)

    def cost(self):
        self.summa_cost = sum(dish.cost for dish in self._leafs)
        print(f'------ Общая стоимость блюд в категории "{self.title}": {self.summa_cost} руб. ------')
        print('--------------------------------------------------------------------------')

    def info(self, indent=0):
        print(' '*indent + f'\n{self.title}\n')
        for leaf in self._leafs:
            print(leaf.info(indent+4))


def get_total_cost(*args):
    total=0
    summa = []
    for arg in args:
        if isinstance(arg, MenuRestaurant):
            total = arg.summa_cost
        if isinstance(arg, Leaf):
            total = arg.cost
        summa.append(total)
    print('--------------------------------------------------------------------------')
    print(f'\n****** Общая стоимость всех блюд в меню: {sum(summa)} руб. ******')


dish_seff = Leaf('Блюдо от Шефа', 'Шашлык из морепродуктов на гриле с овощами', 1500)

snacks = MenuRestaurant('ЗАКУСКИ')
main_leafs = MenuRestaurant('ОСНОВНЫЕ БЛЮДА')
deserts = MenuRestaurant('ДЕСЕРТЫ')
drinks = MenuRestaurant('НАПИТКИ')

snacks_1 = Leaf('Кольца каламаров', 'Жареные каламары в панировке', 200)
snacks_2 = Leaf('Луковые кольца', 'Жареный лук в панировке', 100)
snacks_3 = Leaf('Кольца осьминога', 'Жареный осьминог в панировке', 300)

main_leafs_1 = Leaf('Ягненок', 'Жареный ягненок с брусникой', 500)
main_leafs_2 = Leaf('Рыбка', 'Жареная рыбка с картофелем', 700)
main_leafs_3 = Leaf('Курочка', 'Вареная курица с миндалем и абрикосами', 400)

deserts_1 = Leaf('Торт Наполеон', 'Вкусный и нежный торт', 200)
deserts_2 = Leaf('Варенье', 'Вишневое варенье без косточек', 150)
deserts_3 = Leaf('Блины', 'Классические блинчики с начинкой', 200)

drinks_1 = Leaf('Coca-cola', 'Классическая Кока-Кола 200 ml', 200)
drinks_2 = Leaf('Чай', 'Черный/зеленый чай на выбор', 50)

print('________ МЕНЮ ________\n')
print(dish_seff.info())

snacks.add_leaf(snacks_1)
snacks.add_leaf(snacks_2)
snacks.add_leaf(snacks_3)
snacks.info(indent=4)
snacks.cost()

main_leafs.add_leaf(main_leafs_1)
main_leafs.add_leaf(main_leafs_2)
main_leafs.add_leaf(main_leafs_3)
main_leafs.info(indent=4)
main_leafs.cost()

deserts.add_leaf(deserts_1)
deserts.add_leaf(deserts_2)
deserts.add_leaf(deserts_3)
deserts.info(indent=4)
deserts.cost()

drinks.add_leaf(drinks_1)
drinks.add_leaf(drinks_2)
drinks.info(indent=4)
drinks.cost()

get_total_cost(snacks, main_leafs, deserts, drinks, dish_seff)
