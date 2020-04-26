"""
flake8 plugin
"""
import os.path
import re
from typing import List, Tuple

import pycodestyle  # noqa

from . import constants
from .err import ERROR

__version__ = '1.1.0'


class CheckerTestFile:
    """Base class"""

    name = 'test_code_style_checker'
    version = __version__

    def __init__(self, tree, filename='(none)', file_tokens=None):
        self.filename = 'stdin' if filename in ('stdin', '-', None) else filename
        self.tree = tree
        self.tokens = file_tokens

    def run(self):
        """Auto Call Validation"""

        formatted_filename = self.filename.replace('\\', '_').replace('/', '_')
        if re.match(r'.*tests_cases.+', formatted_filename):
            sanitized_filename = os.path.splitext(os.path.basename(self.filename))[0]
            if (not re.match(r'^test_(post|get|put|delete|patch|smoke_test)_\w+$', sanitized_filename) and
                    not re.match(r'.*database_tests.+', formatted_filename)):
                if not re.match(r'^__init__$', sanitized_filename):
                    yield 0, 0, ERROR['MC100'], type(self)
            else:
                errors = []

                read_line = list(pycodestyle.readlines(self.filename))
                for line_number, line in enumerate(read_line):
                    if line.strip().startswith(constants.CLASS):  # Check class
                        # Checking the occurrence of the file name in the class name
                        if sanitized_filename.replace('_', '') not in line[len(constants.CLASS) + 1:-1].lower():
                            yield line_number + 1, len(constants.CLASS) + 1, ERROR['MC101'], type(self)

                    if line.strip().startswith(constants.DEF):
                        errors += function_validator(line, line_number, read_line)

                if self.tokens:
                    errors += token_parser(self.tokens)

                for error in errors:
                    yield error[0] + 1, error[1], error[2], type(self)


def function_validator(line: str, num: int, read_line: List[str]) -> List[Tuple[int, int, str]]:
    """
    Function validation
    :param line: Current row
    :param num: Current line number
    :param read_line: List of all lines
    :return: Error list [(num, col, message)]
    """
    errors = []
    start = line.find(constants.DEF)
    col = start + len(constants.DEF) + 1

    if line[start:].startswith(f'{constants.DEF} test_'):
        errors += [(num, col, i) for i in function_test_validator(num, read_line)]

    elif line[start:].startswith(f'{constants.DEF} setup_') or line[start:].startswith(f'{constants.DEF} teardown_'):
        errors += [(num, col, i) for i in function_fixture_validator(line, num, read_line)]

    elif line[start:].startswith(f'{constants.DEF} _'):
        errors += [(num, c or col, i) for c, i in function_support_validator(line, num, read_line)]

    else:
        errors.append((num, col, ERROR['MC110']))

    return errors


