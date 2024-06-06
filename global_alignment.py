def initialize_chart(seqa: list, seqb: list, gap):
    # align_chart = []
    first_row = []
    # points = 0
    # r = range(0, gap * len(seqa), gap)
    values = [[[[x, i]] for i in range(len(seqa)+1)] for x in range(len(seqa)+1)]
    first_row = values[0]
    for index, element in enumerate(first_row):
        element.insert(0, index * gap)
    for i in range(1, len(seqa)+1):
        item = values[i][0]
        item.insert(0, i * gap)
    return values

def correct_sequences(seqa, seqb, gap):
    length_difference = len(seqa) - len(seqb)
    adding, ref = seqa, seqb
    if len(seqa) < len(seqb):
        length_difference *= -1
        adding, ref = seqb, seqa
    for i in range(length_difference):
        ref.append(adding[-1])
    return initialize_chart(seqa, seqb, gap)

def fill_score(sequences, match_info):
    top_seq, bot_seq = sequences
    travel_values = {}
    LT, LB = len(top_seq), len(bot_seq)
    if LT > LB:
        longer = LT
    elif LB > LT:
        longer = LB
    else:
        longer = LT
    chart = correct_sequences(top_seq, bot_seq, match_info[2])
    for x in range(1, longer+1):
        for y in range(1, longer+1):
            diagonal_score = chart[x-1][y-1][0]
            top_score = chart[x][y-1][0]
            bot_score = chart[x-1][y][0]
            scores = (diagonal_score, top_score, bot_score)
            result, check = find_optimal_score(top_seq, bot_seq, (x,y), scores, match_info)
            if check == "diagonal":
                if (x-1,y-1) not in travel_values:
                    travel_values[(x-1,y-1)] = [(x,y)]
                else: 
                    travel_values[(x-1,y-1)].append((x,y))
            elif check == "top":
                if (x,y-1) not in travel_values:
                    travel_values[(x,y-1)] = [(x,y)]
                else: 
                    travel_values[(x,y-1)].append((x,y))
            elif check == "bot":
                if (x-1,y) not in travel_values:
                    travel_values[(x-1,y)] = [(x,y)]
                else: 
                    travel_values[(x-1,y)].append((x,y))
            chart[x][y].insert(0, result)
    temporary_chart = chart[:]
    if LT > LB:
        chart = chart[:LB+1]
    elif LB > LT:
        for index, row in enumerate(temporary_chart):
            row = row[:LT+1]
            chart[index] = row
    # for i in chart: # when going up on the side theres no path
        
    # for i in chart:
    #     print(i)
    # for i in travel_values:
    #     print(i, travel_values[i])
    return chart #travel_values

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
    result = max(new_diagonal, new_bot, new_top)
    if result == new_diagonal:
        value = "diagonal"
    elif result == new_bot:
        value = "bot"
    elif result == new_top:
        value = "top"
    return result, value


def find_right_path(travel_values, diagonal, top, left, current):
    dv = diagonal[0]
    tv = top[0]
    lv = left[0]
    values = [dv, tv, lv]
    print("hi")
    print(values)
    while True:
        best = max(values)
        if best == dv and tuple(current[1]) in travel_values[tuple(diagonal[1])]:
            return {tuple(current[1]): tuple(diagonal[1])}
        if best == tv and tuple(current[1]) in travel_values[tuple(top[1])]:
            return {tuple(current[1]): tuple(top[1])}
        if best == lv and tuple(current[1]) in travel_values[tuple(left[1])]:
            return {tuple(current[1]): tuple(left[1])}
        values.remove(best)
        
def return_indices(chart, tup):
    for i, row in enumerate(chart):
        for x, col in enumerate(row):
            if type(col) is not list:
                continue
            col = tuple(col[1])
            if col == tup:
                return (i,x)
    

# def find_alignment(chart, sequences, travel_values):
#     top_seq, bot_seq = sequences
#     top_alignment = []
#     bot_alignment = []
#     for i in chart:
#         print(i)
#     print()
#     print(travel_values)
#     last_row, last_column = len(chart)-1, len(chart[0])-1
#     paths = []
#     while True:
#         check = chart[last_row][last_column]
#         print(check)
#         if check == [0, [0,0]]:
#             break
#         diagonal = chart[last_row-1][last_column-1]
#         top = chart[last_row-1][last_column]
#         left = chart[last_row][last_column-1]
#         new = find_right_path(travel_values, diagonal, top, left, check)
#         paths.append(new)
#         new = list(new.values())
#         last_row, last_column = new[0]
#     print(paths)
#     temp_chart = []
#     for i in chart:
#         temp_chart.append(i[:])
#     top_temp = top_seq[:]
#     bot_temp = bot_seq[:]
#     tomp_temp = [""] + top_temp
#     new_chart = []
#     temp_chart.insert(0, tomp_temp)
#     for i in range(len(temp_chart)):
#         if i == 0 or i == 1:
#             temp_chart[i].insert(0, "")
#         else:
#             temp_chart[i].insert(0, bot_temp[i-2])
#     for i in temp_chart:
#         print(i)
#     # for i in temp_chart:
#     #     row = []
#     #     for x in i:
#     #         if type(x) is not list:
#     #             row.append(i)
#     #         else:
#     #             row.append(tuple(x[1]))
#     #     new_chart.append(row)
#     #     row = []
#     # for i in new_chart:
#     #     print(i)
        


