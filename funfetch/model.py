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
