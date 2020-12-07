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


def valid_photo(file_name):
    try:
        root, ext = os.path.splitext(file_name)
        if ext in BaseCar._file_type:
            return True
        else:
            return False
    except IOError:
        return False



def get_car(data, data_row):
    car = [data_row[i] for i in [1, 3, 5, 2]]
    if not any(car):
        return data
    if valid_photo(car[1]):
        data.append(Car(*car))
    return data


def get_truck(data, data_row):
    truck = [data_row[i] for i in [1, 3, 5, 4]]
    if not any(truck[:-1]):
        return data
    if valid_photo(truck[1]):
        data.append(Truck(*truck))
    return data


def get_spec_car(data, data_row):
    spec_machine = [data_row[i] for i in [1, 3, 5, 6]]
    if not any(spec_machine):
        return data
    if valid_photo(spec_machine[1]):
        data.append(SpecMachine(*spec_machine))
    return data

def get_car_list(file_name_csv:object):
    """
    Фнукция считывает файл в формате csv и собирает список из объектов
    :param file_name_csv:
    :return:
    """
    file_csv = open(file_name_csv, encoding="UTF-8")
    reader = csv.reader(file_csv, delimiter=";")
    car_data = [row for row in reader]
    file_csv.close()
    data_len = len(car_data[0])
    car_list = []
    for row in car_data:
        if len(row) != data_len:
            continue
        if row[0] == "car":
            car_list = get_car(car_list, row)
        elif row[0] == "truck":
            car_list = get_truck(car_list, row)
        elif row[0] == "spec_machine":
            car_list = get_spec_car(car_list, row)
        else:
            continue
    return car_list


if __name__ == "__main__":
    cars = get_car_list("coursera_week3_cars.csv")
    for car in cars:
        print(type(car))
        print(car.brand)