#     for d in paths:
#         tup1, tup2 = list(d.keys())[0], list(d.values())[0]
#         if abs(tup1[0] - tup2[0]) == abs(tup1[1] - tup2[1]):
#             t = temp_chart[return_indices(temp_chart, tup1)[0]][0]
#             top_alignment.append(t)
#             bot_alignment.append(t)
#         elif abs(tup1[0] - tup2[0]) == 0 and abs(tup1[1] - tup2[1]) == 1:
#             t = temp_chart[return_indices(temp_chart, tup1)[0]][0]
#             top_alignment.append("-")
#             bot_alignment.append(t)
#             # top_alignment.append()
#         elif abs(tup1[0] - tup2[0]) == 1 and abs(tup1[1] - tup2[1]) == 0:
#             t = temp_chart[0][return_indices(temp_chart, tup1)[0]]
#             bot_alignment.append("-")
#             top_alignment.append(t)
#     print(bot_alignment)
#     print(top_alignment)
    

def find_alignment(chart, sequences):
    top_seq, bot_seq = sequences
    last_row, last_column = len(chart)-1, len(chart[0])-1
    top_aligned = []
    bot_aligned = []
    first = True
    error = False
    while True:
        if first:
            if top_seq[-1] == bot_seq[-1]:
                top_aligned.append(top_seq[-1])
                bot_aligned.append(top_seq[-1])
            else:
                top_aligned.append(top_seq[-1])
                bot_aligned.append(bot_seq[-1])
            first = False
        check = chart[last_row][last_column]
        if chart[last_row][last_column][1] == [1,1]:
            break
        try:
            if top_seq[last_column-2] == bot_seq[last_row-2]:
                last_row, last_column = last_row-1, last_column-1
                to_add = top_seq[last_column-1]
                top_aligned.append(to_add)
                bot_aligned.append(to_add)
                continue
        except IndexError:
            pass
        diagonal = chart[last_row-1][last_column-1][0]
        top = chart[last_row-1][last_column][0]
        left = chart[last_row][last_column-1][0]
        values = [diagonal, top, left]
        greatest = max(values)
        if values.count(greatest) > 1:
            if values[0] == greatest:
                top_aligned.append(top_seq[last_column-2])
                bot_aligned.append(bot_seq[last_row-2])
                last_row, last_column = last_row-1, last_column-1
        elif values[0] == greatest:
            if last_row != 0 and last_column != 0:
                top_aligned.append(top_seq[last_column-2])
                bot_aligned.append(bot_seq[last_row-2])
            last_row, last_column = last_row-1, last_column-1
        elif values[1] == greatest:
            top_aligned.append("-")
            bot_aligned.append(bot_seq[last_row-2])
            last_row, last_column = last_row-1, last_column
        elif values[2] == greatest:
            bot_aligned.append("-")
            top_aligned.append(top_seq[last_column-2])
            last_row, last_column = last_row, last_column-1
        if last_row < 0 and last_column > 0:
            times = check[1][1]
            top_aligned.pop(-1)
            bot_aligned.pop(-1)
            bot_aligned += ["-"] * times
            top_aligned += top_seq[:times]
            break
        if last_row > 0 and last_column < 0:
            times = check[1][1]
            top_aligned.pop(-1)
            bot_aligned.pop(-1)
            top_aligned += ["-"] * times
            bot_aligned += bot_seq[:times]
            break
        if last_row < 0 and last_column < 0:
            break

    return list(reversed(top_aligned)),list(reversed(bot_aligned))

def run(seqa, seqb, match_info):
    a = seqa
    b = seqb
    c = a[:]
    d = b[:]
    scores = []
    final = []
    chart = fill_score((a,b), match_info) #, travel_values
    
    result = find_alignment(chart, (c,d))
    for i in chart:
        for x in i:
            scores.append(x[0])
        final.append(scores)
        scores = []
    return result, final