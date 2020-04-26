"""Text and error codes"""
from typing import Dict

ERROR: Dict[str, str] = {
    "MC100": "MC100: Invalid file name. Pattern: 'test_{method}_{endpoint}_{other}.py'",
    "MC101": "MC101: Class does not match the file name",
    "MC102": "MC102: Invalid test function docstring. (id, url, title)",
    "MC103": "MC103: No 'pytestrail.case' decorator or 'pytestrail.params' or invalid value case id",
    "MC104": "MC104: Different cases id. Decorator: '{}', Comment: '{}'",
    "MC105": "MC105: Invalid comment case id. '{}'",
    "MC106": "MC106: Invalid decorator case id. '{}'",
    "MC107": "MC107: Invalid comment url: '{}'",
    "MC108": "MC108: Class method invalid params. Expected only 'cls'",
    "MC109": "MC109: No decorator '@classmethod'",
    "MC110": "MC110: Invalid test function/method name",
    "MC111": "MC111: Supporting function. No callback annotation",
    "MC112": "MC112: Supporting function. No docstring",
    "MC113": "MC113: Bad test function/method name",
    "MC114": "MC114: Supporting function. Bad name",
    "MC120": "MC120: Bad variable name",
    "MC121": "MC121: Bad variable name. Do not use digit",
    "MC122": "MC122: Excess decorator '@classmethod'"
}
