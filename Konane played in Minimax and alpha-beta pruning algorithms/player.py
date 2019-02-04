import game_rules, random
from copy import deepcopy
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board, symbol):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


class MinimaxPlayer(Player):
    def __init__(self, symbol, depth):
        super(MinimaxPlayer, self).__init__(symbol)
        self.depth = depth

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        return self.minimax_decision(legalMoves, board)

    def makeMove(self, board, move):
        return self.makePlayerMove(board, game_rules.pieceAt(board, move[0]), move)

    def makePlayerMove(self, board, player, move):
        newBoard = deepcopy(board)
        for jump in game_rules.interpolateMove(move):
            game_rules._makeJump(newBoard, jump)
        return newBoard

    def get_opponent_symbol(self, symbol):
        return 'o' if symbol == 'x' else 'x'

    def minimax_decision(self, legalMoves, board):
        selected_move = None
        max_v = NEG_INF
        for move in legalMoves:
            v = self.min_value(self.makeMove(board, move), self.depth)
            if v > max_v:
                max_v = v
                selected_move = move
        return selected_move

    def max_value(self, board, depth):
        depth -= 1
        if depth == 0:
            return self.h1(board, self.symbol)
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) == 0:
            return self.h1(board, self.symbol)

        v = NEG_INF
        for move in legalMoves:
            v = max(v, self.min_value(self.makeMove(board, move), depth))
        return v

    def min_value(self, board, depth):
        depth -= 1
        if depth == 0:
            return self.h1(board, self.symbol)
        opponent_symbol = self.get_opponent_symbol(self.symbol)
        legalMoves = game_rules.getLegalMoves(board, opponent_symbol)
        if len(legalMoves) == 0:
            return self.h1(board, self.symbol)

        v = POS_INF
        for move in legalMoves:
            v = min(v, self.max_value(self.makeMove(board, move), depth))
        return v


class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth):
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.depth = depth

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        return self.alpha_beta_search(legalMoves, board)

    def makeMove(self, board, move):
        return self.makePlayerMove(board, game_rules.pieceAt(board, move[0]), move)

    def makePlayerMove(self, board, player, move):
        newBoard = deepcopy(board)
        for jump in game_rules.interpolateMove(move):
            game_rules._makeJump(newBoard, jump)
        return newBoard

    def alpha_beta_search(self, legalMoves, board):
        selected_move = None
        max_v = NEG_INF
        for move in legalMoves:
            v = self.min_value(self.makeMove(board, move), NEG_INF, POS_INF, self.depth)
            if v > max_v:
                max_v = v
                selected_move = move
        return selected_move

    def get_opponent_symbol(self, symbol):
        return 'o' if symbol == 'x' else 'x'

    def max_value(self, board, alpha, beta, depth):
        depth -= 1
        if depth == 0:
            return self.h1(board, self.symbol)
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) == 0:
            return self.h1(board, self.symbol)

        v = NEG_INF
        for move in legalMoves:
            v = max(v, self.min_value(self.makeMove(board, move), alpha, beta, depth))
            if v >= beta: return v
            alpha = max(alpha, v)
        return v

    def min_value(self, board, alpha, beta, depth):
        depth -= 1
        if depth == 0:
            return self.h1(board, self.symbol)
        opponent_symbol = self.get_opponent_symbol(self.symbol)
        legalMoves = game_rules.getLegalMoves(board, opponent_symbol)
        if len(legalMoves) == 0:
            return self.h1(board, self.symbol)

        v = POS_INF
        for move in legalMoves:
            v = min(v, self.max_value(self.makeMove(board, move), alpha, beta, depth))
            if v <= alpha: return v
            beta = min(beta, v)
        return v


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)
