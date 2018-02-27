import C4Fast
import C4Helpers
import time

# This Heuristic evaluates the game by counting the single, double, and triple open spots
# that would result in a win if 'X' or 'O' was placed.
# It returns the count for X - the count for Y

# Larger number => better for X
# Smaller number => better for O
# => positive number = state is more favorable for X
# => negative number = state is more favorable for O

# Returns counts for number of single, double, and triple spots in given group that would make 4 in a row for piece type
# count2win([' ', 'X', 'O', 'X', 'X', ' ', ' '], 'O') => 0, 1, 1 is an non-optimal example b/c win is counted twice
def count2win(group, piece):
    # print('In count to win with group {} and piece {}'.format(group, piece))
    count1 = count2 = count3 = 0
    emptySpots = [i for i, ltr in enumerate(group) if ltr == ' '] # find(group, ' ')
    for i in range(len(emptySpots)):
        group[emptySpots[i]] = piece # print('Checking win for group ', group)
        if piece * 4 in ''.join(group):
            count1 += 1
            group[emptySpots[i]] = ' '
            continue # Because we dont want to count the win twice.  Like, once for 4 in a row and once for 5 in a row
        for j in range(i+1, len(emptySpots)):
            group[emptySpots[j]] = piece # print('\tChecking win for group ', group)
            if piece * 4 in ''.join(group):
                count2 += 1
                group[emptySpots[j]] = ' '
                continue # Same thing here
            for k in range(j+1, len(emptySpots)):
                group[emptySpots[k]] = piece # print('\t\tChecking win for group ', group)
                if piece * 4 in ''.join(group):
                    count3 += 1
                group[emptySpots[k]] = ' '
            group[emptySpots[j]] = ' '
        group[emptySpots[i]] = ' '
    return count1, count2, count3


def allCounts2Win(C4game):
    XfullCount1 = XfullCount2 = XfullCount3 = 0
    OfullCount1 = OfullCount2 = OfullCount3 = 0
    for g in C4game.getGroups():
        if g.count('X'):
            Xcount1, Xcount2, Xcount3 = count2win(g, 'X')
            XfullCount1 += Xcount1
            XfullCount2 += Xcount2
            XfullCount3 += Xcount3
        if g.count('O'):
            Ocount1, Ocount2, Ocount3 = count2win(g, 'O')
            OfullCount1 += Ocount1
            OfullCount2 += Ocount2
            OfullCount3 += Ocount3
    return [[XfullCount1, XfullCount2, XfullCount3], [OfullCount1, OfullCount2, OfullCount3]]

# counts for x - counts for y summed
def utility1(C4game):
    allCounts = allCounts2Win(C4game)
    return sum([a - b for a, b in zip(allCounts[0], allCounts[1])])

# counts for x - counts for y count1*3,count2*2,count3*1 then summed
def utility2(C4game):
    allCounts = allCounts2Win(C4game)
    return sum([a * b for a, b in zip([a - b for a, b in zip(allCounts[0], allCounts[1])], [3, 2, 1])])

# counts for x - counts for y count1^3,count2^2,count3^1 then summed
def utility3(C4game):
    allCounts = allCounts2Win(C4game)
    subtract = [a - b for a, b in zip(allCounts[0], allCounts[1])]
    value = subtract[0]**3
    value += subtract[1]**2 if subtract[1] > 0 else subtract[1]**2*-1
    value += subtract[2]
    return value


if __name__ == '__main__':
    # c4f = C4Helpers.randomBoard(15)
    c4f = C4Fast.C4(load=True)
    c4f.makeMove(1)
    print(c4f)
    print(allCounts2Win(c4f))
    print(utility1(c4f))
    print(utility2(c4f))
    print(utility3(c4f))



    # l = ['X', ' ', ' ', ' ', 'O', 'C', ' ']
    # if l.count('X'):
    #     print('l has an X!')
    # if l.count('O'):
    #     print('l has an O!')

