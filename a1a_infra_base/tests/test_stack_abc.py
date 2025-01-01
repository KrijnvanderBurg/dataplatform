import unittest
from typing import Any
from unittest.mock import MagicMock

from constructs import Construct

from a1a_infra_base.stacks.stack_abc import StackABC, StackConfigABC


class MockStackConfig(StackConfigABC):
    def __init__(self) -> None:
        self.config = None

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> "MockStackConfig":
        instance = cls()
        instance.config = dict_
        return instance


class MockStack(StackABC):
    def __init__(self, scope: Construct, id_: str, *, env: str, config: StackConfigABC) -> None:
        self.scope = scope
        self.id_ = id_
        self.env = env
        self.config = config


class TestStackConfigABC(unittest.TestCase):
    def test_from_dict(self) -> None:
        config_dict = {"key": "value"}
        config = MockStackConfig.from_dict(config_dict)
        self.assertEqual(config.config, config_dict)


class TestStackABC(unittest.TestCase):
    def test_initialization(self) -> None:
        scope = MagicMock(spec=Construct)
        id_ = "test_id"
        env = "test_env"
        config = MockStackConfig.from_dict({"key": "value"})
        stack = MockStack(scope, id_, env=env, config=config)
        self.assertEqual(stack.scope, scope)
        self.assertEqual(stack.id_, id_)
        self.assertEqual(stack.env, env)
        self.assertEqual(stack.config, config)
