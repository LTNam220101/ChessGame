import pygame as p
import ChessEngine
import time
import AI

TIME = 48
BORDER = 32
BOARD = 640
MENU = 100
MOVE_LOG = 350
WIDTH = MENU + BOARD + BORDER * 2 + MOVE_LOG
HEIGHT = BOARD + TIME * 2 + BORDER * 2
DIMENSION = 8
SQ_SIZE = (HEIGHT - 2 * BORDER - 2 * TIME) // DIMENSION
MAX_FPS = 15
IMAGES = {}
TIME_LIMIT = remain_time = 600


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Auto Chess", "None")
    screen.fill('#333333')
    start = True
    running = False
    while start:
        global playerOne, playerTwo
        if not running:
            drawMenuState(screen)
            for e in p.event.get():
                if e.type == p.QUIT:
                    start = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()  # (x, y) location of mouse
                    print(location)
                    # 2P
                    # if 278 <= location[0] < 474 and 439 <= location[1] < 500:
                    #     running = True
                    #     playerOne = True
                    #     playerTwo = True
                    if 540 <= location[1] < 590:
                        if 300 <= location[0] < 450:
                            # 1P
                            running = True
                            playerOne = True
                            playerTwo = False
                        elif 526 <= location[0] < 677:
                            # 2P
                            running = True
                            playerOne = True
                            playerTwo = True
                        elif 728 <= location[0] < 880:
                            # 0P
                            running = True
                            playerOne = False
                            playerTwo = False
            p.display.flip()
        else:
            start_time = time.time()
            clock = p.time.Clock()
            gameState = ChessEngine.GameState()
            validMoves = gameState.getValidMoves()
            moveMade = False
            animation = False
            gameOver = False
            loadImages()
            sqSelected = ()  # tuple (row, col)
            playerClicks = []  # keep track of player clicks (2 tuples: [(6, 4), (4, 4)] ex
            global remain_time
            while running:
                humanTurn = (gameState.whiteToMove and playerOne) or (not gameState.whiteToMove and playerTwo)
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    if e.type == p.MOUSEBUTTONDOWN:
                        # LEFT CLICK
                        if e.button == 1:
                            location = p.mouse.get_pos()  # (x, y) location of mouse
                            # print(location)
                            if MENU + BORDER <= location[0] < MENU + BORDER + BOARD and 80 <= location[1] < 720 and not gameOver and humanTurn:
                                col = (location[0] - BORDER - MENU) // SQ_SIZE
                                row = (location[1] - BORDER - TIME) // SQ_SIZE
                                # Unselect
                                if sqSelected == (row, col):
                                    sqSelected = ()
                                    playerClicks = []
                                else:
                                    sqSelected = (row, col)
                                    playerClicks.append(sqSelected)
                                if len(playerClicks) == 2:
                                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)
                                    for i in range(len(validMoves)):
                                        if move == validMoves[i]:
                                            # print(str(move.pieceMoved)+str((move.startRow, move.startCol))+str((move.endRow, move.endCol
                                            gameState.makeMove(validMoves[i])
                                            moveMade = True
                                            animation = False
                                            sqSelected = ()
                                            playerClicks = []
                                            start_time = time.time()
                                            if gameState.promoteTime != '':
                                                print('Promote Completed!')
                                                gameState.promoteTime = ''
                                        if not moveMade:
                                            playerClicks = [sqSelected]
                            elif 25 <= location[0] < 75:
                                # Menu
                                if 63 <= location[1] < 113:
                                    running = False
                                # 1P
                                if 150 <= location[1] < 200:
                                    start_time = time.time()
                                    clock = p.time.Clock()
                                    gameState = ChessEngine.GameState()
                                    validMoves = gameState.getValidMoves()
                                    moveMade = False
                                    animation = False
                                    gameOver = False
                                    playerOne = True
                                    playerTwo = False
                                    sqSelected = ()  # tuple (row, col)
                                    playerClicks = []  # keep track of player clicks (2 tuples: [(6, 4), (4, 4)] ex
                                    global remain_time
                                    drawGameState(screen, gameState, gameState.getValidMoves(), sqSelected)
                                # 2P
                                elif 230 <= location[1] < 28:
                                    start_time = time.time()
                                    clock = p.time.Clock()
                                    gameState = ChessEngine.GameState()
                                    validMoves = gameState.getValidMoves()
                                    moveMade = False
                                    animation = False
                                    gameOver = False
                                    playerOne = True
                                    playerTwo = True
                                    sqSelected = ()  # tuple (row, col)
                                    playerClicks = []  # keep track of player clicks (2 tuples: [(6, 4), (4, 4)] ex
                                    global remain_time
                                    drawGameState(screen, gameState, gameState.getValidMoves(), sqSelected)
                                # 0P
                                elif 330 <= location[1] < 380:
                                    start_time = time.time()
                                    clock = p.time.Clock()
                                    gameState = ChessEngine.GameState()
                                    validMoves = gameState.getValidMoves()
                                    moveMade = False
                                    animation = False
                                    gameOver = False
                                    playerOne = False
                                    playerTwo = False
                                    sqSelected = ()  # tuple (row, col)
                                    playerClicks = []  # keep track of player clicks (2 tuples: [(6, 4), (4, 4)] ex
                                    global remain_time
                                    drawGameState(screen, gameState, gameState.getValidMoves(), sqSelected)
                                # Undo
                                if 417 <= location[1] < 471:
                                    if playerOne and playerTwo:
                                        gameState.undoMove()
                                    else:
                                        gameState.undoMove()
                                        gameState.undoMove()
                                    moveMade = True
                                    animation = False
                                    gameOver = False
                                # New Game
                                if 516 <= location[1] < 569:
                                    start_time = time.time()
                                    clock = p.time.Clock()
                                    gameState = ChessEngine.GameState()
                                    validMoves = gameState.getValidMoves()
                                    moveMade = False
                                    animation = False
                                    gameOver = False
                                    sqSelected = ()  # tuple (row, col)
                                    playerClicks = []  # keep track of player clicks (2 tuples: [(6, 4), (4, 4)] ex
                                    global remain_time
                                    drawGameState(screen, gameState, gameState.getValidMoves(), sqSelected)
                        # RIGHT CLICK
                        elif e.button == 3:
                            if playerOne and playerTwo:
                                gameState.undoMove()
                            else:
                                gameState.undoMove()
                                gameState.undoMove()
                            moveMade = True
                            animation = False
                            gameOver = False

                # AI move
                if not gameOver and not humanTurn:
                    for e in p.event.get():
                        if e.type == p.MOUSEBUTTONDOWN:
                            if e.button == 1:
                                location = p.mouse.get_pos()  # (x, y) location of mouse
                                if 25 <= location[0] < 75:
                                    # Menu
                                    if 63 <= location[1] < 113:
                                        running = False
                                    # 1P
                                    if 150 <= location[1] < 200:
                                        start_time = time.time()
                                        clock = p.time.Clock()
                                        gameState = ChessEngine.GameState()
                                        validMoves = gameState.getValidMoves()
                                        moveMade = False
                                        animation = False
                                        gameOver = False
                                        sqSelected = ()  # tuple (row, col)
                                        playerClicks = []  # keep track of player clicks (2 tuples: [(6, 4), (4, 4)] ex
                                        global remain_time
                                        drawGameState(screen, gameState, gameState.getValidMoves(), sqSelected)
                                        playerOne = True
                                        playerTwo = False
                                    # 2P
                                    elif 230 <= location[1] < 28:
                                        start_time = time.time()
                                        clock = p.time.Clock()
                                        gameState = ChessEngine.GameState()
                                        validMoves = gameState.getValidMoves()
                                        moveMade = False
                                        animation = False
                                        gameOver = False
                                        sqSelected = ()  # tuple (row, col)
                                        playerClicks = []  # keep track of player clicks (2 tuples: [(6, 4), (4, 4)] ex
                                        global remain_time
                                        drawGameState(screen, gameState, gameState.getValidMoves(), sqSelected)
                                        playerOne = True
                                        playerTwo = True
                                    # 0P
                                    elif 330 <= location[1] < 380:
                                        start_time = time.time()
                                        clock = p.time.Clock()
                                        gameState = ChessEngine.GameState()
                                        validMoves = gameState.getValidMoves()
                                        moveMade = False
                                        animation = False
                                        gameOver = False
                                        sqSelected = ()  # tuple (row, col)
                                        playerClicks = []  # keep track of player clicks (2 tuples: [(6, 4), (4, 4)] ex
                                        global remain_time
                                        drawGameState(screen, gameState, gameState.getValidMoves(), sqSelected)
                                        playerOne = False
                                        playerTwo = False

                    move = AI.findRandomMove(validMoves)
                    # move = AI.findBestMoveMinMax(gameState, validMoves)
                    if move is None:
                        move = AI.findRandomMove(validMoves)
                    gameState.makeMove(move)
                    moveMade = True
                    animation = False

                if moveMade:
                    if animation:
                        animationMove(gameState.moveLog[-1], screen, gameState.board, clock)
                    validMoves = gameState.getValidMoves()
                    moveMade = False

                drawGameState(screen, gameState, gameState.getValidMoves(), sqSelected)

                if gameState.checkmate:
                    gameOver = True
                    gameOverText(screen, gameState.whiteToMove)
                elif gameState.stalemate:
                    gameOver = True
                    gameOverText(screen, gameState.whiteToMove)
                remain_time = TIME_LIMIT - int(time.time() - start_time)
                gameOver = drawTime(screen, gameState.whiteToMove, gameOver)
                clock.tick(MAX_FPS)
                p.display.flip()


