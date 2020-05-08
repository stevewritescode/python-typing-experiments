#!/usr/bin/env python3

# Experiments in error handling

from typing import Union, NoReturn
from dataclasses import dataclass

# Method 1: Idomatic Python


def do_work1(success: bool) -> int:
    if success:
        return 1
    raise RuntimeError("A bad thing happened")


try:
    do_work1(True)
    print("It passed")
    do_work1(False)
except RuntimeError as e:
    print(f"One of them failed: {e}")


# Method 2: Return a Union Type


def do_work2(success: bool) -> Union[int, Exception]:
    if success:
        return 1
    else:
        return RuntimeError("A bad thing happened")


def handle_result(result: Union[int, Exception]) -> None:
    if isinstance(result, Exception):
        print(f"It failed: {result}")
        return

    # mypy tracks the isinstance() call and return statement above,
    # automatically refining the type for "result" to int
    total = 1 + result
    print(f"It passed: Total is {total}")


handle_result(do_work2(False))
handle_result(do_work2(True))


# Experiment: Statically verify exhaustive type matching / type refinement


@dataclass
class EndpointPE:
    name: str = "EndpointPE"


@dataclass
class EndpointMacro:
    name: str = "EndpointMacro"


@dataclass
class EndpointMacho:
    name: str = "EndpointMacho"


ModelType = Union[EndpointPE, EndpointMacro]


def assert_unreachable(x: NoReturn) -> NoReturn:
    # This function signals to mypy that the code should be unreachable
    assert False


def match_model(model: ModelType) -> str:
    if isinstance(model, EndpointPE):
        return "I'm PE"
    if isinstance(model, EndpointMacro):
        return "I'm Macro"

    assert_unreachable(model)


print(match_model(EndpointPE()))
print(match_model(EndpointMacro()))
