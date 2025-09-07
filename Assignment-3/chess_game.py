import chess
from chessboard import display
import time

PAWN_TABLE_ROWS = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_TABLE_ROWS = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_TABLE_ROWS = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_TABLE_ROWS = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [ 0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN_TABLE_ROWS = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [  0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

KING_MID_TABLE_ROWS = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]
]

KING_END_TABLE_ROWS = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]

def rows_to_pst(rows):
    pst = [0] * 64
    for i, row in enumerate(rows):
        rank = 7 - i
        for file in range(8):
            sq = chess.square(file, rank)
            pst[sq] = row[file]
    return pst

PAWN_PST = rows_to_pst(PAWN_TABLE_ROWS)
KNIGHT_PST = rows_to_pst(KNIGHT_TABLE_ROWS)
BISHOP_PST = rows_to_pst(BISHOP_TABLE_ROWS)
ROOK_PST = rows_to_pst(ROOK_TABLE_ROWS)
QUEEN_PST = rows_to_pst(QUEEN_TABLE_ROWS)
KING_MID_PST = rows_to_pst(KING_MID_TABLE_ROWS)
KING_END_PST = rows_to_pst(KING_END_TABLE_ROWS)

class State:
    def __init__(self, board=None, player=True):
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board
        self.player = player  # True = White's turn, False = Black's turn

    def goalTest(self):
        # Check if the game is over
        if self.board.is_checkmate():
            return not self.player  # The opponent just made a winning move
        return None

    def isTerminal(self):
        return self.board.is_game_over()

    def moveGen(self):
        # Generate next states
        children = []
        for move in self.board.legal_moves:
            new_board = self.board.copy()
            new_board.push(move)
            children.append(State(new_board, not self.player))
        return children

    def __str__(self):
        return str(self.board)

    def __eq__(self, other):
        return self.board.fen() == other.board.fen() and self.player == other.player

    def __hash__(self):
        return hash((self.board.fen(), self.player))

    # def piece_value(piece):
    #     if piece == chess.PAWN:
    #         return 100
    #     elif piece == chess.KNIGHT:
    #         return 320
    #     elif piece == chess.BISHOP:
    #         return 330
    #     elif piece == chess.ROOK:
    #         return 500
    #     elif piece == chess.QUEEN:
    #         return 900
    #     elif piece == chess.KING:
    #         return 20000

    def material_score(self) -> int:
        white_pieces = 0
        black_pieces = 0
        score = 0

        PIECE_VALUES = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

        # MATERIAL
        white_pawns = len(self.board.pieces(chess.PAWN, chess.WHITE))
        white_knights = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        white_bishops = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        white_rooks = len(self.board.pieces(chess.ROOK, chess.WHITE))
        white_queens = len(self.board.pieces(chess.QUEEN, chess.WHITE))

        #white pieces
        white_pieces = white_pawns+white_knights+white_bishops+white_rooks+white_queens
        white_score = white_pawns*PIECE_VALUES[chess.PAWN] + white_knights*PIECE_VALUES[chess.KNIGHT] + white_bishops*PIECE_VALUES[chess.BISHOP] + white_rooks*PIECE_VALUES[chess.ROOK] + white_queens*PIECE_VALUES[chess.QUEEN]

        black_pawns = len(self.board.pieces(chess.PAWN, chess.BLACK))
        black_knights = len(self.board.pieces(chess.KNIGHT, chess.BLACK))
        black_bishops = len(self.board.pieces(chess.BISHOP, chess.BLACK))
        black_rooks = len(self.board.pieces(chess.ROOK, chess.BLACK))
        black_queens = len(self.board.pieces(chess.QUEEN, chess.BLACK))

        #black pieces
        black_pieces =black_pawns+black_knights+black_bishops+black_rooks+black_queens
        black_score = black_pawns*100 + black_knights*320 + black_bishops*330 + black_rooks*500 + black_queens*900

        # adjust the piece values based on number of pawns
        #    ....
        score += white_score - black_score

        #pieces difference
        pieces_difference = white_pieces - black_pieces
        if pieces_difference > 0:
            score += pieces_difference*10

        # no pawns
        if white_pawns == 0:
            score -= 50
        if black_pawns == 0:
            score += 50

        # more number of pawns
        if white_pawns + black_pawns > 12:
            if white_queens:
                score -= white_queens*15
            if black_queens:
                score += black_queens*15

        if white_pawns+black_pawns > 14:
            if white_rooks:
                score -= white_rooks*10
            if black_rooks:
                score += black_rooks*10

        # if total pieces are less
        total_pieces = white_pieces + black_pieces
        if total_pieces <= 6:
            if (white_knights + white_bishops) < 2 and black_pawns >= 2:
                score -= 70
                if white_pawns <= 2:
                    score -=30
            if (black_knights + black_bishops) < 2 and white_pawns >= 2:
                score += 70
                if black_pawns <= 2:
                    score +=30

        # pair of bishops are benifited
        if white_bishops == 2 and black_bishops < 2 and black_knights < 2:
            score += 20
        if black_bishops == 2 and white_bishops < 2 and white_knights < 2:
            score += 20

        return score

    #checks if the game is at the ending state or not
    def is_endgame(self):
        white_queens = len(self.board.pieces(chess.QUEEN, chess.WHITE))
        black_queens = len(self.board.pieces(chess.QUEEN, chess.BLACK))
        if white_queens == 0 and black_queens == 0:
            return True

        white_minors , white_rooks = self.minor_major_count(chess.WHITE)
        black_minors, black_rooks = self.minor_major_count(chess.BLACK)

        if (white_queens > 0 and white_minors <= 1 and white_rooks == 0 and (black_minors + black_rooks) <= 1) or (black_queens > 0 and black_minors <= 1 and black_rooks == 0 and (white_minors + white_rooks) <= 1):
            return True

        return False

    # returns the minor pieces (knights, bishops) and major pieces (rooks) count
    def minor_major_count(self,color):
        minors = len(self.board.pieces(chess.BISHOP, color)) + len(self.board.pieces(chess.KNIGHT, color))
        rooks = len(self.board.pieces(chess.ROOK, color))
        return minors, rooks

    # It tells how better the piece at placed on the board
    def pieces_square_table_score(self):
        score = 0
        endgame = self.is_endgame()

        for sq, piece in self.board.piece_map().items():
            pt = piece.piece_type
            color = piece.color

            if color == chess.BLACK:
                sq = chess.square_mirror(sq)

            if pt == chess.PAWN:
                val = PAWN_PST[sq]
            elif pt == chess.KNIGHT:
                val = KNIGHT_PST[sq]
            elif pt == chess.BISHOP:
                val = BISHOP_PST[sq]
            elif pt == chess.ROOK:
                val = ROOK_PST[sq]
            elif pt == chess.QUEEN:
                val = QUEEN_PST[sq]
            elif pt == chess.KING:
                val = KING_END_PST[sq] if endgame else KING_MID_PST[sq]
            else:
                val = 0

            if color == chess.WHITE:
                score += val
            else:
                score -= val

        return score

    #number of moves can be done
    def mobility(self):
        score = 0
        b = self.board.copy()
        b.turn = chess.WHITE
        white_moves = len(list(b.legal_moves))

        b.turn = chess.BLACK
        black_moves = len(list(b.legal_moves))

        score += 2 * (white_moves - black_moves)

        return score

    # if black control the center advantage for black and vice versa
    def center_control(self):
        score = 0
        center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        for square in center_squares:
            piece = self.board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    score += 10
                else:
                    score -= 10

        return score

    # checks if the king is safe from getting attacked
    def king_safety(self):
        score = 0

        # white_king = self.board.king(chess.WHITE)
        # attackers_of_white_king = self.board.attackers(chess.BLACK, white_king)
        # if attackers_of_white_king:
        #     score -= 50 * (len(attackers_of_white_king))
        # black_king = self.board.king(chess.BLACK)
        # attackers_of_black_king = self.board.attackers(chess.WHITE, black_king)
        # if attackers_of_black_king:
        #     score += 50 * (len(attackers_of_black_king))

        # attackers
        for color in [chess.WHITE, chess.BLACK]:
            king_sq = self.board.king(color)
            if not king_sq:
                # will not enter into this
                # this mean there is no king exits
                continue

            attackers = self.board.attackers(not color, king_sq)
            if attackers:
                penalty = 50 * len(attackers)
                score += penalty if color == chess.BLACK else -penalty

            # sheilding
            # if not self.is_endgame():
            #     rank = chess.square_rank(king_sq)
            #     file = chess.square_file(king_sq)
            #     bonus = 0
            #     if color == chess.WHITE:
            #         for f in [file-1, file, file+1]:
            #             if 0<=f<=7 and rank+1<5:
            #                 sq = chess.square(f,rank)
            #                 if sq and self.board.piece_at(sq).color == chess.WHITE:
            #                     bonus += 10
            #         score += bonus
            #     elif color == chess.BLACK:
            #         for f in [file-1, file, file+1]:
            #             if 0<=f<=7 and rank-1>4:
            #                 sq = chess.square(f,rank)
            #                 if sq and self.board.piece_at(sq).color == chess.BLACK:
            #                     bonus += 10
            #         score -= bonus

        return score

    # evaluation function
    def evaluate(self):
        # Step 1: Handle finished games
        if self.board.is_checkmate():
            return -99999 if self.player else 99999  # Current player is mated
        if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.can_claim_draw():
            return 0

        score = 0

        #MATERIAL SCORE
        score += self.material_score()

        # PIECE-SQUARE TABLE SCORE
        score += self.pieces_square_table_score()

        # MOBILITY
        score += self.mobility()

        # CENTER CONTROL
        score += self.center_control()

        # KING SAFETY
        score += self.king_safety()

        # PAWN STRUCTURE
        # score += self.pawn_structure()

        # Step 2: YOUR WORK STARTS HERE
        # ------------------------------------
        # Right now we return 0 for all positions.
        # This means the AI plays randomly.
        # Replace this with your own scoring rules!
        return score
        # ------------------------------------


