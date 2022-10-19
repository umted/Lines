"""Файл реализующий действия с игрой"""
import json
from collections import OrderedDict


def add_record(player_name, score):
    """Добавление новой записи в таблицу записей"""
    try:
        file = open('records.json', 'r', encoding='utf-8')
        records = json.load(file)
        file.close()
        if records.get(player_name) is None or records.get(player_name) < score:
            records.update({player_name: score})
            sorted_records = OrderedDict(sorted(records.items(), key=lambda y: y[1], reverse=True))
            records.clear()
            records.update(sorted_records)
            file = open('records.json', 'w', encoding='utf-8')
            json.dump(records, file, indent=4)
            file.close()
        if len(records) > 8:
            sorted_records = OrderedDict(sorted(records.items(), key=lambda y: y[1], reverse=True))
            sorted_records.popitem()
            records.clear()
            records.update(sorted_records)
    except FileNotFoundError:
        file = open('records.json', 'w', encoding='utf-8')
        records = {}
        records.update({player_name: score})
        json.dump(records, file, indent=4)
        file.close()
    except Exception as exception:
        raise AddRecordError(exception)


def get_records():
    """Получение записи из файла"""
    try:
        with open('records.json', 'r', encoding='utf-8') as file:
            records = json.load(file)
            return records
    except Exception as exception:
        raise GetRecordsError(exception)


class AddRecordError(Exception):
    """Не может добавить запись ошибка"""
    pass


class GetRecordsError(Exception):
    """Не может получить запись ошибка"""
    pass


class LoadError(Exception):
    """Загрузка игры из файла исключения"""
    pass
