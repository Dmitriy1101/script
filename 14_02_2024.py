import json, datetime


def hide_info(data: str) -> str:
    """Преобразуем строку в строку скрывая лишнее"""

    if not data:
        return ""
    elif data.startswith("Счет"):
        return f"Счет **{data[-4:]}"
    else:
        return f"{data[:-12]} {data[-12:-10]}** **** {data[-4:]}"


def get_data():
    """Читаем с файла."""
    with open(f"operations.json", encoding="utf-8") as f:
        jdata = json.load(f)
    return jdata


def get_executed_data(data_list: list[dict]) -> list:
    """Получаем отсортированные данные извлечём и вернём EXECUTED"""

    new_data: list = []
    for data in data_list:
        if data.get("state") == "EXECUTED":
            time = datetime.datetime.strftime(
                datetime.datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%S.%f"),
                "%d.%m.%Y",
            )
            new_data.append(
                f'{time} {data["description"]}\
                \n{hide_info(data.get("from"))} -> {hide_info(data["to"])}\
                \n{data["operationAmount"]["amount"]} {data["operationAmount"]["currency"]["name"]}\n'
            )
    return new_data


def print_data_list(data: list, count: int = None) -> None:
    """Выводим переданное количество данных на экран."""

    if not count:
        count: int = len(data)
    print("\n".join(data[:count]))


def main():
    jdata = get_data()
    data = [i for i in jdata if i]
    new_data = sorted(
        data,
        key=lambda item: datetime.datetime.strptime(
            item["date"], "%Y-%m-%dT%H:%M:%S.%f"
        ),
        reverse=True,
    )
    executed_data = get_executed_data(new_data)
    print_data_list(data=executed_data, count=5)


if __name__ == "__main__":
    main()
