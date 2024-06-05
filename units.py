class MatrixUnit:
    def __init__(self, value, position):
        self._value = value
        self._position = position
        self._lead_to = []
    
    def value(self):
        return self._value
    
    def position(self):
        return self._position
    
    def lead_to(self):
        return self._lead_to
    
    def add_leading(self, position):
        self._lead_to.append(position)

    def __lt__(self, other):
        if type(other) is MatrixUnit or type(other) is ZeroMatrixUnit:
            return self.value() < other.value()
        else:
            return NotImplemented
    
    def __eq__(self, other: object) -> bool:
        if type(other) is MatrixUnit or type(other) is ZeroMatrixUnit:
            return self.value() == other.value()
        else:
            return NotImplemented
    
    def __le__(self, other):
        if type(other) is MatrixUnit or type(other) is ZeroMatrixUnit:
            return self.value() <= other.value()
        else:
            return NotImplemented



class ZeroMatrixUnit:
    def __init__(self, position):
        self._value = 0
        self._position = position
    
    def value(self):
        return self._value

    def position(self):
        return self._position

    def __lt__(self, other):
        if type(other) is MatrixUnit or type(other) is ZeroMatrixUnit:
            return self.value() < other.value()
        else:
            return NotImplemented
    
    def __eq__(self, other: object) -> bool:
        if type(other) is MatrixUnit or type(other) is ZeroMatrixUnit:
            return self.value() == other.value()
        else:
            return NotImplemented
    
    def __le__(self, other):
        if type(other) is MatrixUnit or type(other) is ZeroMatrixUnit:
            return self.value() <= other.value()
        else:
            return NotImplemented