class Response:
    def __init__(self, data):
        self._data = data
        self.route = data["route"]
        for key, value in data["data"].items():
            setattr(self, key, value)

    def to_dict(self):
        return self._data

    def __repr__(self):
        return f"<Response from {self.route}>"

    def __len__(self):
        return len(self._data)


class AnyType:
    """Some Compile format string"""

    pass


class CompileOutput:
    def __init__(
        self, source: str, error=False, error_type=None, error_msg=None, result=None
    ):
        self.source = source
        self.result = None
        self.error_msg = None
        self.error = error
        if not error:
            self.result = result
        else:
            self.error_msg = error_msg
            self.error_type = error_type


class DictObject:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