'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''


def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wB', 'wN', 'wR', 'wQ', 'wK', 'wp']
    blocks = ['blackBlock', 'whiteBlock', 'blackBlock1', 'whiteBlock1', 'highlightBlock']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chessOri/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # IMAGES[piece + "l"] = p.transform.scale(p.image.load("images/" + piece + "l.png"), (SQ_SIZE, SQ_SIZE))
    for block in blocks:
        IMAGES[block] = p.transform.scale(p.image.load("images/" + block + ".png"), (SQ_SIZE, SQ_SIZE))


def drawMenuState(screen):
    board = p.transform.scale(p.image.load("chessv2/menu1.png"), (WIDTH, HEIGHT))
    screen.blit(board, (0, 0))


def drawGameState(screen, gameState, validMoves, sqSelected):
    board = p.transform.scale(p.image.load("chessv2/menu.png"), (WIDTH, HEIGHT))
    screen.blit(board, (0, 0))
    drawBroad(screen)
    highlightPieces(screen, gameState, sqSelected)
    drawPieces(screen, gameState.board)
    highlightMoves(screen, gameState, validMoves, sqSelected)
    drawMoveLog(screen, gameState)


def drawBroad(screen):
    # board = p.image.load("chessv2/board2.png")
    board = p.transform.scale(p.image.load("chessv2/board2big.png"), (BOARD + BORDER * 2, BOARD + BORDER * 2))
    screen.blit(board, (MENU, TIME))
    # for r in range(DIMENSION):
    #     for c in range(DIMENSION):
    #         screen.blit(IMAGES['whiteBlock1'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)) if (
    #                                                     r + c) % 2 == 0 else screen.blit(
    #             IMAGES['blackBlock1'], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlightPieces(screen, gameState, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if r >= 0 and c >= 0:
            if gameState.board[r][c][0] == ('w' if gameState.whiteToMove else 'b'):
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)
                s.fill(p.Color('blue'))
                screen.blit(s, (c * SQ_SIZE + BORDER + MENU, r * SQ_SIZE + BORDER + TIME))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':  # Not empty
                screen.blit(IMAGES[piece],
                            p.Rect(c * SQ_SIZE + BORDER + MENU, r * SQ_SIZE + BORDER + TIME, SQ_SIZE, SQ_SIZE))


