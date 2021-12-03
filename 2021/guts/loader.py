class Loader:
    _data = None

    def __init__(self, path):
        self._path = path

    def _load(self):
        if self._data is None:
            self._data = [l for l in self.read()]
            return self._data

    def read(self):
        with open(self._path, 'r') as f:
            for line in f:
                yield line.strip()

    @property
    def data(self):
        return self._load()
