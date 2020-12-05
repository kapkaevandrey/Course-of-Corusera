import os

class BaseCar:

    _file_type = [".jpg", ".jpeg", ".gif", ".png"]

    def __init__(self, car_type="unknown",brand="unknown",
                 photo_file_name="unknown", carrying="unknown",):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying
        self.car_type = car_type

    def get_photo_file_ext(self):
        try:
            root, ext = os.path.splitext(self.photo_file_name)
        except IOError:
            return "File not exist"
        if ext not in self._file_type:
            ext = "unknown"
            return f"invalid format. Format of file must be {','.join(self._file_type)} not {ext}"
        else:
            return ext

class Car(BaseCar):
    def __init__(self,brand="unknown",
                 photo_file_name="unknown", carrying="unknown", passenger_seats_count=4):
        super(Car, self).__init__("Car", brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count

class Truk(BaseCar):
    def __init__(self, body_whl=0):
        self.body_whl = body_whl
        try:
            pass  # релизация не валидных значений
        except:   # ошибка типа, длинны, преобразования, Index?
            pass

        super(Truk, self).__init__()


class SpecMachine(BaseCar):
    def __init__(self, extra="unknown"):
        self.extra = extra
        super(SpecMachine, self).__init__()

car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')
print(car.car_type, car.brand, car.photo_file_name, car.carrying,
      car.passenger_seats_count, sep='\n')
print(car.get_photo_file_ext())


