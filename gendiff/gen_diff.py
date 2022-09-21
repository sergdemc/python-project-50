from collections import OrderedDict
from gendiff.views import RENDERS
from gendiff.parse_files import get_dict, normalize_values


def get_diff(old: dict, new: dict) -> dict:
    res = {}
    old_keys = set(old.keys()) - set(new.keys())
    for key in old_keys:
        res[key] = {'flag': 'removed', 'value': old[key]}

    new_keys = set(new.keys()) - set(old.keys())
    for key in new_keys:
        res[key] = {'flag': 'added', 'value': new[key]}

    return res


def get_final_diff(old: dict, new: dict) -> OrderedDict:
    res = get_diff(old, new)

    for key in old.keys() & new.keys():
        old_val = old[key]
        new_val = new[key]
        if isinstance(old[key], dict) and isinstance(new[key], dict):
            res[key] = \
                {'flag': 'nested', 'value': get_final_diff(old_val, new_val)}
        elif old_val == new_val:
            res[key] = \
                {'flag': 'unchanged', 'value': old_val}
        elif old_val != new_val:
            res[key] = \
                {'flag': 'changed', 'old_value': old_val, 'new_value': new_val}
    return OrderedDict(sorted(res.items()))


def generate_diff(path1: str, path2: str, format_name='stylish') -> str:
    file1 = normalize_values(get_dict(path1))
    file2 = normalize_values(get_dict(path2))
    diff = get_final_diff(file1, file2)
    return RENDERS[format_name].view_diff(diff)