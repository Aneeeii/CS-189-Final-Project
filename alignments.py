def initialize_chart(seqa: list, seqb: list, gap):
    align_chart = []
    first_row = []
    points = 0
    for i in range(len(seqa)):
        first_row.append((points, (0, i)))
        points += gap
    align_chart.append(first_row)

    points = gap
    for i in range(1, len(seqb)):
        align_chart.append([(points, (i, 0))])
        points += gap
    
    return align_chart


def global_alignment(seqa, seqb, match, mismatch, gap):
    seqa_split = ["-"] + list(seqa)
    seqb_split = ["-"] + list(seqb)

    align_chart = initialize_chart(seqa_split, seqb_split, gap)

    print(align_chart)

    # a = seqa_split[0]
    # b = seqb_split[0]
    # value = 0
    # if 

    # need to save where they come from, and what value they have
    # save in a matrix?
    # local alignment uses less memory because it can disregard zeros?
    pass


a = "GACA"
b = "ACA"
global_alignment(a, b, 2, -1, -2)