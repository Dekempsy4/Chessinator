import IPython.display
import chess
import chess.svg

from IPython.display import SVG, display


ptable = [0, 0, 0, 0, 0, 0, 0, 0,5, 10, 10, -20, -20, 10, 10, 5,5, -5, -10, 0, 0, -10, -5, 5,0, 0, 0, 20, 20, 0, 0, 0,5, 5, 10, 25, 25, 10, 5, 5,10, 10, 20, 30, 30, 20, 10, 10,50, 50, 50, 50, 50, 50, 50, 50,0, 0, 0, 0, 0, 0, 0, 0]

ktable = [-50, -40, -30, -30, -30, -30, -40, -50,-40, -20, 0, 5, 5, 0, -20, -40,-30, 5, 10, 15, 15, 10, 5, -30,-30, 0, 15, 20, 20, 15, 0, -30,-30, 5, 15, 20, 20, 15, 5, -30,-30, 0, 10, 15, 15, 10, 0, -30,-40, -20, 0, 0, 0, 0, -20, -40,-50, -40, -30, -30, -30, -30, -40, -50]

btable = [-20, -10, -10, -10, -10, -10, -10, -20,-10, 5, 0, 0, 0, 0, 5, -10,-10, 10, 10, 10, 10, 10, 10, -10,-10, 0, 10, 10, 10, 10, 0, -10,-10, 5, 5, 10, 10, 5, 5, -10,-10, 0, 5, 10, 10, 5, 0, -10,-10, 0, 0, 0, 0, 0, 0, -10,-20, -10, -10, -10, -10, -10, -10, -20]

rtable = [0, 0, 0, 5, 5, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,5, 10, 10, 10, 10, 10, 10, 5,0, 0, 0, 0, 0, 0, 0, 0]

qtable = [-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 0, 0, 0, 5, 0, -10,-10, 0, 5, 5, 5, 5, 5, -10,-5, 0, 5, 5, 5, 5, 0, 0, -5, 0, 5, 5, 5, 5, 0, -5, -10, 0, 5, 5, 5, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10, -10, -5, -5, -10, -10, -20]

kmtable = [20, 30, 10, 0, 0, 10, 30, 20, 20, 20, 0, 0, 0, 0, 20, 20, -10, -20, -20, -20, -20, -20, -20, -10, -20, -30, -30, -40, -40, -30, -30, -20, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30]

board = chess.Board()


def evalPos():
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    wPawn = len(board.pieces(chess.PAWN, chess.WHITE))
    bPawn = len(board.pieces(chess.PAWN, chess.BLACK))
    wKnight = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bKnight = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wBishop = len(board.pieces(chess.BISHOP, chess.WHITE))
    bBishop = len(board.pieces(chess.BISHOP, chess.BLACK))
    wRook = len(board.pieces(chess.ROOK, chess.WHITE))
    bRook = len(board.pieces(chess.ROOK, chess.BLACK))
    wQueen = len(board.pieces(chess.QUEEN, chess.WHITE))
    bQueen = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100*(wPawn - bPawn) + 320*(wKnight - bKnight) + 330*(wBishop-bBishop) + 500*(wRook - bRook) + 900*(wQueen - bQueen)

    pawnsq = sum(ptable[i] for i in board.pieces(chess.PAWN, chess.WHITE))
    pawnsq = pawnsq + sum([-ptable[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])

    knightsq = sum([ktable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-ktable[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])

    bishopsq = sum(btable[i] for i in board.pieces(chess.BISHOP, chess.WHITE))
    bishopsq = bishopsq + sum([-btable[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])

    rooksq = sum([rtable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rtable[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])

    queensq = sum([qtable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-qtable[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])

    kingmiddlesq = sum([kmtable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingmiddlesq = kingmiddlesq + sum([-kmtable[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])

    evaluation = material + kingmiddlesq + queensq + rooksq + bishopsq + knightsq + pawnsq

    if board.turn:
        return evaluation
    else:
        return -evaluation


def alphabeta(alpha, beta, depth):
    bestscore = -9999
    if (depth == 0):
        return quisesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depth - 1)
        board.pop()
        if (score >= beta):
            return score
        if (score >= bestscore):
            bestscore = score
        if (score >= alpha):
            alpha = score
    return bestscore

def quisesce(alpha, beta):
    standPat = evalPos()
    if (standPat >= beta):
        return beta
    if (alpha < standPat):
        alpha = standPat
    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quisesce(-beta, -alpha)
            board.pop()
            if(score >= beta):
                return beta
            if(score > alpha):
                alpha = score
    return alpha

def playerMove(color):
    isplayermove = True
    while isplayermove:
        inputMove = input("type move\n")
        try:
            if (board.is_legal(chess.Move.from_uci(inputMove))):
                board.push(chess.Move.from_uci(inputMove))
                # print(board)
                if color:
                    display(SVG(chess.svg.board(board=board,size=400)))
                else:
                    display(SVG(chess.svg.board(board=board, orientation=chess.BLACK, size=400)))
                print(board.fen())
                isplayermove = False
            else:
                print("not legal move")
        except:
            print("invalid move format")

def computerMove(color, depth):
    print("chessinator's turn. He is thinking...")
    alpha = -100000
    beta = 100000
    bestMove = chess.Move.null()
    bestScore = -99999
    for move in board.legal_moves:
        board.push(move)
        eval = -alphabeta(-beta, -alpha, depth - 1)
        if (eval > bestScore):
            bestScore = eval
            bestMove = move
        if (eval > alpha):
            alpha = eval
        board.pop()
    print("chessinator has decided on: ")
    print(bestMove)
    board.push(bestMove)
    # print(board)
    if color:
        display(SVG(chess.svg.board(board=board,size=400)))
    else:
        display(SVG(chess.svg.board(board=board, orientation=chess.BLACK, size=400)))

def playGame():
    gameOver = False
    print("chessinator activated!")
    display(SVG(chess.svg.board(board=board, size=400)))
    SVG(chess.svg.board(board=board, size=400))
    player = input("type 'w' to play white and 'b' to play black. Or type 'f' to input fen \n")
    if player == "w":
        while(not gameOver):
            if board.turn:
                playerMove(True)
                print("\n\n")
            else:
                computerMove(True, 4)
                print("\n\n")
    elif player == "b":
        while(not gameOver):
            if not board.turn:
                playerMove(True)
                print("\n\n")
            else:
                computerMove(True, 4)
                print("\n\n")
    elif player == 'f':
        fen = input("type fen\n")
        board.set_fen(fen)
        playGame()
    else:
        print("bad input try again")
        playGame()


playGame()
