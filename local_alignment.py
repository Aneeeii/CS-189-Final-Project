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


def fill_chart(chart, gap, mismatch, match, start_pos, seqa, seqb):
    down_fill = start_pos[0]
    across_fill = start_pos[1]

    for i in range(down_fill, len(seqa)):
        previous = chart[i - 1][across_fill - 1]
        previous_value = previous.value()
        left = chart[i][across_fill - 1]
        up = chart[i - 1][across_fill]
        left_value = left.value()
        up_value = up.value()
        leads = []
        value = 0
        if seqa[i] == seqb[across_fill]:  # match
            value = previous_value + match
            leads.append(previous.position())
        if value <= previous_value + mismatch: # mismatch
            if value == previous_value + mismatch and previous.position() not in leads:
                leads.append(previous.position())
            else:
                value = previous_value + mismatch
                leads = [previous.position()]
        if value <= up_value + gap:  # gap from top
            if value == up_value + gap and up.position() not in leads:
                leads.append(up.position())
            else:
                value = up_value + gap
                leads = [up.position()]
        if value <= left_value + gap:  # gap from side
            if value == left_value + gap and left.position() not in leads:
                leads.append(left.position())
            else:
                value = left_value + gap
                leads = [left.position()]
            
        if value <= 0:
            unit = ZeroMatrixUnit((i, across_fill))
        else:
            unit = MatrixUnit(value, (i, across_fill))
            for k in leads:
                unit.add_leading(k)
        
        chart[i].append(unit)
    
    return chart


a = create_matrix(["a", "b", "c"], ["b", "b", "c", "a"], 2)

b = fill_chart(a, -2, -1, 2, (1, 1), ["a", "b", "c"], ["b", "b", "c", "a"])

for i in b:
    print(i)