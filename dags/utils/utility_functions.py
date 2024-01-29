import re
from functools import wraps
from typing import Union, Callable, Literal


class TextFormatter:
    """
    This class allows to custom format text.

    This module is created due to the needs of text formatting in various modules of the framework. And it is designed
    to be extensible and flexible so that it can be adapted to multiple use cases.

    E.g:

    1. Initialize the text formatter, with the desired rules:
        text_formatter = TextFormatter(strip_text=True, remove_double_spaces=True, encode_utf8=True)

    2. Enjoy applying format to anything; The formatter can be applied over:
        - Lists.
        - Dictionaries (only applies over dictionary values).
        - Strings, of course!

    Notes:
        - The formatter will be recursively applied to the elements of the passed object,
          so **be careful** when using it!
        - The formatter can receive a function in order to be used as decorator, as shown::

            @text_formatter.format
            def fn()
                return ["some unForMaTatted    string", "ONE string MORE"]
    """

    def __init__(
            self,
            strip_text: bool = False,
            remove_double_spaces: bool = False,
            case_type: Literal["lowercase", "uppercase", "title_case"] = None,
    ):
        self._transformation_stages = set()

        if strip_text:
            self._transformation_stages.add(self._strip_text)

        if remove_double_spaces:
            self._transformation_stages.add(self._remove_double_spaces)

        if case_type == "title_case":
            self._transformation_stages.add(self._convert_to_title)

        if case_type == "lowercase":
            self._transformation_stages.add(self._convert_to_title)

        if case_type == "uppercase":
            self._transformation_stages.add(self._convert_to_title)

    def format_object(self, _object: Union[str, list, dict, Callable]):
        if isinstance(_object, str):
            return self._format_str(_object)

        if isinstance(_object, list):
            return [self.format_object(element) for element in _object]

        if isinstance(_object, dict):
            return {key: self.format_object(value) for key, value in _object.items()}

        if callable(_object):
            @wraps(_object)
            def wrapper(*args, **kwargs):
                text = _object(*args, **kwargs)
                return self.format_object(text)

            return wrapper

        return _object

    def _format_str(self, text: str) -> str:
        """
        Format a string, according to the transformation stages defined.
        """
        for transformation_stage in self._transformation_stages:
            text = transformation_stage(text)
        return text

    @staticmethod
    def _strip_text(text: str) -> str:
        return text.strip()

    @staticmethod
    def _remove_double_spaces(text: str) -> str:
        return re.sub(r" +", " ", text)

    @staticmethod
    def _convert_to_title(text: str) -> str:
        return text.title().replace("'S", "'s")

    @staticmethod
    def _convert_to_lower(text):
        return text.lower()

    @staticmethod
    def _convert_to_upper(text):
        return text.upper()
