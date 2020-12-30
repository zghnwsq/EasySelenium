import yaml


def read_yaml(file_path, encoding='utf-8'):
    with open(file_path, encoding=encoding) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        return data


def write_yaml(file_path, data, mode='w', encoding='utf-8'):
    with open(file_path, mode=mode, encoding=encoding) as file:
        yaml.dump(data, file, encoding=encoding, allow_unicode=True)














