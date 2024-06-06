from types import UnionType
from typing import Any
import units


def create_matrix(seqa: list, seqb: list, match):
    align_chart = []

    # creates a blank matrix
    for i in range(len(seqa)):
        align_chart.append([])

    # initializes first column
    count = 0
    for j in range(len(seqa)):
        if seqa[j] == seqb[count]:
            # row x column
            unit = units.MatrixUnit(match, (j, count))
        else:
            unit = units.ZeroMatrixUnit((j, count))
        align_chart[j].append(unit)
    
    # initializes first row
    for k in range(0, len(seqb)):
        if k == 0:
            continue
        elif seqb[k] == seqa[0]:
            unit = units.MatrixUnit(match, (0, k))
        else:
            unit = units.ZeroMatrixUnit((0, k))
        align_chart[0].append(unit)

    return align_chart


def fill_chart(chart, gap, mismatch, match, start_pos, seqa, seqb):
    # only fills down
    down_fill = start_pos[0]
    across_fill = start_pos[1]

    for i in range(down_fill, len(seqa)):
        # if down_fill < across_fill:
        #     break
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
            unit = units.ZeroMatrixUnit((i, across_fill))
        else:
            unit = units.MatrixUnit(value, (i, across_fill))
            for k in leads:
                if type(k) is units.ZeroMatrixUnit:
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
        # if across_fill < down_fill:
        #     break
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
            unit = units.ZeroMatrixUnit((down_fill, i))
        else:
            unit = units.MatrixUnit(value, (down_fill, i))
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


def keep_repeat(chart, seqa, seqb):
    if len(chart) < len(seqa):
        return False
    for i in chart:
        if len(i) < len(seqb):
            return False
    return True


def repeat(initial_pos, chart, seqa, seqb, match, mismatch, gap):
    current_pos = initial_pos
    while not keep_repeat(chart, seqa, seqb):
        chart, new_pos = fill_chart(chart, gap, mismatch, match, current_pos, seqa, seqb)
        chart, current_pos = fill_across(chart, gap, mismatch, match, current_pos, seqa, seqb)
        current_pos = new_pos
    
    return chart


def get_max_location(chart, seqa, seqb):
    local_maxes = []
    for i in chart:
        local_maxes.append(max(i))
    
    highest = None
    total_max = []
    for j in local_maxes:
        if highest is None:
            highest = j
            total_max.append(j)
        if highest < j:
            highest = j
            total_max = [j]
        elif highest == j:
            total_max.append(j)
    return total_max


def trace_path(chart, unit, path: list):
    start_pos = unit.position()
    leads = unit.lead_to()

    path.append(unit)

    if len(leads) > 1:
        for i in leads:
            new = trace_path(chart, chart[i[0]][i[1]], path)
            new += path
            path = new
    elif len(leads) == 1:
        lead = leads[0]
        new_unit = chart[lead[0]][lead[1]]
        path = trace_path(chart, new_unit, path)
    
    return path


def find_alignments(seqa, seqb, match, mismatch, gap):
    paths = []
    init_chart = create_matrix(seqa, seqb, match)
    chart = repeat((1, 1), init_chart, seqa, seqb, match, mismatch, gap)
    maxes = get_max_location(chart, seqa, seqb)
    print(maxes[0].position(), maxes[0].value())
    for i in maxes:
        pathway = trace_path(chart, i, [])
        # pathway = list(trace_path(chart, i)) + [i]
        # print("pathway:", pathway)
        # print(pathway)
        # for j in pathway:
        #     print(j.value(), j.position())
        # while None in pathway:
        #     pathway.remove(None)
        paths.append(pathway[::-1])
    
    return chart, paths


def stringify(paths, seqa, seqb):
    paths_aligned = []
    for p in paths:
        indices = []
        for unit in p:
            position = unit.position()
            indices.append(position)
        align_a = []
        align_b = []
        for i in indices:
            if indices.index(i) == 0:
                align_a.append(seqa[i[0]])
                align_b.append(seqb[i[1]])
            else:
                ind = indices.index(i) - 1
                previous = indices[ind]
                if previous[0] == i[0]:
                    align_a.append("-")
                    align_b.append(seqb[i[1]])
                elif previous[1] == i[1]:
                    align_a.append(seqa[i[0]])
                    align_b.append("-")
                else:
                    align_a.append(seqa[i[0]])
                    align_b.append(seqb[i[1]])
        paths_aligned.append((align_a, align_b))
    
    return paths_aligned


def total():
    seqa = ["A", "A", "T", "G"]
    seqb = ["G", "A", "T", "T", "G", "A"]
    chart, paths = find_alignments(seqa, seqb, 2, -1, -2)
    paths_aligned = stringify(paths, seqa, seqb)
    # print(paths)
    # for j in paths[0]:
    #     print(j.position(), j.value())
    print(paths_aligned)
    # for i in paths_aligned:
    #     print(i[0])
    #     print(i[1])
    # print(chart)


# set it so seqa is the shorter string

total()