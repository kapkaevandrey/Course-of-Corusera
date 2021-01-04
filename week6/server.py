import asyncio

# список для хранения метрик в виде набора кортежей
# <сервер.метрика><значение><временная_отметка>
METRICS = []


class ClientServerProtocol(asyncio.Protocol):
    # TODO добавить опкисание протокола взаимодействия
    pass


# создаём цикл обработки событий
loop = asyncio.get_event_loop()
# создаём корутину объекта типа сервер
coroutine = loop.create_server(protocol_factory=ClientServerProtocol,
                               host="127.0.0.1",
                               port=8888)
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
