from dump_library.dump_service import *

test_dict = {
    'v_int': 1,
    'v_float': 1.23,
    'v_bool': True,
    'v_dict': {'1': 1, '2': 2, '3': 3, '4': 4},
    'v_list': [1, [1, 'fsdsd', True], 3, 4]
}


class InnerClass(object):
    qwe = "qwe"

    def equal(self, obj):
        return self.qwe == obj.qwe


class ParentClass(object):
    def __init__(self):
        self.vint = 123

    v_qwe = InnerClass()
    v_int = 1
    v_float = 1.23
    v_bool = True
    v_dict = {'1': 1, '2': 2, '3': 3, '4': 4}
    v_list = [1, [1, 'fsdsd', True], 3, 4]
    v_class = InnerClass


class ChildClass(ParentClass):

    vstr = "1234567890"

    def insert_in_method(self, k: int, f):
        return self.insert_in_function(k + self.v_int, f)

    def insert_in_function(self, k: int, f):
        return f(k + function(1))

    def equal(self, obj):
        return self.vint == obj.vint and self.v_int == obj.v_int and self.v_qwe.equal(obj.v_qwe) and \
               self.v_bool == obj.v_bool and self.v_dict == obj.v_dict and self.v_float == obj.v_float and \
               self.vstr == obj.vstr and self.v_class().equal(obj.v_class())


def function(a: int):
    return a ** a


def rec(steps: int, add:int):
    if steps <= 0:
        return 0
    return rec(steps - 1, add) + add


def rec_and_func(steps, a: int):
    return rec(steps, function(a))


def test_service_simple_string():
    assert loads(dumps(test_dict, 'json'), 'json') == test_dict
    assert loads(dumps(test_dict, 'yaml'), 'yaml') == test_dict
    assert loads(dumps(test_dict, 'toml'), 'toml') == test_dict


def test_service_simple_file():
    dump(test_dict, 'json', 'test.service')
    assert load('test.service', 'json') == test_dict
    dump(test_dict, 'yaml', 'test.service')
    assert load('test.service', 'yaml') == test_dict
    dump(test_dict, 'toml', 'test.service')
    assert load('test.service', 'toml') == test_dict
    pass


def test_service_classes_file():

    dump(ChildClass(), 'json', 'test.service')
    assert ChildClass().equal(load('test.service', 'json'))

    dump(ChildClass(), 'yaml', 'test.service')
    assert ChildClass().equal(load('test.service', 'yaml'))


def test_service_classes_string():
    assert ChildClass().equal(loads(dumps(ChildClass(), 'json'), 'json'))
    assert ChildClass().equal(loads(dumps(ChildClass(), 'yaml'), 'yaml'))


def test_service_functions_file():
    dump(rec_and_func, 'json', 'test.service')
    assert load('test.service', 'json')(3, 3) == rec_and_func(3, 3)
    dump(rec_and_func, 'yaml', 'test.service')
    assert load('test.service', 'yaml')(3, 3) == rec_and_func(3, 3)


def test_service_functions_string():
    assert loads(dumps(rec_and_func, 'json'), 'json')(3, 3) == rec_and_func(3, 3)
    assert loads(dumps(rec_and_func, 'yaml'), 'yaml')(3, 3) == rec_and_func(3, 3)
