#!/usr/bin/env python
# coding=utf8

"""
====================================
 :mod: Test case for Config Module
====================================
.. module author:: 임덕규 <hong18s@gmail.com>
.. note:: MIT License
"""

import unittest
import os

from genson import SchemaBuilder
import json
import yaml

from pyschemaconf.config import Config
from jsonschema.exceptions import ValidationError

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

TEST_CONFIG_FILE_JSON = "test_config.json"
TEST_CONFIG_FILE_YAML = "test_config.yaml"
TEST_SCHEMA_FILE_JSON = "test_schema.json"
TEST_SCHEMA_FILE_YAML = "test_schema.yaml"

TEST_CONFIG = {
    "name": "홍길동",
    "cellphone": "010-1345-7764",
    "address": "이상국 행복리 234",
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

# test_config.json 생성
with open(TEST_CONFIG_FILE_JSON, 'w') as f:
    f.write(json.dumps(TEST_CONFIG, indent=4, ensure_ascii=False))

# test_config.yaml 생성
with open(TEST_CONFIG_FILE_YAML, 'w') as f:
    f.write(yaml.dump(TEST_CONFIG, indent=4, allow_unicode=True))

# test_schema 생성
sc = SchemaBuilder()
sc.add_object(TEST_CONFIG)
TEST_SCHEMA = json.loads(sc.to_json(indent=4))

# test_schema.json 생성
with open(TEST_SCHEMA_FILE_JSON, 'w') as f:
    f.write(json.dumps(TEST_SCHEMA, indent=4))

# test_schema.yaml 생성
with open(TEST_SCHEMA_FILE_YAML, 'w') as f:
    f.write(yaml.dump(TEST_SCHEMA, indent=4))


TEST_WRONG_CONFIG = {
	"name" : 123,
	"cellphone": "010-1345-7764",
	"address": "이상국 행복리 234",
	"age": "33",
    "test_1": [1, 2, 3],
    "test_2": {
        "test3": {
            "test4": 1,
            "test5": 2
        },
        "test6": 2222
    }
}



################################################################################
class TestUnit (unittest.TestCase):
    # ==========================================================================
    def setUp(self):
        self.config = Config()

    # ==========================================================================
    def tearDown(self):
        pass

    # ==========================================================================
    def test_load_yaml_shcema_file(self):
        """
        준비된 Yaml 파일을 읽어서 Json으로 변경하여 확인
        :return:
        """
        self.config._load_yaml_schema_file(
            os.path.join(__location__, 'test_schema.yaml'))
        self.assertEqual(self.config.schema, TEST_SCHEMA)

    # ==========================================================================
    def test_load_json_schema_file(self):
        """
        준비된 Json 파일을 읽어 올 수 있어야 한다.
        :return:
        """
        self.config._load_json_schema_file(
            os.path.join(__location__, 'test_schema.json'))
        self.assertEqual(self.config.schema, TEST_SCHEMA)

    # ==========================================================================
    def test_load_dict_schema(self):
        """
        Dict 형태의 Schema
        :return:
        """
        self.config._load_dict_schema(TEST_SCHEMA)
        self.assertEqual(self.config.schema, TEST_SCHEMA)

    # ==========================================================================
    def test_load_yaml_config_file(self):
        """
        yaml 파일의 설정을 불러올 수 있어야 한다.
        :return:
        """
        self.config._load_yaml_config_file(
            os.path.join(__location__, 'test_config.yaml'))
        self.assertEqual(self.config, TEST_CONFIG)

    # ==========================================================================
    def test_load_json_config_file(self):
        """
        json 파일의 설정을 불러올 수 있어야 한다.
        :return:
        """
        self.config._load_json_config_file(
            os.path.join(__location__, 'test_config.json'))
        self.assertEqual(self.config, TEST_CONFIG)

    # ==========================================================================
    def test_load_dict_config(self):
        """
        dict 형태의 설정을 불러올 수 있다.
        :return:
        """
        self.config._load_dict_config(TEST_CONFIG)
        self.assertEqual(self.config, TEST_CONFIG)

    # ==========================================================================
    def test_load_wrong_config(self):
        """
        스키마 내용과 다른 설정파일을 불러올 때 예외발생
        :return:
        """
        self.config._load_dict_schema(TEST_SCHEMA)
        self.assertRaises(
            ValidationError,
            lambda: self.config._load_dict_config(TEST_WRONG_CONFIG))

    # ==========================================================================
    def test_load_config(self):
        """
        스키마를 이용하여 프로퍼티를 만들고 설정정보를 불러온다
        :return:
        """
        self.config.load(TEST_CONFIG, schema=TEST_SCHEMA)
        self.assertEqual(self.config.name, TEST_CONFIG['name'])
        self.assertEqual(self.config.test_1, TEST_CONFIG['test_1'])
        self.assertEqual(
            self.config.test_2_test3_test4,
            TEST_CONFIG['test_2']['test3']['test4'])

    # ==========================================================================
    def test_load_properties_with_reference_to_schema(self):
        """
        스키마를 참고하여 프로퍼티를 생성
        :return:
        """
        self.config._load_dict_schema(TEST_SCHEMA)
        d = self.config._load_properties_with_reference_to_schema(
            self.config.schema)
        self.config.update(d)

        self.assertEqual(
            list(self.config._load_properties_with_reference_to_schema(
                self.config.schema)),
            list(TEST_SCHEMA['properties'].keys()))

    # ==========================================================================
    def test_set_get_the_property_value(self):
        """
        프로퍼티에서 값을 읽을 수 있어야 한다.
        :return:
        """
        self.config._load_dict_schema(TEST_SCHEMA)
        self.config._load_properties_with_reference_to_schema(
            self.config.schema)

        self.config.name = TEST_CONFIG['name']
        self.config.age = TEST_CONFIG['age']
        self.config.address = TEST_CONFIG['address']
        self.config.cellphone = TEST_CONFIG['cellphone']

        self.config.test_1 = TEST_CONFIG['test_1']
        self.config.test_2_test3_test4 = TEST_CONFIG['test_2']['test3']['test4']
        self.config.test_2_test3_test5 = TEST_CONFIG['test_2']['test3']['test5']
        self.config.test_2_test6 = TEST_CONFIG['test_2']['test6']

        self.assertEqual(self.config.name, TEST_CONFIG['name'])
        self.assertEqual(self.config.age, TEST_CONFIG['age'])
        self.assertEqual(self.config.address, TEST_CONFIG['address'])
        self.assertEqual(self.config.cellphone, TEST_CONFIG['cellphone'])

        self.assertEqual(self.config.test_1, TEST_CONFIG['test_1'])
        self.assertEqual(self.config.test_2_test3_test4,
                         TEST_CONFIG['test_2']['test3']['test4'])
        self.assertEqual(self.config.test_2_test3_test5,
                         TEST_CONFIG['test_2']['test3']['test5'])
        self.assertEqual(self.config.test_2_test6,
                         TEST_CONFIG['test_2']['test6'])

    # ==========================================================================
    def test_setter_exception(self):
        """
        잘못된 값이 프로퍼티에 들어왔을 때 예외를 일으킨다.
        :return:
        """
        self.config._load_dict_schema(TEST_SCHEMA)
        self.config._load_properties_with_reference_to_schema(
            self.config.schema)

        self.assertRaises(
            ValidationError, lambda: setattr(self.config, "name", 1234))
        self.assertRaises(
            ValidationError, lambda: setattr(self.config, "age", "1234"))
        self.assertRaises(
            ValidationError, lambda: setattr(self.config, "test_1", "1234"))
        self.assertRaises(
            ValidationError,
            lambda: setattr(self.config, "test_2_test3_test4", "1234"))
        self.assertRaises(
            AttributeError, lambda: getattr(self.config, "test_2_test3"))

    # ==========================================================================
    def test_save_conf_file(self):
        """
        저장된 설정 정보를 파일로 저장
        기본 저장형태는 Json
        :return:
        """
        self.config.load(
            os.path.join(__location__, TEST_CONFIG_FILE_JSON),
            os.path.join(__location__, TEST_SCHEMA_FILE_JSON))

        TEST_VALUE_1 = 'John Doe'
        TEST_VALUE_2 = 11

        self.config.name = TEST_VALUE_1
        self.config.age = TEST_VALUE_2
        self.config.save()

        # 불러들인 설정 정보 파일을 올바르게 가지고 있는지 검증
        config = Config(TEST_CONFIG_FILE_JSON, TEST_SCHEMA_FILE_JSON)
        self.assertEqual(config.name, TEST_VALUE_1)
        self.assertEqual(config.age, TEST_VALUE_2)
