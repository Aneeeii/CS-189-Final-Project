from types import UnionType
from typing import Any


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
    for j in range(len(seqa)):
        if seqa[j] == seqb[count]:
            # row x column
            unit = MatrixUnit(match, (j, count))
        else:
            unit = ZeroMatrixUnit((j, count))
        align_chart[j].append(unit)
    
    # initializes first row
    for k in range(0, len(seqb)):
        if k == 0:
            continue
        elif seqb[k] == seqa[0]:
            unit = MatrixUnit(match, (0, k))
        else:
            unit = ZeroMatrixUnit((0, k))
        align_chart[0].append(unit)

    return align_chart


def fill_chart(chart, gap, mismatch, match, start_pos, seqa, seqb):
    # only fills down
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
                if type(k) is ZeroMatrixUnit:
                    continue
                else:
                    unit.add_leading(k)
        
        chart[i].append(unit)
    
    if down_fill + 1 < len(seqa):
        x = down_fill + 1
    else:
        x = down_fill
    if across_fill + 1 < len(seqb):
        y = across_fill + 1
    else:
        y = across_fill

    return chart, (x, y)


def fill_across(chart, gap, mismatch, match, start_pos, seqa, seqb):
    down_fill = start_pos[0]
    across_fill = start_pos[1]
    for i in range(across_fill + 1, len(seqb)):
        previous = chart[down_fill - 1][i - 1]
        previous_value = previous.value()
        left = chart[down_fill][i - 1]
        up = chart[down_fill - 1][i]
        left_value = left.value()
        up_value = up.value()
        leads = []
        value = 0
        if seqb[i] == seqa[down_fill]:  # match
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
            unit = ZeroMatrixUnit((down_fill, i))
        else:
            unit = MatrixUnit(value, (down_fill, i))
            for k in leads:
                unit.add_leading(k)
        
        chart[down_fill].append(unit)
    
    if down_fill + 1 < len(seqa):
        x = down_fill + 1
    else:
        x = down_fill
    if across_fill + 1 < len(seqb):
        y = across_fill + 1
    else:
        y = across_fill

    return chart, (x, y)


def repeat(initial_pos, chart, seqa, seqb, match, mismatch, gap):
    end_pos = (len(seqa) - 1, len(seqb) - 1)
    current_pos = initial_pos
    while end_pos != current_pos:
        chart, new_pos = fill_chart(chart, gap, mismatch, match, current_pos, seqa, seqb)
        chart, current_pos = fill_across(chart, gap, mismatch, match, current_pos, seqa, seqb)
        current_pos = new_pos
    #     print(current_pos)
    # for i in chart:
    #     print(i)
    
    return chart


def get_max_location(chart, seqa, seqb):
    local_maxes = []
    for i in chart:
        local_maxes.append(max(i))
    total_max = max(local_maxes)
    return total_max


def trace_path(chart, unit):
    start_pos = unit.position()
    leads = unit.lead_to()

    if len(leads) > 1:
        for i in leads:
            yield from trace_path(chart, chart[i[0]][i[1]])
    elif not leads:
        yield
    else:
        lead = leads[0]
        new_unit = chart[lead[0]][lead[1]]
        yield new_unit


def main():
    seqa = ["A", "C", "G", "C"]
    seqb = ["G", "A", "T", "T", "G", "A"]
    a = create_matrix(seqa, seqb, 2)

    b = repeat((1, 1), a, seqa, seqb, 2, -1, -2)
    print(b)
    c = get_max_location(b, seqa, seqb)
    d = list(trace_path(b, c)) + [c]
    print(d)


if __name__ == "__main__":
    main()