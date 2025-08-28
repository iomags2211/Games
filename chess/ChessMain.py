"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
from chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR",
        "bp", "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]
    for piece in pieces:    
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        if len(playerClicks) == 0 and gs.board[row][col] == '--':
                            pass
                        else:
                            playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for validMove in validMoves:    
                            if move == validMove:
                                gs.makeMove(validMove)
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins!")
            else:
                drawText(screen, "White wins!")
        elif gs.stalemate:
            gameOver = True
            drawText(screen, "Stalemate.")

        clock.tick(MAX_FPS)
        p.display.flip()


def drawText(screen, text):
    font = p.font.SysFont('Helvetica', 32, True, False)
    textObj = font.render(text, 0, p.Color('Gray'))
    textLoc = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObj.get_width()/2, HEIGHT/2 - textObj.get_height()/2)
    shadowObj = font.render(text, 0, p.Color('Black'))
    shadowLoc = textLoc.move(2, 2)
    screen.blit(textObj, textLoc)
    screen.blit(shadowObj, shadowLoc)


def highlightSquares(screen, gs, validMoves, sqSelected):
    s = p.Surface((SQ_SIZE, SQ_SIZE))
    s.set_alpha(100)
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
    if gs.inCheck():
        s.fill(p.Color('red'))
        if gs.whiteToMove:
            screen.blit(s, (gs.whiteKingLocation[1]*SQ_SIZE, gs.whiteKingLocation[0]*SQ_SIZE))
        else:
            screen.blit(s, (gs.blackKingLocation[1]*SQ_SIZE, gs.blackKingLocation[0]*SQ_SIZE))


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()