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


class ZeroMatrixUnit:
    def __init__(self, position):
        self._value = 0
        self._position = position
    
    def value(self):
        return self._value

    def position(self):
        return self._position


def create_matrix(seqa: list, seqb: list, match):
    #   s e q b
    # s
    # e
    # q
    # a

    align_chart = []

    # creates a blank matrix
    for i in range(len(seqa)):
        align_chart.append([])

    # initializes first column
    count = 0
    for j in seqa:
        if j == seqb[count]:
            # row x column
            unit = MatrixUnit(match, (seqa.index(j), count))
        else:
            unit = ZeroMatrixUnit((seqa.index(j), count))
        align_chart[seqa.index(j)].append(unit)
    
    # initializes first row
    for k in seqb[1:]:
        if k == seqa[0]:
            unit = MatrixUnit(match, (0, seqb.index(k)))
        else:
            unit = ZeroMatrixUnit((0, seqb.index(k)))
        align_chart[0].append(unit)
    
    return align_chart


def fill_chart(chart, gap, mismatch, match, start_pos):
    down_fill = start_pos[0]
    across_fill = start_pos[1]
    


a = create_matrix(["a", "b", "c"], ["b", "b", "c", "a"], 2)
for i in a:
    print(i)

fill_chart(a, -2, -1, 2, (1, 1))