#### patterns_home_work.py

## abstract factory.py
""" Задание 1: Магазин «Цифровые товары»

Представьте, что вы разрабатываете систему для онлайн-магазина, продающего разные виды цифровых товаров:
игры и музыку. В зависимости от типа товара необходимо создавать объекты, которые будут содержать
специфическую информацию и методы для загрузки, воспроизведения и отображения описания."""

from abc import ABC, abstractmethod

## Abstract Product
class Game(ABC):
    @abstractmethod
    def get_details(self) ->str:
        pass

    @abstractmethod
    def download(self) -> str:
        pass

    @abstractmethod
    def play(self) -> str:
        pass

## concreate product
class ActionGame(Game):
    def get_details(self) ->str:
        return '**** ЭКШН-ИГРА ****'

    def download(self) -> str:
        return 'Экшн-игра загружается'

    def play(self) -> str:
        return 'Экшн-игра запущена\n'

## concreate product
class PuzzleGame(Game):
    def get_details(self) ->str:
        return '**** РАЗВИВАЮЩАЯ ИГРА ****'

    def download(self) -> str:
        return 'Развивающаяся игра загружается'

    def play(self) -> str:
        return 'Развивающая игра запущена\n'

## Abstract Product
class Music(ABC):
    @abstractmethod
    def get_details(self) -> str:
        pass

    @abstractmethod
    def download(self) -> str:
        pass

    @abstractmethod
    def play(self) -> str:
        pass

## concreate product
class RockMusic(Music):
    def get_details(self) ->str:
        return '**** РОК-МУЗЫКА ****'

    def download(self) -> str:
        return 'РОК-музыка загружается'

    def play(self) -> str:
        return 'Воспроизведение Рок-музыки\n'

## concreate product
class JazzMusic(Music):
    def get_details(self) ->str:
        return '**** ДЖАЗ-МУЗЫКА ****'

    def download(self) -> str:
        return 'ДЖАЗ-музыка загружается'

    def play(self) -> str:
        return 'Воспроизведение джазовой музыки\n'

## Abstract factory
class DigitalProductFactory(ABC):
    @abstractmethod
    def set_game(self) -> Game:
        pass

    @abstractmethod
    def set_music(self) -> Music:
        pass

## concreate factory
class ActionGameFactory(DigitalProductFactory):
    def set_game(self) -> Game:
        return ActionGame()

    def set_music(self) -> Music:
        return JazzMusic()

## concreate factory
class  RockMusicFactory(DigitalProductFactory):
    def set_game(self) -> Game:
        return PuzzleGame()

    def set_music(self) -> Music:
        return RockMusic()

## client code
def show_all(factory: DigitalProductFactory)->None:
    game = factory.set_game()
    music = factory.set_music()
    print(game.get_details())
    print(game.download())
    print(game.play())
    print(music.get_details())
    print(music.download())
    print(music.play())

show_all(ActionGameFactory())
show_all(RockMusicFactory())



""" **** ЭКШН-ИГРА ****
Экшн-игра загружается
Экшн-игра запущена

**** ДЖАЗ-МУЗЫКА ****
ДЖАЗ-музыка загружается
Воспроизведение джазовой музыки

**** РАЗВИВАЮЩАЯ ИГРА ****
Развивающаяся игра загружается
Развивающая игра запущена

**** РОК-МУЗЫКА ****
РОК-музыка загружается
Воспроизведение Рок-музыки"""
