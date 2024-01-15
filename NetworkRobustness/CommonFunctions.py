import json
import os
from datetime import datetime


def read_tuple_data(connections_string):
    connections_string = connections_string.replace('\n', '')
    connections = connections_string.split(' ')
    return int(connections[0]), int(connections[1])


def check_if_file_is_empty(file_path):
    return os.stat(file_path).st_size == 0


def check_if_file_exists(file_path):
    return os.path.exists(file_path)


def check_if_file_has_data(file_path, sub_dir=''):
    path = os.path.join(sub_dir, file_path) if sub_dir else file_path
    if check_if_file_exists(path):
        if check_if_file_is_empty(path) is False:
            return True
        else:
            raise FileNotFoundError
    else:
        return False


def make_directories(list_of_dirs):
    for directory in list_of_dirs:
        if not check_if_file_exists(directory):
            os.mkdir(directory)


def save_json_file(dict_with_data, json_file_name, sub_dir=''):
    path = os.path.join(sub_dir, json_file_name) if sub_dir else json_file_name
    json_file = open(path, 'w')
    json.dump(dict_with_data, json_file)
    json_file.close()
    print(f'Created new file {json_file_name} with simulation data.')


def read_json_file(json_file_name, sub_dir=''):
    path = os.path.join(sub_dir, json_file_name) if sub_dir else json_file_name
    print(f'Reading data from file {json_file_name}...')
    json_file = open(path, 'r')
    dict_with_data = json_file.read()
    dict_with_data = json.loads(dict_with_data)
    json_file.close()
    return dict_with_data


def print_and_store(variable, message=None, disable_print=False, end='\n'):
    if message is None:
        message = f'Program executed on {datetime.now()}.'
        variable += message + end
    else:
        variable += message + end
    if not disable_print:
        print(message, end=end)
    return variable