def function_test_validator(num: int, read_line: List[str]) -> List[str]:
    """
    Validation of test functions
    :param num: Current line number
    :param read_line: List of all lines
    :return: list of messages [message, message]
    """
    errors = []

    if func_name := re.findall(r'def\s(test_.+)\(', read_line[num]):
        func_name_list = func_name[0].split('_')
        if len(func_name_list) < 3:
            errors.append(ERROR['MC113'])

    # Checking the comment under the function
    function_comment = '\n'.join(read_line[num + 1: num + 7])
    case_id = re.findall(r'id:\s?(.+)', function_comment)
    url = re.findall(r'url:\s?(.+)', function_comment)
    title = re.findall(r'title:\s?(.+)', function_comment)
    if not case_id or not url or not title:
        errors.append(ERROR['MC102'])

    # Case id validity in the comment
    if case_id:
        if not re.match(r'^C\d+$', case_id[0]):
            errors.append(ERROR['MC105'].format(case_id[0]))

    # Checking the decorator @pytestrail.case...
    test_rail_decorator = '\n'.join(read_line[num - 5: num])
    case_id_decorator = re.findall(r'\s*@pytestrail\.case\([\'\"](C\d+)[\'\"]\)', test_rail_decorator)

    # Checking the decorator @pytest.mark.parametrize('value', pytestrail.params...
    case_id_parametrize = re.findall(
        r'\s@pytest\.mark\.parametrize\(\s*[\'\"]\w+[\'\"],\s*pytestrail\.params\(\s*[\'\"](C\d+)[\'\"],',
        test_rail_decorator
    )
    case_id_list = case_id_decorator or case_id_parametrize
    if not case_id_list:
        errors.append(ERROR['MC103'])

    # Case id validator in decorator
    if case_id_list:
        if not re.match(r'^C\d+$', case_id_list[0]):
            errors.append(ERROR['MC106'].format(case_id_list[0]))

    # Checking the id of cases
    if case_id and case_id_list:
        if case_id[0] != case_id_list[0]:
            errors.append(ERROR['MC104'].format(case_id_list[0], case_id[0]))

    if url:
        if not re.match(r'^(GET|POST|DELETE|PUT|PATCH)\s/[^\s]+\s?$', url[0]) and not re.match(
                r'(DataBase test|Smoke Test)', url[0], re.IGNORECASE):
            errors.append(ERROR['MC107'].format(url[0]))

    return errors


def function_fixture_validator(line: str, num: int, read_line: List[str]) -> List[str]:
    """
    Checking basic functions, fixtures
    :param line: Current row
    :param num: Current line number
    :param read_line: List of all lines
    :return: list of messages [message, message]
    """
    errors = []
    pattern = re.compile(r'.*@classmethod.*')

    if re.match(r'.*\s(setup_class|teardown_class)\s?\(cls\).*', line):
        if not pattern.match(read_line[num - 1]):
            errors.append(ERROR['MC109'])

    elif re.match(r'.*\s(setup_method|teardown_method)\(.*', line):
        if pattern.match(read_line[num - 1]):
            errors.append(ERROR['MC122'])
    else:
        errors.append(ERROR['MC110'])
    return errors


def function_support_validator(line: str, num: int, read_line: List[str]) -> List[Tuple[int, str]]:
    """
    Validation of auxiliary functions in the test
    :param line: Current row
    :param num: Current line number
    :param read_line: List of all lines
    :return: list of messages [(col, message)]
    """
    errors = []

    if func_name := re.findall(r'def\s_(.+)\(', read_line[num]):
        func_name_list = func_name[0].split('_')
        if len(func_name_list) < 2:
            errors.append((False, ERROR['MC114']))

    if not re.match(r'.*\)\s?->\s?.*:.*', line):
        errors.append((len(line) - 3, ERROR['MC111']))

    data = ''.join(read_line[num:num + 11]).replace('\n', ' ')
    if not re.match(r'.*""".*""".*', data):
        errors.append((1, ERROR['MC112']))

    return errors


def token_parser(token) -> List[Tuple[int, int, str]]:
    """
    File token parser
    :param token: token
    :return: [(num, col, message)]
    """
    errors = []

    for data in token:
        if data.type == 1 and data.string != '_':
            pattern = r'^{}\s?:?[^.:]*\s=\s.*'.format(data.string)
            if re.match(pattern, data.line.strip()):
                net_variable = data.string.replace('_', '')

                if (len(net_variable) < constants.MIN_LENGTH_VARIABLE and
                        net_variable not in constants.GOOD_VARIABLE_NAME):
                    errors.append((data.start[0] - 1, data.start[1], ERROR['MC120']))

                if data.string in constants.BAD_VARIABLE_NAME or net_variable in constants.BAD_VARIABLE_NAME:
                    errors.append((data.start[0] - 1, data.start[1], ERROR['MC120']))

                if not net_variable.isalpha() and net_variable not in constants.GOOD_VARIABLE_NAME:
                    errors.append((data.start[0] - 1, data.start[1], ERROR['MC121']))
    return errors
