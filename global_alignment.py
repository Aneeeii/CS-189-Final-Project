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
            result = find_optimal_score(top_seq, bot_seq, (x,y), scores, match_info)
            chart[x][y].insert(0, result)
    temporary_chart = chart[:]
    if LT > LB:
        chart = chart[:LB+1]
    elif LB > LT:
        for index, row in enumerate(temporary_chart):
            row = row[:LT+1]
            chart[index] = row
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


def find_alignment(chart, sequences):
    top_seq, bot_seq = sequences
    last_row, last_column = len(chart)-1, len(chart[0])-1
    top_aligned = []
    bot_aligned = []
    for i in chart:
        print(i)
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
        if not error:
            try:
                check = chart[last_row][last_column]
                if chart[last_row][last_column][1] == [1,1]:
                    break
                if top_seq[last_column-2] == bot_seq[last_row-2]:
                    last_row, last_column = last_row-1, last_column-1
                    to_add = top_seq[last_column-1]
                    top_aligned.append(to_add)
                    bot_aligned.append(to_add)
                    continue
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
            except IndexError:
                error = True
        else:
            if last_row == 0:
                print("hi")
                break

    print(list(reversed(top_aligned)), list(reversed(bot_aligned)))

# y = initialize_chart(a, b, -2)
# for i in y:
#     print(i)

def main():
    b = list("C")
    a = list("A")
    match_info = (1,-1,-2)
    chart = fill_score((a,b), match_info)
    find_alignment(chart, (a,b))
# z = fill_score((a,b), (1,-1,-2))
# for i in z:
#     print(i)
main()