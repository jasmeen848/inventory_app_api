from enum import Enum


class Presentable(Enum):
    @property
    def text(self):
        return self.__presentable__[self.value]


class VehicleType(Presentable):
    __enumtype__ = int

    BIKE = 1
    CYCLE = 2
    CAR = 3
    BOAT = 4

    __presentable__ = {
        BIKE: 'bike',
        CYCLE: 'cycle',
        CAR: 'car',
        BOAT: 'boat',
    }
    