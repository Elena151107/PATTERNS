""" Задание:

Создайте классы:
- Car с атрибутами license_plate, model, driver, location.
- Trip с атрибутами start_location, end_location, status, vehicle.
- Driver с атрибутами name, rating, bonuses.

Реализуйте:
- Adapter для интеграции данных о GPS местоположении автомобиля в формате, используемом внешним сервисом.
- Composite для группировки разных типов транспортных средств в один список для диспетчера (например, «все автомобили» или «все минивэны»)
- Decorator для расширения функциональности автомобилей, например, для предоставления премиум-сервисов.
- Flyweight для хранения общей информации о марках и моделях автомобилей.
- Proxy для защиты доступа к конфиденциальной информации (например, личные данные водителя)
- Facade для упрощения взаимодействия с системой для водителей и диспетчеров (например, оформление поездки и отслеживание маршрута).

Демонстрация работы:
- Добавьте несколько автомобилей с водителями и маршруты.
- Группируйте автомобили по типам (легковые, минивэны).
- Добавьте декораторы для автомобилей (например, премиум-услуги).
- Используйте фасад для создания новых поездок и отслеживания их статуса.
- Примените адаптер для интеграции с внешним GPS-сервисом.
- Заитите доступ к данным водителей с помоью прокси."""

from abc import ABC, abstractmethod

class Driver():
    def __init__(self, name: str=None, rating: float=0, bonuses: int=0):
        self.name = name
        self.rating = rating
        self.bonuses = bonuses

    def info_by_driver(self):
        return f'Водитель: {self.name}, rating: *{self.rating}*, bonuses: {self.bonuses}'


# component
class CarComponent(ABC):
    @abstractmethod
    def info_by_car(self, indent=0):
        pass


# хранит внутреннее состояние транспортного средства
class CarType(CarComponent):
    def __init__(self, car_brand: str=None, car_model: str=None,  license_plate: str=None):
        self.car_brand = car_brand
        self.car_model = car_model
        self.license_plate = license_plate

    def info_by_car(self, indent=0):
        return f'Автомобиль {self.car_brand} {self.car_model} с номерным знаком "{self.license_plate}"'

    def get_loc(self, location):
        pass

    def set_driver(self, driver):
        pass


# хранит внешнее состояние транспортного средства
class Car(CarComponent):
    def __init__(self, car_type: CarType):
        self.car_type = car_type
        self.car_brand = self.car_type.car_brand

    def info_by_car(self, indent=0):
        return self.car_type.info_by_car()

    def set_driver(self, driver: Driver):
        return driver.info_by_driver()

    def set_loc(self, location='База'):
        return f'Местонахождение автомобиля в настоящий момент: {location}'


class CarFactory():
    _list_cars = []

    @staticmethod
    def get_cars_in_park(*args: Car):
        for arg in args:
            key = f'{arg.car_type.car_brand} {arg.car_type.car_model}, рег.номер {arg.car_type.license_plate}'
            if arg not in CarFactory._list_cars:
                CarFactory._list_cars.append(key)
        return CarFactory._list_cars


#composite
class CarComposite(CarComponent):
    def __init__(self, name: str=None):
        self.name = name
        self._cars = []

    def add_car(self, car):
        self._cars.append(car)

    def remove(self, car):
        self._cars.remove(car)

    def info_by_car(self, indent=0):
        print(' '*(indent+4) + f'{self.name}:')
        for num, car in enumerate(self._cars, 1):
            print(" " * (indent + 8) + f'{num}: {car.info_by_car()}')


class GPS(ABC):
    @abstractmethod
    def get_location(self, location: str):
        pass


class GPSAdapter(GPS):
    def __init__(self, adapt: Car):
        self.adapt = adapt
        self.location = None
        self.car_brand = None

    def get_location(self, location: str='База'):
        return self.adapt.set_loc(location)

    def info_by_car(self):
        return self.adapt.info_by_car()

    def set_driver(self, driver: Driver):
        return driver.info_by_driver()

    def all_info(self):
        return f'{self.info_by_car()}\n{self.get_location()}'


#concreate decorator
class PremiumDecorator(GPSAdapter):
    def __init__(self, car: GPSAdapter, premium_paket: str='Включен премиум-сервис: улучшенное качество обслуживания, прохладительный приветственный напиток, Wi-Fi'):
        self.car = car
        self.premium_paket = premium_paket
        self.location = None
        self.car_brand = None

    def info_by_car(self, indent=0):
        return f'{self.car.info_by_car()}\n\t\t\t<< {self.premium_paket} >>'

    def all_info(self):
        return f'{self.car.all_info()}\n\t\t<< {self.premium_paket} >>'


class Trip():
    def __init__(self, start_location: str=None, end_location: str=None, premium_paket: bool=False):
        self.start_location = start_location
        self.end_location = end_location
        self.premium_paket = premium_paket
        self.status = 'Поиск машины'

    def __str__(self):
        return f'Заказ оформлен:\nПоездка от места: {self.start_location}, до места: {self.end_location}. {"Премиум-сервис включен" if self.premium_paket else ""}\nStatus: {self.status}'

    def add_car(self, car):
        if car is None:
            print('Идет поиск машины')
        else:
            return f'Status: Назначен {car.all_info()}\nПоездка от: {self.start_location}\n\t\t до: {self.end_location}'
  
    def set_driver(self, driver: Driver, car):
        if isinstance(car, GPSAdapter):
            driver.bonuses = 500
        if isinstance(car, PremiumDecorator):
            driver.bonuses = 1000
        return driver.info_by_driver()


