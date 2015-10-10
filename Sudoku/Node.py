class Node():
    def __init__(self, value):
        self._value = value
        self._p = [1,2,3,4,5,6,7,8,9]
        if value is not None:
            self._p.remove(value)
            self._np = [value]
        else:
            self._np = []
            
    def __str__(self):
        return self.string()
    def string(self):
        if self._value == None:
            return "_"
        else:
            return str(self._value)
