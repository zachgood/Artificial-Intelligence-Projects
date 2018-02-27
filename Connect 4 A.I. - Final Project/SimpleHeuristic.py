import C4Fast

# This heuristic evaluates the game by counting the number of open spots that would result in a win
# for 'X' and for 'O'.
# It returns count for 'X' - count for 'O'

def countSpotWins(C4game, piece):
    count = 0
    for row in range(6):
        for col in range(7):
            if C4game.getSpot(row, col) != ' ':
                continue
            C4game.placePiece(piece, row, col)
            if C4game.isWon()[0]: count += 1
            C4game.placePiece(' ', row, col)
    return count

def utility(C4game):
    return countSpotWins(C4game, 'X') - countSpotWins(C4game, 'O')


if __name__ == '__main__':
    c4 = C4Fast.C4(True)
    print(c4)
    print('above game has utility', utility(c4))
    c4.makeMove(1)
    print(c4)
    print('above game has utility', utility(c4))