def highlightMoves(screen, gameState, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if r >= 0 and c >= 0:
            if gameState.board[r][c][0] == ('w' if gameState.whiteToMove else 'b'):
                for move in validMoves:
                    if move.startRow == r and move.startCol == c:
                        p.draw.circle(screen, p.Color('blue'), (
                            (move.endCol + 0.5) * SQ_SIZE + BORDER + MENU,
                            (move.endRow + 0.5) * SQ_SIZE + BORDER + TIME), 12)


def animationMove(move, screen, board, clock):
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 2  # frame to move 1 square
    frameCount = (abs(dR) + abs(dC)) * framePerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBroad(screen)
        drawPieces(screen, board)
        # erase piece moved from it's ending square
        endSquare = p.Rect(move.endCol * SQ_SIZE + BORDER, move.endRow * SQ_SIZE + BORDER + TIME, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, (0, 255, 0), endSquare)
        # draw captured piece onto ractangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved],
                    p.Rect(c * SQ_SIZE + BORDER, r * SQ_SIZE + BORDER + TIME, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawTime(screen, whiteToMove, gameOver):
    global remain_time
    m, s = divmod(remain_time, 60)
    h, m = divmod(m, 60)
    timeLeft = str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
    color = p.Color('White')
    if remain_time <= 10:
        color = p.Color('Red')
    if remain_time == 0:
        gameOver = True
        gameOverText(screen, whiteToMove)
    GAME_FONT = p.font.Font('./Font/Digital Dismay.otf', 50)
    if not whiteToMove:
        textBlack = GAME_FONT.render(timeLeft, 0, color)
        textWhite = GAME_FONT.render('00:10:00', 0, color)
    else:
        textWhite = GAME_FONT.render(timeLeft, 0, color)
        textBlack = GAME_FONT.render('00:10:00', 0, color)
    textBlackLocation = p.Rect(SQ_SIZE + BORDER + MENU, 0, 60, 60)
    textWhiteLocation = p.Rect(SQ_SIZE + BORDER + MENU, SQ_SIZE * 8 + TIME + BORDER * 2, 60,
                               60)
    surfaceBlackLocation = p.Rect(SQ_SIZE + BORDER - 10 + MENU, 0, 60, 60)
    surfaceWhiteLocation = p.Rect(SQ_SIZE + BORDER - 10 + MENU, SQ_SIZE * 8 + TIME + BORDER * 2, 60, 60)
    s = p.Surface((textBlack.get_width() + 20, TIME))
    s.fill('#000000')
    screen.blit(s, surfaceBlackLocation)
    screen.blit(s, surfaceWhiteLocation)
    screen.blit(textBlack, textBlackLocation)
    screen.blit(textWhite, textWhiteLocation)
    return gameOver


def gameOverText(screen, whiteToMove):
    green = (0, 255, 0)
    font = p.font.Font('freesansbold.ttf', 100)
    winner = "Black Win!" if whiteToMove else "White Win!"
    textObj = font.render(winner, True, green)
    textLocation = p.Rect(SQ_SIZE * 4 + BORDER - textObj.get_width() / 2 + MENU,
                          SQ_SIZE * 4 + BORDER + TIME - textObj.get_height() / 2, 60, 60)
    screen.blit(textObj, textLocation)


def drawMoveLog(screen, gs):
    font = p.font.Font('.\Font\seguisym.ttf', 16)
    moveLogRect = p.Rect(MENU + BOARD + BORDER * 2 + 20, TIME + 10, MOVE_LOG, BORDER*2 + BOARD)
    # p.draw.rect(screen, p.Color('Black'), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + "." + moveLog[i].getChessNotation() + ", "
        if i + 1 < len(moveLog):
            moveString += moveLog[i + 1].getChessNotation() + "   "
        moveTexts.append(moveString)
    movesPerRow = 3
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ''
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]
        textObj = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObj, textLocation)
        textY += textObj.get_height() + lineSpacing
        if textY >= 677:
            break


if __name__ == "__main__":
    main()
