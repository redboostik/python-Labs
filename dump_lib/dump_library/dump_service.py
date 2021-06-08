from dump_library.parsers.Parser import parser
from dump_library.parsers.Json.json import json
from dump_library.parsers.YAML.yaml import YAML
from dump_library.parsers.TOML.toml import TOML
from dump_library.dump_settings import *

main_parser = parser()


def get_format(format_parser: str):
    if format_parser == 'json':
        return json()
    elif format_parser == 'yaml':
        return YAML()
    elif format_parser == 'toml':
        return TOML()
    else:
        raise ValueError('Unknown parser. You may have entered the wrong name for the parser')


def dump(obj, format_parser: str, file_path: str):
    f = open(file_path, 'w')
    f.write(get_format(format_parser).serialization(main_parser.dump(obj).data, PARSER_DATA_NAME))


def dumps(obj, format_parser: str):
    return get_format(format_parser).serialization(main_parser.dump(obj).data, PARSER_DATA_NAME)


def load(file_path: str, format_parser:str):
    main_parser.data = get_format(format_parser).deserialization(open(file_path, 'r').read())
    return main_parser.load()
    pass


def loads(string: str, format_parser: str):
    main_parser.data = (get_format(format_parser).deserialization(string))
    return main_parser.load()

