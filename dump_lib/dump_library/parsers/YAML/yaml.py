import yaml

class YAML():
    def dump_complex(self, o):
        ans = ""
        ans = yaml.dump(o)
        return ans

    def dump_obj(self, o):
        string = ""
        tp = type(o)
        if tp == bool:
            if o:
                string += "True"
            else:
                string += "False"
        elif o is None:
            string += "None"
        elif tp == int or tp == float:
            string += str(o)
        elif tp != str:
            string += self.dump_complex(o)
        else:
            string += str(o)

        return string

    def serialization(self, obj, name:str):
        s = self.dump_complex({name: obj})
        return s

    def deserialization(self, s):
        return yaml.load(s, Loader=yaml.FullLoader)
