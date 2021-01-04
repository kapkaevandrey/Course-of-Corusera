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
        except socket.error as err:
            raise ClientError("the connection is not established", err)

    def _read_data(self):
        # пытаемся получить ответ от сервера
        message = b""
        try:
            while message.endswith(b"\n\n"):
                message += self.sock.recv(1024).decode("utf-8")
        except socket.error as err:
            raise ClientError("no response received from the server", err)

        # анализируем результат ответа получаем результат и список с данными
        result, *data = message.split("\n")[:-2]
        if result != "ok":
            raise ClientError("operation failed")
        return data

    def put(self, metric: str, value: float, timestamp=None):
        timestamp = int(time.time()) if timestamp is None else timestamp
        try:
            self.sock.send(f"put {metric} {value} {timestamp}\n".encode("utf-8"))
        except socket.error as err:
            raise ClientError("failed to send data",  err)
        self._read_data()

    def get(self, metric_name):
        try:
            self.sock.send(f"get {metric_name}\n".encode("utf-8"))
        except socket.error as er:
            raise ClientError("couldn't send a request", er)

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
        except ValueError as er:
            raise ClientError("invalid data format", er)

        # сортировка словаря по значению time
        for name in metrics:
            metrics[name] = sorted(metrics[name], key=lambda x: x[0], reverse=False)
        return metrics

    def close(self):
        try:
            self.sock.close()
        except socket.error as er:
            raise ClientError("failed to close connection", er)
