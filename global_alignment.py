def initialize_chart(seqa: list, seqb: list, gap):
    align_chart = []
    first_row = []
    points = 0
    r = range(0, gap * len(seqa), gap)
    values = [[[[x, i]] for i in range(len(seqa)+1)] for x in range(len(seqa)+1)]
    first_row = values[0]
    for index, element in enumerate(first_row):
        element.insert(0, index * gap)
    for i in range(1, len(seqa)+1):
        item = values[i][0]
        item.insert(0, i * gap)
        print(item)
    return values

        
        
    # for i in first_row:
    #     index = first_row.index(i)
    #     first_row.insert(index, index * gap)
    # print(first_row)

    # for i in range(len(seqa)):
    #     first_row.append([points, (0, i)])
    #     points += gap
    # align_chart.append(first_row)

    # points = gap
    # for i in range(1, len(seqb)):
    #     align_chart.append([(points, (i, 0))])
    #     for o
    #     points += gap
    
    # return align_chart

def global_alignment(chart, match, mismatch, gap):
    pass


y = initialize_chart(["A", "A", "C", "G", "C"], ["A", "A", "T", "C", "G"], -2)
for i in y:
    print(i)
