import inspect
from behave import *

import tkinter as tk
from conscience.lobes.lobe import Lobe


class CodeDesign(Lobe):
    """Lobe which adds functionality to check that certain classes and functions are defined."""

    def on_load(self, suite):
        load_design_tests()


def load_design_tests():
    @given("the {clazz:w} class is defined")
    def class_defined(context, clazz):
        assert hasattr(context.under_test, clazz), f"{clazz} not defined"
        assert isinstance(
            getattr(context.under_test, clazz), type
        ), f"{clazz} is not a class"

    @given("the {func:w} function is defined")
    def function_defined(context, func):
        assert hasattr(context.under_test, func), f"{func} not defined"
        assert callable(getattr(context.under_test, func)), f"{func} is not callable"

    @given("{func:w} function takes {args:d} positional parameters")
    def function_takes_args(context, func, args):
        assert hasattr(context.under_test, func), f"{func} not defined"
        func_obj = getattr(context.under_test, func)

        parameters = inspect.signature(func_obj).parameters
        positional_parameters = [
            param
            for param in parameters
            if parameters[param].kind != inspect.Parameter.VAR_KEYWORD
        ]
        num_args = len(positional_parameters)
        assert (
            num_args == args
        ), f"{func} does not have {args} positional parameters, it has {num_args} ({positional_parameters})"

    @given("{subclazz:w} class inherits from {clazz:w}")
    def subclazz_inherits_from_clazz(context, subclazz, clazz):
        assert hasattr(context.under_test, clazz), f"{clazz} not defined"
        assert hasattr(context.under_test, subclazz), f"{subclazz} not defined"
        assert issubclass(
            getattr(context.under_test, subclazz), getattr(context.under_test, clazz)
        ), f"{subclazz} does not inherit from {clazz}"

    @given("{subclazz:w} class inherits from tk.{clazz:w}")
    def subclazz_inherits_from_tk_clazz(context, subclazz, clazz):
        assert hasattr(context.under_test, subclazz), f"{subclazz} not defined"
        assert issubclass(
            getattr(context.under_test, subclazz), getattr(tk, clazz)
        ), f"{subclazz} does not inherit from {clazz}"

    @given("{clazz:w}.{method:w} with {params:d} positional parameters is defined")
    def method_defined(context, clazz, method, params):
        assert hasattr(context.under_test, clazz), f"{clazz} not defined"

        clazz_obj = getattr(context.under_test, clazz)
        assert hasattr(clazz_obj, method), f"{clazz}.{method} not defined"

        method_obj = getattr(clazz_obj, method)
        assert callable(method_obj), f"{clazz}.{method} is not callable"

        parameters = inspect.signature(method_obj).parameters
        positional_parameters = [
            param
            for param in parameters
            if parameters[param].kind != inspect.Parameter.VAR_KEYWORD
        ]
        num_args = len(positional_parameters)
        assert (
            num_args == params
        ), f"{clazz}.{method} does not have {params} positional parameters, it has {num_args} ({positional_parameters})"

    @given(
        "{clazz:w}.{method:w} with {params:d} positional parameters and {kwargs:d} keyword parameters is defined"
    )
    def method_defined_kw(context, clazz, method, params, kwargs):
        method_defined(context, clazz, method, params)

        clazz_obj = getattr(context.under_test, clazz)
        method_obj = getattr(clazz_obj, method)

        parameters = inspect.signature(method_obj).parameters
        keyword_parameters = [
            param
            for param in parameters
            if parameters[param].kind == inspect.Parameter.VAR_KEYWORD
        ]
        num_kwargs = len(keyword_parameters)

        assert (
            num_kwargs == kwargs
        ), f"{clazz}.{method} does not have {kwargs} keyword parameters, it has {num_kwargs} ({keyword_parameters})"
