from django.utils.encoding import force_text
from rest_framework.exceptions import ValidationError

def _force_text_recursive(data):
    """
    Descend into a nested data structure, forcing any
    lazy translation strings into plain text.
    Or, forcely converts any value into plain text of list and dict.
    """
    if isinstance(data, list):
        res = [
            _force_text_recursive(item) for item in data
        ]
        print(res)
        return res
    elif isinstance(data, dict):
        res = dict([
            (key, _force_text_recursive(value))
            for key, value in data.items()
        ])
        print(res, 'in dict')
        return res
    return force_text(data)

class HttpValidationError(ValueError):
    "For validation errors the 'detail' key is always required."
    def __init__(self, detail):
        if isinstance(detail, (dict, list)):
            # check if detail is dict or list object.
            # works for both dict & list item.
            self.detail = _force_text_recursive(detail)
        else:
            self.detail = force_text(detail)