import asyncio


# список для хранения метрик в виде набора кортежей
# <сервер.метрика><значение><временная_отметка>


class ClientServerProtocol(asyncio.Protocol):
    error_answer = "error\nwrong command\n\n"
    METRICS = {}

    def connection_made(self, transport: asyncio.transports.BaseTransport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        message = data.decode("utf-8")
        try:
            method, *data = message.strip("\n").split()
            if method not in ("put", "get"):
                received = ClientServerProtocol.error_answer
            elif method == "put":
                received = self.put(data)
            elif method == "get":
                received = self.get(data)
            else:
                received = ClientServerProtocol.error_answer
        except (TypeError, ValueError):
            received = ClientServerProtocol.error_answer
        self.transport.write(received.encode("utf-8"))

    def get(self, data: str):
        if len(data) != 1:
            return ClientServerProtocol.error_answer
        data = data[0]
        recived = ""
        if data == "*":
            for name, values in ClientServerProtocol.METRICS.items():
                for value, time_stamp in values:
                    recived += f"{name} {value} {time_stamp}\n"
        elif data not in ClientServerProtocol.METRICS:
            print("ok\n\n")
            return "ok\n\n"
        elif data in ClientServerProtocol.METRICS:
            for value, time_stamp in ClientServerProtocol.METRICS[data]:
                recived += f"{data} {value} {time_stamp}\n"
        print(f"ok\n{recived}\n")
        return f"ok\n{recived}\n"

    def put(self, data: str):
        metric, value, time_stamp = data
        try:
            value = float(value)
            time_stamp = int(time_stamp)
        except TypeError:
            return ClientServerProtocol.error_answer
        if metric in ClientServerProtocol.METRICS:
            self.update_metrics(metric, value, time_stamp)
        else:
            ClientServerProtocol.METRICS[metric] = [(value, time_stamp)]
        return "ok\n\n"

    def update_metrics(self, metric, value, time_stamp):
        for key, values in enumerate(ClientServerProtocol.METRICS[metric]):
            if time_stamp == values[1]:
                ClientServerProtocol.METRICS[metric][key] = (value, time_stamp)
                return
        ClientServerProtocol.METRICS[metric].append((value, time_stamp))







def run_server(host, port):
    # создаём цикл обработки событий
    loop = asyncio.get_event_loop()
    # создаём корутину объекта типа сервер
    coroutine = loop.create_server(protocol_factory=ClientServerProtocol,
                                   host=host,
                                   port=port)
    # запуск сервера на исполнение пока объект Future не закончит своё исполнение
    server = loop.run_until_complete(coroutine)

    # запуск цикла событий до момента вызова метода .stop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Goodbye my little Server")

    # закрытие соединения с сервером
    server.close()
    # цикл событий ожидает выполнения корутины закрытия сервера
    loop.run_until_complete(server.wait_closed())
    # завершить цикл обработки событий
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 10001)
