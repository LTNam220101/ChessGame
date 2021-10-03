import pygame as p
import ChessEngine

WIDTH = HEIGHT = 768
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''


def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wB', 'wN', 'wR', 'wQ', 'wK', 'wp']
    blocks = ['blackBlock', 'whiteBlock', 'blackBlock1', 'whiteBlock1', 'highlightBlock']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        IMAGES[piece + "l"] = p.transform.scale(p.image.load("images/" + piece + "l.png"), (SQ_SIZE, SQ_SIZE))
    for block in blocks:
        IMAGES[block] = p.transform.scale(p.image.load("images/" + block + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gameState = ChessEngine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False
    animation = False
    loadImages()
    running = True
    sqSelected = ()  # tuple (row, col)
    playerClicks = []  # keep track of player clicks (2 tuples: [(6, 4), (4, 4)] ex
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                # LEFT CLICK
                if e.button == 1:
                    location = p.mouse.get_pos()  # (x, y) location of mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    # if 2 click on the same square
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    # else:
                    #     # if 1st click on an empty square
                    #     if len(playerClicks) == 0 and gameState.board[row][col] == '--':
                    #         playerClicks = []
                    #         sqSelected = ()
                    #         firstClick = False
                    #     # if white turn but 1st click on an black one
                    #     # or black turn but 1st click on an white one
                    #     if (len(playerClicks) == 0 and gameState.whiteToMove and gameState.board[row][col][0] == 'b') or \
                    #             (len(playerClicks) == 0 and not gameState.whiteToMove and gameState.board[row][col][
                    #                 0] == 'w'):
                    #         playerClicks = []
                    #         sqSelected = ()
                    #         firstClick = False
                    #     # if 2nd click on an ally, playerClicks = [ally]
                    #     elif len(playerClicks) == 1 and gameState.board[row][col][0] == \
                    #             gameState.board[playerClicks[0][0]][playerClicks[0][1]][0]:
                    #         sqSelected = (row, col)
                    #         playerClicks = [sqSelected]
                    #         firstClick = True
                    #     # if it's turn white but 1st click on a black one or
                    #     # turn black but 1st click on a white one,
                    #     elif (len(playerClicks) == 1 and gameState.board[playerClicks[0][0]][playerClicks[0][1]][
                    #         0] == 'b' and gameState.whiteToMove) \
                    #             or (len(playerClicks) == 1 and gameState.board[playerClicks[0][0]][playerClicks[0][1]][
                    #         0] == 'w' and not gameState.whiteToMove):
                    #         # if 2nd click on right one
                    #         if gameState.board[row][col][0] != gameState.board[playerClicks[0][0]][playerClicks[0][1]][
                    #             0]:
                    #             sqSelected = (row, col)
                    #             playerClicks = [sqSelected]
                    #             firstClick = True
                    #         else:
                    #             playerClicks = []
                    #             sqSelected = ()
                    #             firstClick = False
                    #     else:
                    #         sqSelected = (row, col)
                    #         playerClicks.append(sqSelected)
                    #         firstClick = True
                    # if len(playerClicks) == 2:
                    #     move = ChessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)
                    #     print(move.isEnPassantMove)
                    #     if move in validMoves:
                    #         gameState.makeMove(move)
                    #         moveMade = True
                    #         sqSelected = ()
                    #         playerClicks = []
                    #     else:
                    #         playerClicks = []
                    #         firstClick = False
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gameState.makeMove(validMoves[i])
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
                # RIGHT CLICK
                elif e.button == 3:
                    gameState.undoMove()
                    moveMade = True
        if moveMade:
            if animation:
                animationMove(gameState.moveLog[-1], screen, gameState.board, clock, gameState.whiteToMove)
            validMoves = gameState.getValidMoves()
            moveMade = False

        drawGameState(screen, gameState, gameState.whiteToMove, gameState.getValidMoves(), sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gameState, whiteToMove, validMoves, sqSelected):
    drawBroad(screen)
    highlight(screen, gameState, validMoves, sqSelected)
    drawPieces(screen, gameState.board, whiteToMove)


def drawBroad(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            screen.blit(IMAGES['whiteBlock1'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)) if (
                                                        r + c) % 2 == 0 else screen.blit(
                IMAGES['blackBlock1'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board, whiteToMove):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':  # Not empty
                if whiteToMove:
                    if piece[0] == 'w':
                        piece = piece + 'l'
                else:
                    if piece[0] == 'b':
                        piece = piece + 'l'
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight(screen, gameState, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gameState.board[r][c][0] == ('w' if gameState.whiteToMove else 'b'):
            p.draw.rect(screen, p.Color('yellow'), (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    p.draw.circle(screen, (0, 0, 139), ((move.endCol+0.5)*SQ_SIZE, (move.endRow+0.5)*SQ_SIZE), 12)


def animationMove(move, screen, board, clock, whiteToMove):
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 5  # frame to move 1 square
    frameCount = (abs(dR) + abs(dC)) * framePerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBroad(screen)
        drawPieces(screen, board, whiteToMove)
        # erase piece moved from it's ending square
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, (0,255,0), endSquare)
        # draw captured piece onto ractangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
