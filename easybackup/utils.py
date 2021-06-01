import configparser


def load_config():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    return config


def listed_to_skip(skip_list, obj):
    skip = False
    for el in skip_list:
        if el in obj:
            skip = True
            break
    return skip
