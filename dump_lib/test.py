from dump_library.parsers.Parser import parser
from dump_library.parsers.Json.json import json
from dump_library.parsers.YAML.yaml import YAML
from dump_library.parsers.TOML.toml import TOML
from dump_library.dump_service import load, loads, dump, dumps
import inspect
class InnerClass(object):
    qwe = "qwe"


class ParentClass(object):
    def __init__(self):
        self.vint = 123

    v_qwe = InnerClass()
    v_int = 1
    v_float = 1.23
    v_bool = True
    v_tuple = (1, 2, 3)
    v_dict = {'1': 1, '2': 2, '3': 3, '4': 4}
    v_list = [1, [1, 'fsdsd', True], 3, 4, InnerClass]


class ChildClass(ParentClass):

    vstr = "1234567890"
    vint = 1
    def insert_in_method(self, k: int, f):
        self.insert_in_function(k + self.vint, f)

    def insert_in_function(self, k: int, f):
        return f(k + function(1))


def function(a: int):
    return a ** a

test_dict = {
    'v_int': 1,
    'v_float': 1.23,
    'v_bool': True,
    'v_tuple': (1, 2, 3),
    'v_dict': {'1': 1, '2': 2, '3': 3, '4': 4},
    'v_list': [1, [1, 'fsdsd', True], 3, 4]
}

b = parser()
par = json()
t2 = ChildClass()
dub = b.dump(t2)
aa = t2.insert_in_function.__code__
gl = globals()
s = par.serialization(dub.data, 'Parser_Data')
ss = par.deserialization(s)
k = dub.dump(ss).load()
# dump(t2,'json', 'txt.json')
pass
