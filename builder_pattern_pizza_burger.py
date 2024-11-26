""" Задание 2: Конструктор пиццы и бургеров.

Создайте систему, где пользователь может «собрать» пиццу или бургер, используя паттерн Builder.
У пиццы и бургера будут различные параметры, которые можно настраивать."""

## product
class Pizza:
    def __init__(self):
        self.testo = None
        self.size = None
        self.sauce = None
        self.fillings = []

    def __str__(self):
        return f'Pizza with: {self.testo} тесто , {self.size} размер, {self.sauce} соус, добавки: {self.fillings}'
## product
class Burger:
    def __init__(self):
        self.bun = None
        self.cutlet = None
        self.elements = []

    def __str__(self):
        return f'Burger with: {self.bun} булочка, {self.cutlet} котлета, добавки: {self.elements}'

class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def set_testo(self, testo: str = 'толстое'):
        self.pizza.testo = testo
        return self

    def set_size(self, size: str = 'маленький'):
        self.pizza.size = size
        return self

    def set_sauce(self, sauce: str = 'томатный'):
        self.pizza.sauce = sauce
        return self

    def add_fillings(self, fillings: list = ['без начинки']):
        self.pizza.fillings = fillings
        return self

    def result(self):
        return self.pizza

# concreate Builder
class BurgerBuilder:
    def __init__(self):
        self.burger = Burger()

    def set_bun(self, bun: str = 'классическая'):
        self.burger.bun = bun
        return self

    def set_cutlet(self, cutlet: str = 'курица'):
        self.burger.cutlet = cutlet
        return self

    def add_elements(self, elements: list = ['без начинки']):
        self.burger.elements = elements
        return self

    def result(self):
        return self.burger

## Director
class UserInterface():
    def cook_standart_pizza(self):
        pizza = PizzaBuilder()
        pizza.set_testo().set_size().set_sauce().add_fillings()
        return pizza.result()

    def cook_standart_burger(self):
        burger = BurgerBuilder()
        burger.set_bun().set_cutlet().add_elements()
        return burger.result()

    def create_pizza(self, testo, size, sauce, fillings):
        builder = PizzaBuilder()
        builder.set_testo(testo).set_size(size).set_sauce(sauce).add_fillings(fillings)
        return builder.result()

    def create_burger(self, bun, cutlet, elements):
        builder = BurgerBuilder()
        builder.set_bun(bun).set_cutlet(cutlet).add_elements(elements)
        return builder.result()

def main():
    action = input('выберите блюдо: PIZZA/BURGER ').strip().upper()
    type = input('Хотите стандартный состав или хотите сделать свой вариант? Выберите: STANDART / NEW  ').strip().upper()
    choice = UserInterface()
    try:
        if type == 'STANDART' and action == 'PIZZA':
            print('Вы выбрали: ', choice.cook_standart_pizza())
        elif type == 'STANDART' and action == 'BURGER':
            print('Вы выбрали: ', choice.cook_standart_burger())
        elif type == 'NEW' and action == 'PIZZA':
            testo = input('Выберите тесто: THICK / THIN  ').strip().upper()
            if testo not in ['THICK', 'THIN']:
                raise Exception('Нет такого вида теста')
            size = input('Выберите размер: SMALL / MIDDLE / KING  ').strip().upper()
            if size not in ['SMALL', 'MIDDLE', 'KING']:
                raise Exception('Нет такого размера')
            sauce = input('Выберите соус: TOMATO / CREAM  ').strip().upper()
            if sauce not in ['TOMATO', 'CREAM']:
                raise Exception('Нет такого соуса')
            fillings = input('Выберите начинку через пробел: MOZZARELLA / PEPPERONI / MUSHROOMS / OLIVE / RED-PEPPER / NOT ').strip().upper().split()
            for fil in fillings:
                if fil not in ['MOZZARELLA', 'PEPPERONI', 'MUSHROOMS', 'OLIVE', 'RED-PEPPER', 'NOT']:
                    raise Exception('Нет такой начинки')
            print('Вы выбрали: ', choice.create_pizza(testo, size, sauce, fillings))
        elif type == 'NEW' and action == 'BURGER':
            bun = input('Выберите булку: CLASSIC / RYE / GLUTEN-FREE  ').strip().upper()
            if bun not in ['CLASSIC', 'RYE', 'GLUTEN-FREE']:
                raise Exception('Нет такого вида булки')
            cutlet = input('Выберите котлету: CHICKEN / BEEF / VEGETABLE  ').strip().upper()
            if cutlet not in ['CHICKEN', 'BEEF', 'VEGETABLE']:
                raise Exception('Нет такого вида котлеты')
            elements = input('Выберите начинку через пробел: CHEESE / SALAD / TOMATO / BACON / RED-PEPPER / NOT ').strip().upper().split()
            for el in elements:
                if el not in ['CHEESE', 'SALAD', 'TOMATO', 'BACON', 'RED-PEPPER', 'NOT']:
                    raise Exception('Нет такой начинки')
            print('Вы выбрали: ', choice.create_burger(bun, cutlet, elements))
        else:
            raise Exception('Нет такого блюда в меню')
    except ValueError as e:
        print(e)

main()


##
""" выберите блюдо: PIZZA/BURGER burger

Хотите стандартный состав или хотите сделать свой вариант? Выберите: STANDART / NEW  standart
Вы выбрали:  Burger with: классическая булочка, курица котлета, добавки: ['без начинки'] """
##
""" выберите блюдо: PIZZA/BURGER pizza

Хотите стандартный состав или хотите сделать свой вариант? Выберите: STANDART / NEW  new
Выберите тесто: THICK / THIN  thin
Выберите размер: SMALL / MIDDLE / KING  middle
Выберите соус: TOMATO / CREAM  tomato
Выберите начинку через пробел: MOZZARELLA / PEPPERONI / MUSHROOMS / OLIVE / RED-PEPPER / NOT pepperoni olive
Вы выбрали:  Pizza with: THIN тесто , MIDDLE размер, TOMATO соус, добавки: ['PEPPERONI', 'OLIVE'] """
