import tempfile
import argparse
import os
import json

PATH = os.path.join(tempfile.gettempdir(), 'storage.data')


def get_data_file(path: str) -> object:
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        data = f.read()
        return json.loads(data)


def put_on_fail(keys, values, path=PATH) -> None:
    data = get_data_file(path)
    if keys in data:
        data[keys] += values
    else:
        data[keys] = values
    with open(path, "w") as f:
        f.write(json.dumps(data))


def get_on_fail(keys, path=PATH):
    data = get_data_file(path)
    if keys in data:
       print(*data[keys], sep=", ")
    else:
        return None


def parser() -> object:
    parser = argparse.ArgumentParser()
    parser.add_argument('--key')
    parser.add_argument('--value', nargs='+')
    data = parser.parse_args()
    return data.key, data.value


if __name__ == "__main__":
    key, value = parser()
    if not os.path.exists(PATH) and value is None:
        print()
    elif key and value:
        put_on_fail(key, value)
    elif key:  # передача данных по ключу плюс проверка создания файла
        get_on_fail(key)
    else:
        print('wrong command')
