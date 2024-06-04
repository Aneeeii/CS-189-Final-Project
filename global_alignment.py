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


def correct_sequences(seqa, seqb, gap):
    length_difference = len(seqa) - len(seqb)
    adding, ref = seqa, seqb
    if len(seqa) < len(seqb):
        length_difference *= -1
        adding, ref = seqb, seqa
    for i in range(length_difference):
        ref.append(adding[-1])
    return initialize_chart(seqa, seqb, gap)

def fill_score(sequences, match_info, chart):
    top_seq, bot_seq = sequences
    for x in range(1, len(top_seq)+1):
        for y in range(1, len(top_seq)+1):
            diagonal_score = chart[x-1][y-1][0]
            top_score = chart[x][y-1][0]
            bot_score = chart[x-1][y][0]
            scores = (diagonal_score, top_score, bot_score)
            result = find_optimal_score(top_seq, bot_seq, (x,y), scores, match_info)
            chart[x][y].insert(0, result)
    return chart

def find_optimal_score(top_seq, bot_seq, coordinates, scores, match_info):
    match, mismatch, gap =  match_info
    diagonal, top, bot = scores
    x,y = coordinates
    if top_seq[y-1] == bot_seq[x-1]:
        new_diagonal = diagonal + match
    else:
        new_diagonal = diagonal + mismatch
    new_bot = bot + gap
    new_top = top + gap
    return max(new_diagonal, new_bot, new_top)


a = list("GTCGACGCA")
b = list("GATTACAAA")
y = initialize_chart(a, b, -2)
# for i in y:
#     print(i)


z = global_alignment((a,b), (1,-1,-2), y)
for i in z:
    print(i)