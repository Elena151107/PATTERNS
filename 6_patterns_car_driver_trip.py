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
from typing import Dict,List

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
    def __init__(self, name: str):
        self.name = name
        self._cars = []

    def add_car(self, car: CarComponent):
        self._cars.append(car)

    def remove(self, car: CarComponent):
        self._cars.remove(car)

    def info_by_car(self, indent=0):
        print(' '*(indent+4) + f'{self.name}:')
        for num, car in enumerate(self._cars, 1):
            print(" "*(indent+8) + f'{num}: {car.info_by_car()}')


class GPS(ABC):
    @abstractmethod
    def get_location(self, location: str):
        pass


class GPSAdapter(GPS):
    def __init__(self, adapt: Car):
        self.adapt = adapt
        # self.location = None

    def get_location(self, location: str='База'):
        # self.location = location
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

    def info_by_car(self, indent=0):
        return f'{self.car.info_by_car()}\n\t\t\t<<{self.premium_paket}>>'

    def all_info(self):
        return f'{self.car.all_info()}\n\t\t\t<<{self.premium_paket}>>'


class Trip():
    def __init__(self, start_location: str=None, end_location: str=None, premium_paket: bool=False, vehicle=None, driver=None):
        self.start_location = start_location
        self.end_location = end_location
        self.premium_paket = premium_paket
        self.status = 'Поиск машины'
        self.vehicle = vehicle
        self.driver = driver

    def __str__(self):
        return f'Заказ оформлен:\nПоездка от места: {self.start_location} до места: {self.end_location}. {"Премиум-сервис включен" if self.premium_paket else ""}\nStatus: {self.status}'

    def add_car(self, vehicle: GPSAdapter):
        if vehicle is None:
            print('Идет поиск машины')
        else:
            return f'Заказ подтвержден:\nПоездка от места: {self.start_location} до места: {self.end_location}. \nStatus: Назначен {vehicle.all_info()}'

    def add_car_with_premium(self, vehicle: PremiumDecorator):
        if vehicle is None:
            print('Идет поиск машины')
        else:
            return f'Заказ подтвержден:\nПоездка от места: {self.start_location} до места: {self.end_location}. \nStatus: Назначен {vehicle.all_info()}'

#proxy
class TripProxy(Trip):
    def __init__(self, trip: Trip):
        self.trip = trip

    def get_driver(self, vehicle: GPSAdapter, driver: Driver):
        if not self.trip.add_car(vehicle):
                return 'Водитель не назначен'
        else:
            driver.bonuses += 500
            return f'{self.trip.add_car(vehicle)}\n{vehicle.set_driver(driver)}'

    def get_driver_premium(self, vehicle: PremiumDecorator, driver: Driver):
        if not self.trip.add_car_with_premium(vehicle):
            return 'Водитель не назначен'
        else:
            driver.bonuses += 1000
            return f'{self.trip.add_car_with_premium(vehicle)}\n{vehicle.set_driver(driver)}'


#facade
class Facade():
    def __init__(self):
        self.trip = TripProxy(Trip())
        self._trips = {}

     def add_trip(self, trip: TripProxy):
        if trip in self._trips:
            print(f'ВНИМАНИЕ: Такой заказ уже был создан и подтвержден!\n')
        else:
            self._trips[trip] = TripProxy(Trip())

    def get_status_orders(self):
        self.get_cars_in_park()
        print('\n***** ORDERS: *****')
        for num, i in enumerate(self._trips, 1):
            print(f'{num}.\n{i}')

    def get_cars_in_park(self):
        print('ПАРК АВТОТРАНСПОРТА:')
        print('______________________')
        for num, i in enumerate(CarFactory.get_cars_in_park(), 1):
            print(f'{num}. {i}')
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

print('ПАРК ТРАНСПОРТНЫХ СРЕДСТВ:')
type1.add_car(car3)
type1.add_car(decorator_mercedes)
type1.info_by_car()

type2.add_car(decorator_prado)
type2.add_car(car2)
type2.info_by_car()

type3.add_car(car5)
type3.add_car(decorator_chevr_bolt)
type3.add_car(car7)
type3.info_by_car()
print()

print('<<<  Заказы на оформлении: >>>')
print('________________________________')
print('*** TRIP 1 ***')
trip1 = Trip('ul.Dostoevskogo, 15', 'ul. Lenina, 25')
print(trip1)
print()
proxy1 = TripProxy(trip1)
proxy1 = proxy1.get_driver(gps3,driver_1)

print('*** TRIP 2 ***')
trip2 = Trip('pl.Lenina', 'pl.Red Prospect', premium_paket=True)
print(trip2)
print()
proxy2 = TripProxy(trip2)
proxy2 = proxy2.get_driver_premium(decorator_mercedes, driver_2)

print('*** TRIP 3 ***')
trip3 = Trip('ul.Distinkt, 23', 'ul. Minina, 99')
print(trip3)
print()
proxy3 = TripProxy(trip3)
proxy3 = proxy3.get_driver_premium(decorator_mercedes,driver_1)

facade = Facade()
facade.add_trip(proxy1)
facade.add_trip(proxy2)
facade.add_trip(proxy3)
facade.get_status_orders()