#proxy
class TripProxy(Trip):
    def __init__(self, trip: Trip):
        self.trip = trip
        self.start_location = self.trip.start_location
        self.end_location = self.trip.end_location
        self.premium_paket = self.trip.premium_paket
        self.status = self.trip.status

        self.car_type = CarType()
        self.car = Car(self.car_type)

    def get_driver(self, driver, car):
        if driver is None:
            return 'Водитель не назначен'
        else:
            return f'{self.trip.add_car(car)}\n{self.trip.set_driver(driver, car)}'


#facade
class Facade():
    def __init__(self):
        self._trips = {}
        self._orders = []

    def add_trip(self, trip: TripProxy):
        if trip not in self._trips:
            self._trips[trip] = TripProxy(Trip())

    def get_status_trips(self):
        self.get_cars_in_park()
        print('<<<  Заказы: >>>')
        for num, i in enumerate(self._trips, 1):
            print(f'{num}.\n{i}')

    def get_orders(self, trip, driver, car):
        if trip not in self._orders:
            self._orders.append(trip.get_driver(driver, car))
        # if trip.car.car_brand in self._orders:
        #     for i in self._orders:
        #         trip.car[i].location = trip.car[i-1].end_location

    def show_orders(self):
        print('_____________________________________________')
        print('           ***  ORDERS: ***')
        for num, i in enumerate(self._orders, 1):
            print(f'--- Trip: {num}. ---\n{i}\n')

    def get_cars_in_park(self):
        print('ВЕСЬ ПАРК АВТОТРАНСПОРТА:')
        print('______________________')
        for num, i in enumerate(CarFactory.get_cars_in_park(), 1):
            print(f'{num}. {i}')
        print('_____________________________')
        print('_____________________________')

    def add_car_composite(self, composite, *args):
        for arg in args:
            composite.add_car(arg)

    def remove_composite(self, composite, car):
        composite.remove(car)

    def info_by_composite(self, *args):
        print('Тип транспортных средств:')
        print('______________________')
        for arg in args:
            arg.info_by_car()
        print('______________________')


driver_1 = Driver('John', 5.0)
driver_2 = Driver("Kate", 4.5)
driver_3 = Driver("Bob", 4.3)

car1 = Car(CarType('Toyota', 'Land Cruser Prado', 'E388AA 154'))
car2 = Car(CarType('Toyota', 'RAV 4', 'C734AO 154'))
car3 = Car(CarType('Renault', 'Logan', 'D124AE 154'))
car4 = Car(CarType('Mercedes', 'E class', 'A153AA 154'))
car5 = Car(CarType('Audi', 'E-tron', 'E455AM 154'))
car6 = Car(CarType('Chevrolet', 'Bolt', 'E999EE 154'))
car7 = Car(CarType('BMW', 'i3', 'M333NA 154'))

CarFactory.get_cars_in_park(car1, car2, car3, car4, car5, car6, car7)

gps1 = GPSAdapter(car1)
gps2 = GPSAdapter(car2)
gps3 = GPSAdapter(car3)
gps4 = GPSAdapter(car4)
gps5 = GPSAdapter(car5)
gps6 = GPSAdapter(car6)
gps7 = GPSAdapter(car7)

decorator_chevr_bolt = PremiumDecorator(gps6)
decorator_mercedes = PremiumDecorator(gps4)
decorator_prado = PremiumDecorator(gps1)

type1 = CarComposite('Все легковые автомобили')
type2 = CarComposite('Все минивэны')
type3 = CarComposite('Все электромобили')

print()

trip1 = Trip('ul.Dostoevskogo, 15', 'ul. Lenina, 25')
trip2 = Trip('pl.Lenina', 'pl.Red Prospect', premium_paket=True)
trip3 = Trip('ul.Distinkt, 23', 'ul. Minina, 99')
trip3 = Trip('ul.Distinkt, 23', 'ul. Minina, 99')

proxy1 = TripProxy(trip1)
proxy2 = TripProxy(trip2)
proxy3 = TripProxy(trip3)
proxy3 = TripProxy(trip3)

facade = Facade()

facade.add_car_composite(type1, car3, decorator_mercedes)
facade.add_car_composite(type2, decorator_prado, car2)
facade.add_car_composite(type3, car5, decorator_chevr_bolt, car7)
facade.info_by_composite(type1, type2, type3)
print()

facade.add_trip(proxy1)
facade.add_trip(proxy2)
facade.add_trip(proxy3)
facade.add_trip(proxy3)
facade.get_status_trips()
print()

facade.get_orders(proxy1, driver_1, decorator_mercedes)
facade.get_orders(proxy2, driver_2, gps3)
facade.get_orders(proxy3, driver_3, gps3)
facade.show_orders()
