# PySchemaConf
Configuration File Handle Module for Python. It supports varieties of data type such as JSON, YAML, PYTHON DICT.

```python
>>> from pyschemaconf import Config
>>> conf = Config(config_file, schema_file)
>>> conf.name
John Doe
>>> conf.name = "Jack"
>>> conf.name
Jack
>>> conf.test_2_test3_test4
1
>>> conf.save() 
``` 
# Installation
```shell
pip install pyschemaconf
```

# Usage
## Import module
```python
from pyschemaconf import Config
```

## Load Schema and Config File wrote in JSON or YAML

```python
conf = Config(config, schema)
```
or
```python
conf = Config()
conf.load(config, schema)
```

## Reading values

```python
CONFIG = {
    "name": "John Doe",
    "cellphone": "010-1345-7764",
    "address": "Pitt st. 33",
    "age": 33,
    "test_1": [1, 2, 3],
    "test_2": {
        "test3": {
            "test4": 1,
            "test5": 2
        },
        "test6": "Hello World"
    }
}

>>> conf.name
John Doe
>>> conf.test_1
[1, 2, 3]
>>> conf.test_2_test3_test4
1
>>> conf.test_2_test6
Hello World
```

### Writing values
__It must load the schema for the config before writing values__

```python
>>> conf.name = "Snake"
>>> conf.age = 34
```

if you tried to write the value different to schema, it raises **Validation Error**.

```python
>>> conf.name = 1
Traceback (most recent call last):
  File "/Applications/PyCharm.app/Contents/helpers/pydev/_pydevd_bundle/pydevd_exec2.py", line 3, in Exec
    exec(exp, global_vars, local_vars)
  File "<input>", line 1, in <module>
  File "<string>", line 6, in name_setter
  File "/Users/limdeokyu/pyschemaconf/venv/lib/python3.6/site-packages/jsonschema/validators.py", line 541, in validate
    cls(schema, *args, **kwargs).validate(instance)
  File "/Users/limdeokyu/pyschemaconf/venv/lib/python3.6/site-packages/jsonschema/validators.py", line 130, in validate
    raise error
jsonschema.exceptions.ValidationError: 1 is not of type 'string'
Failed validating 'type' in schema:
    {'type': 'string'}
On instance:
    1
```