def minimax(state, depth, alpha, beta, maximizingPlayer, maxDepth):
    if state.isTerminal() or depth == maxDepth:
        return state.evaluate(), None

    best_move = None

    if maximizingPlayer:  # MAX node (White)
        maxEval = float('-inf')
        for child in state.moveGen():
            eval_score, _ = minimax(child, depth + 1, alpha, beta, False, maxDepth)

            if eval_score > maxEval:
                maxEval = eval_score
                best_move = child.board.peek()  # Last move made

            alpha = max(alpha, eval_score)
            if alpha >= beta:
                break  # Alpha-beta pruning

        return maxEval, best_move

    else:  # MIN node (Black)
        minEval = float('inf')
        for child in state.moveGen():
            eval_score, _ = minimax(child, depth + 1, alpha, beta, True, maxDepth)

            if eval_score < minEval:
                minEval = eval_score
                best_move = child.board.peek()

            beta = min(beta, eval_score)
            if alpha >= beta:
                break

        return minEval, best_move


def play_game():
    current_state = State(player=True)  # White starts
    maxDepth = 3  # Try experimenting with the Search depth for more inteligent ai
    game_board = display.start()  # Initialize the GUI

    print("Artificial Intelligence – Assignment 3")
    print("Simple Chess AI")
    print("You are playing as White (enter moves in UCI format, e.g., e2e4)")

    while not current_state.isTerminal():
        # Update the display
        display.update(current_state.board.fen(), game_board)

        # Check for quit event
        if display.check_for_quit():
            break

        if current_state.player:  # Human move (White)
            try:
                move_uci = input("Enter your move (e.g., e2e4, g1f3, a7a8q) or 'quit': ")

                if move_uci.lower() == 'quit':
                    break

                move = chess.Move.from_uci(move_uci)

                if move in current_state.board.legal_moves:
                    new_board = current_state.board.copy()
                    new_board.push(move)
                    current_state = State(new_board, False)
                else:
                    print("Invalid move! Try again.")
                    continue
            except ValueError:
                print("Invalid input format! Use UCI format like 'e2e4'.")
                continue
        else:  # AI move (Black)
            print("AI is thinking...")
            start_time = time.time()
            eval_score, best_move = minimax(current_state, 0, float('-inf'), float('inf'), False, maxDepth)
            end_time = time.time()

            print(f"AI thought for {end_time - start_time:.2f} seconds")

            if best_move:
                new_board = current_state.board.copy()
                new_board.push(best_move)
                current_state = State(new_board, True)
                print(f"AI plays: {best_move.uci()}")
            else:
                # Fallback
                legal_moves = list(current_state.board.legal_moves)
                if legal_moves:
                    move = legal_moves[0]
                    new_board = current_state.board.copy()
                    new_board.push(move)
                    current_state = State(new_board, True)
                    print(f"AI plays (fallback): {move.uci()}")
                else:
                    break

    # Game over
    print("\nGame over!")
    display.update(current_state.board.fen(), game_board)

    if current_state.board.is_checkmate():
        print("Checkmate! " + ("White" if not current_state.player else "Black") + " wins!")
    elif current_state.board.is_stalemate():
        print("Stalemate! It's a draw.")
    elif current_state.board.is_insufficient_material():
        print("Insufficient material! It's a draw.")
    elif current_state.board.can_claim_draw():
        print("Draw by repetition or 50-move rule!")

    # Keep the window open for a moment
    time.sleep(3)
    display.terminate()


if __name__ == "__main__":
    play_game()