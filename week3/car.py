import os
import csv

class BaseCar:
    _file_type = [".jpg", ".jpeg", ".gif", ".png"]

    def __init__(self, car_type="unknown",brand="unknown",
                 photo_file_name="unknown", carrying="unknown",):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying
        self.car_type = car_type

    def get_photo_file_ext(self):
        root, ext = os.path.splitext(self.photo_file_name)
        return ext

class Car(BaseCar):
    def __init__(self,brand="unknown",
                 photo_file_name="unknown", carrying="unknown", passenger_seats_count=4):
        super(Car, self).__init__("car", brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count

class Truck(BaseCar):
    def __init__(self, brand="unknown",
                 photo_file_name="unknown", carrying="unknown", body_whl=None):
        super(Truck, self).__init__("truck",  brand, photo_file_name, carrying)
        try:
            self.body_whl = body_whl.split("x")
            self.body_length = float(self.body_whl[0])
            self.body_width = float(self.body_whl[1])
            self.body_height = float(self.body_whl[2])
        except (AttributeError, ValueError):   # ошибка типа, длинны, преобразования, Index?
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0

    def get_body_volume(self):
        self.volume = self.body_length * self.body_width * self.body_height
        return self.volume


class SpecMachine(BaseCar):
    def __init__(self, brand="unknown",
                 photo_file_name="unknown", carrying="unknown", extra=""):
        self.extra = extra
        super(SpecMachine, self).__init__("spec_machine",  brand, photo_file_name, carrying)




def get_car_list(file_name_csv):
    """
    Фнукция считывает файл в формате csv и собирает список из объектов
    :param file_name_csv:
    :return:
    """
    file_csv = open(file_name_csv, encoding="UTF-8")
    reader = csv.reader(file_csv, delimiter=";")
    car_list = []
    for row in reader:
        if row[0] == "car":
            car_list = get_car(car_list)
        if row[0] == "truck":
            car_list = get_truck(car_list)
        if row[0] == "spec_machine":
            car_list = get_spec_machine(car_list)
        else:
            continue
        return car_list



