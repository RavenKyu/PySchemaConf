import json
import yaml
import jsonschema

PROPERTY_FORM = """self{addr} = dict()
def {name}_getter(self):
    return self{addr}

def {name}_setter(self, value):
    jsonschema.validate(value, self.schema['properties']{schema})
    self{addr} = value

Config.{name} = property({name}_getter, {name}_setter)
"""


################################################################################
class Config(dict):
    # ==========================================================================
    def __init__(self, config=None, schema=None):
        dict.__init__(self)
        self._schema = dict()
        self._filename = ""
        if config:
            self.load(config, schema)

    # ==========================================================================
    # 설정 정보의 값의 Validation 정보
    @property
    def schema(self) -> dict:
        return self._schema
    @schema.setter
    def schema(self, schema: dict):
        if not isinstance(schema, dict):
            raise TypeError("not dict")
        self._schema = schema

    # ==========================================================================
    def _make_schema(self, filename):
        self.load(filename)
        from genson import SchemaBuilder
        sc = SchemaBuilder()
        sc.add_object(self)
        # filename = filename[:filename.rfind('.')]
        return sc.to_json(indent=4) + '\n'

    # ==========================================================================
    def validate_config(self, config: dict):
        # todo: 스키마 파일 없을 경우 동작 추가
        jsonschema.validate(config, self.schema)

    # ==========================================================================
    def _load_dict_schema(self, schema):
        self.schema = schema

    # ==========================================================================
    def _load_json_schema_file(self, filename):
        with open(filename, 'r') as f:
            self.schema = json.load(f)

    # ==========================================================================
    def _load_yaml_schema_file(self, filename):
        with open(filename, 'r') as f:
            self.schema = yaml.load(f)

    # ==========================================================================
    def _load_schema(self, schema):
        if isinstance(schema, dict):
            self._load_dict_schema(schema)
            return
        ext = schema[schema.rfind('.') + 1:]
        if ext in ('json',):
            self._load_json_schema_file(schema)
        elif ext in ('yaml', 'yml',):
            self._load_yaml_schema_file(schema)
        else:
            raise ValueError("Not Supported Schema File")

    # ==========================================================================
    def load(self, data, schema=None):
        if schema:
            self._load_schema(schema)
            self._load_properties_with_reference_to_schema(self.schema)

        if isinstance(data, dict):
            self._load_dict_config(data)
            return

        self._filename = data
        ext = data[data.rfind('.') + 1:]
        if ext in ('json',):
            self._load_json_config_file(data)
        elif ext in ('yaml', 'yml',):
            self._load_yaml_config_file(data)
        else:
            raise ValueError("Not Supported Config File")

    # ==========================================================================
    def _load_dict_config(self, config):
        self.validate_config(config)
        self.update(config)

    # ==========================================================================
    def _load_json_config_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.validate_config(data)
        self.update(data)

    # ==========================================================================
    def _load_yaml_config_file(self, filename):
        with open(filename, 'r') as f:
            data = yaml.load(f)
        self.validate_config(data)
        self.update(data)

    # ==========================================================================
    def _load_properties_with_reference_to_schema(self, schema, depth=list()):
        # todo: 리팩토링 필요
        d = dict()

        # 더 이상의 깊이가 없는 말단 데이터
        # 말단 데이터만 프로퍼티 생성
        if 'properties' not in schema:
            n = list()
            for name in depth:
                n.append("['" + name + "']")
            exec(PROPERTY_FORM.format(**{
                'addr': ''.join(n),
                'schema': "['properties']".join(n),
                'name': '_'.join(depth)}))

            if depth:
                depth.pop()
            return {'str': '', 'int': 0, 'float': 0.0, 'list': []}[
                self._change_type_for_python(schema['type'])]

        # 하위 설정이 있을 경우
        for prop in schema['properties']:
            depth.append(prop)

            n = list()
            for name in depth:
                n.append("['" + name + "']")
            exec("self{addr} = dict()".format(**{
                'addr': ''.join(n)}))

            # 하위 설정으로 진입
            d[prop] = self._load_properties_with_reference_to_schema(
                schema['properties'][prop], depth)
            if depth:
                depth.pop()
        return d

    # ==========================================================================
    def _change_type_for_python(self, name):
        if name in ('string',):
            return 'str'
        elif name in ('number', 'integer'):
            return 'float'
        elif name in ('object',):
            return 'dict'
        elif name in ('array',):
            return 'list'
        elif name in ('boolean',):
            return 'bool'
        else:
            return 'None'

    # ==========================================================================
    def save(self):
        if not self._filename:
            raise Exception
        save = {
            "json": self._save_as_json,
            "yaml": self._save_as_yaml,
            "yml": self._save_as_yaml,}
        ext = self._filename[self._filename.rfind('.') + 1:]
        save[ext](self, self._filename)

    # ==========================================================================
    def _save_as_json(self, data: dict, filename: str):
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

    # ==========================================================================
    def _save_as_yaml(self, data: dict, filename: str):
        with open(filename, 'w') as f:
            f.write(yaml.dump(data, indent=4, allow_unicode=True))
