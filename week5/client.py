import socket
import time


# класс пользовательское исключение
class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        # регисрируем host и port
        self._host = host
        self._port = port
        self._timeout = timeout
        # создаём соединение
        try:
            self.sock = socket.create_connection((host, port), timeout)
        except socket.error:
            raise ClientError("соединение не установлено")

    def _read_data(self):
        # пытаемся получить ответ от сервера
        try:
            message = self.sock.recv(1024).decode("utf-8")
        except socket.error:
            raise ClientError("ответ от сервера не получен")

        # анализируем результат ответа получаем результат и список с данными
        result, *data = message.split("\n")[:-2]
        if result != "ok":
            raise ClientError("операция не выполнена")
        return data

    def put(self, metric: str, value: float, timestamp=None):
        timestamp = int(time.time()) if timestamp is None else timestamp
        try:
            self.sock.send(f"put {metric} {value} {timestamp}\n".encode("utf-8"))
        except socket.error:
            raise ClientError("не удалось отправить данные")
        self._read_data()

    def get(self, metric_name):
        try:
            self.sock.send(f"get {metric_name}\n".encode("utf-8"))
        except socket.error:
            raise ClientError("не уадлось отправить сообщение")

        data = self._read_data()
        metrics = {}
        if not data:
            return metrics
        #  поптыка заполнение словаря с данными по ключам типа сервер.метрика с содержимым
        # <имя_сервераю.метрика> <занчение> <временная метка>
        try:
            for value in data:
                server, value, time_stamp = value.split()
                if server in metrics:
                    metrics[server].append((int(time_stamp), float(value)))
                else:
                    metrics[server] = [(int(time_stamp), float(value))]
        # не корректные данные
        except ValueError:
            raise ClientError("не корректный формат данных")

        # сортировка словаря по значению time
        for name in metrics:
            metrics[name] = sorted(metrics[name], key=lambda x: x[0], reverse=False)
        return metrics

    def close(self):
        try:
            self.sock.close()
        except socket.error:
            raise ClientError("не удалось закрыть соединение")
