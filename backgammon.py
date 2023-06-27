import random
from typing import Any
from classes.stone import Stone
from classes.home import Home
from classes.double_dice import DoubleDice
from classes.human_player import HumanPlayer
from classes.ai_player import AIPlayer
from classes.player import Player
from classes.spike import Spike
import json


# TODO: bíly hráč začíná jako první


NUMBER_OF_STONES = 15
NUMBER_OF_SPIKES = 24
PLAYERS_ATRB = [["white", -1, 25, 0, range(1, 6+1)], ["black", 1, 0, 25, range(19, 24+1)]]


def main():
    opponent = None

    user_input = input("Load a game -> 'vrhcaby.json' | new game -> 'new game': ")
    while user_input not in ['vrhcaby.json', 'new game']:
        user_input = input("Wrong input try: 'vrhcaby.json' for load or 'new game' for a new game: ")

    if user_input == 'new game':
        opponent_type = input("Play against ai or human: ")
        while opponent_type.lower() not in ['human', 'ai']:
            opponent_type = input("Wrong input: ai or human: ")

        if opponent_type == 'human':
            opponent = HumanPlayer(*PLAYERS_ATRB.pop(random.randrange(len(PLAYERS_ATRB))))
        else:
            opponent = AIPlayer(*PLAYERS_ATRB.pop(random.randrange(len(PLAYERS_ATRB))))
        
        player = AIPlayer(*PLAYERS_ATRB.pop())
        game = Game([player, opponent])
    else:

        data = json.load(open('vrhcaby.json'))
        players = []
        for player in data['players']:
            new_player = None
            player_atrb = PLAYERS_ATRB[0] if player['color'] == 'white' else PLAYERS_ATRB[-1]
            if player['player_type'] == 'HumanPlayer':
                new_player = HumanPlayer(*player_atrb, player['stones_kicked'])
            else:
                new_player = AIPlayer(*player_atrb, player['stones_kicked'])
            for _ in range(player['bar_size']):
                new_player.bar.push_stone(Stone(player["color"], "bar", ["bar"]))
            players.append(new_player)
        game = Game(players, data['list_of_stones'], data['current_player'], data['remaining_moves'], data["double_dice_roll"])


class Game: 
    def __init__(self, players: list, list_of_stones=[], current_player=0, load_remaining_moves=[], double_dice_roll=[]) -> None:
        self._game_board = GameBoard()
        self._game_board.create_stones(list_of_stones)
        self._dvojkostka = DoubleDice()
        self._double_dice_roll = double_dice_roll
        self._players = players
        self._current_player = current_player
        self._game_is_running = True
        self.game_on(load_remaining_moves)

    def game_on(self, load_remaining_moves=[]) -> None:
        if len(load_remaining_moves) != 0:
            self.finish_turn(load_remaining_moves, self._players[self._current_player])
        while self._game_is_running:
            remaining_moves = self.beginning_of_turn()
            self.finish_turn(remaining_moves, self._players[self._current_player])
        else:
            self.show_statistics(self._players, self._game_board.board)

    def finish_turn(self, remaining_moves: list, curr_player: Player) -> None:
        legal_moves = self.get_legal_moves(remaining_moves, curr_player)

        while len(remaining_moves) != 0 and self._game_is_running:

            self.game_output(curr_player, self._players[self.next_player()], remaining_moves, legal_moves)
            
            if not any(legal_moves.values()):
                print("NO MOVE AVAILABLE")
                break
            
            # str, str, list[int, int]
            move = curr_player.play_move(legal_moves)

            if move == "save":
                self.save_game(self._game_board.board, self._players, self._current_player, remaining_moves, self._double_dice_roll)
                while move == "save":
                    print("GAME SAVED")
                    move = curr_player.play_move(legal_moves)
            if move == "exit":
                self._game_is_running = False
                break
            
            current_position, new_position = move
            distance = new_position - current_position
            if distance in remaining_moves:
                self._game_board.move_stone(current_position, new_position, curr_player, self._players[self.next_player()])
                remaining_moves.remove(distance)
            else:
                if len(set(remaining_moves)) == 1:
                    iteration = distance / remaining_moves[0]
                    while iteration > 0 and any(legal_moves.values()):
                        new_position = self.vrat_novou_pozici(legal_moves, current_position)
                        self._game_board.move_stone(current_position, new_position, curr_player, self._players[self.next_player()])
                        remaining_moves.remove(new_position - current_position)
                        current_position = new_position
                        legal_moves = self.get_legal_moves(remaining_moves, curr_player)
                        iteration -= 1
                else:
                    while len(remaining_moves) != 0 and any(legal_moves.values()):
                        new_position = self.vrat_novou_pozici(legal_moves, current_position)
                        self._game_board.move_stone(current_position, new_position, curr_player, self._players[self.next_player()])
                        remaining_moves.remove(new_position - current_position)
                        current_position = new_position
                        legal_moves = self.get_legal_moves(remaining_moves, curr_player)
                
            legal_moves = self.get_legal_moves(remaining_moves, curr_player)
            #self.game_output(curr_player, self._players[self.next_player()], remaining_moves, legal_moves) 

            self.check_win(self._game_board.board, curr_player, self._players[self.next_player()])

        self._current_player = self.next_player()

    def beginning_of_turn(self) -> None:    
        curr_player = self._players[self._current_player]
        self._double_dice_roll = self._dvojkostka.throw_double_dice()
        remaining_moves = [i * curr_player.move_direction for i in self._double_dice_roll]
        #legal_moves = self.get_legal_moves(remaining_moves, curr_player)
        #self.game_output(curr_player, self._players[self.next_player()], remaining_moves, legal_moves)
        return remaining_moves

    def game_output(self, player: Player, opponent: Player, remaining_moves: list, legal_moves: dict) -> None:
        print("---------------------------------------------------------")
        print(f"{opponent} {opponent.bar}")
        print(self._game_board)
        print(f"{player} {player.bar}")
        print("--------------")
        print(f"It's {player}'s turn")
        print(f"Numbers on dice: {self._double_dice_roll}, ramaining moves: {[abs(x) for x in remaining_moves]}")
        print(f"Legal moves: {legal_moves}")
        print("---------------------------------------------------------")

    def show_statistics(self, players: list, board: list):
        print("---------------------------------------------------------")
        print("STATISTICS")
        for player in players:
            print(f"Player's color: {player}")
            print(f"Stones kicked: {player.stones_kicked}")
            print(f"Stones in home: {board[player.home_index].size()}")
            print(f"Abandoned stones: {NUMBER_OF_STONES - board[player.home_index].size()}")
            print("--------------")
        print("---------------------------------------------------------")
        exit_game = input("To quit game write 'exit': ")
        while exit_game != "exit":
            exit_game = input("To quit game write 'exit': ")

    def check_win(self, board: list, player: Player, opponent: Player):
        if board[player.home_index].size() == NUMBER_OF_STONES:
            self._game_is_running = False
            s = f"PLAYER {player.color} HAS WON. TYPE OF WIN: "
            if board[opponent.home_index].is_empty() and opponent.bar.size() > 0:
                s += "BACKGAMMON"
            elif board[opponent.home_index].is_empty():
                s += "GAMMON"
            else:
                s += "COMMON WIN"
            print(s)

    def save_game(self, spikes: list, players: list, current_player: int, remaining_moves: list, double_dice_roll: list):
        list_of_stones = []
        for spike in spikes:
            for stone in spike.stones:
                list_of_stones.append({
                    "color": stone.color,
                    "history": stone.history
                })

        players_to_save = []
        for player in players:
            players_to_save.append({
                "color": player.color,
                "stones_kicked": player.stones_kicked,
                "bar_size": player.bar.size(),
                "player_type": "HumanPlayer" if isinstance(player, HumanPlayer) else "AIPlayer" 
            })
                    
        dict_to_save = {
            "current_player": current_player,
            "remaining_moves": remaining_moves,
            "double_dice_roll": double_dice_roll,
            "players": players_to_save,
            "list_of_stones": list_of_stones
        }
    
        with open("vrhcaby.json", "w") as soubor:
            json.dump(dict_to_save, soubor, indent=4)

    def next_player(self):
        return (self._current_player + 1) % len(self._players)

    def get_legal_moves(self, remaining_moves: list, player: Player) -> dict:
        return self._game_board.get_legal_moves(remaining_moves, player)
          
    def vrat_novou_pozici(self, legal_moves: dict, aktualni_pozice: int) -> Any:
        if aktualni_pozice in [0, 25]:
            aktualni_pozice = "bar"
        return legal_moves.get(aktualni_pozice)[0]


class GameBoard:
    def __init__(self) -> None:
        self._board = self.create_spikes()

    @property
    def board(self) -> list:
        return self._board

    def create_spikes(self) -> list:
        spikes = []
        spikes.append(Home(0, 15))
        for i in range(1, NUMBER_OF_SPIKES+1):
            spikes.append(Spike(i))
        spikes.append(Home(25, 15))
        return spikes

    def create_stones(self, loaded_stones: list) -> None:
        if len(loaded_stones) == 0:
            startng_pos_of_stones = [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0, 0]
            for i in range(len(startng_pos_of_stones)):
                for _ in range(startng_pos_of_stones[i]):
                        self._board[i].push_stone(Stone("black", i, []))
                        # print(self._board[i].get_stone().history)
                        self._board[len(startng_pos_of_stones) - i - 1].push_stone(Stone("white", len(startng_pos_of_stones) - i - 1, []))
        else:
            for stone in loaded_stones:
                color = stone['color']
                history = stone['history']
                position = history[-1]
                self._board[position].push_stone(Stone(color, position, history))
   
    def move_stone(self, current_position: int, new_position: int, player: Player, opponent: Player) -> None:
        stone = None
        if current_position == player.bar.index:
            stone = player.bar.pop_stone()
            stone.delete_history()
        else:
            stone = self._board[current_position].pop_stone()

        if self.can_kick_stone(stone.color, new_position):
            self.kick_stone(new_position, opponent)

        self._board[new_position].push_stone(stone)
        stone.add_positon_to_history(new_position)    
        print(f"STONE MOVED FROM {current_position} TO {new_position}")

    def get_legal_moves(self, list_of_moves: list, player: Player) -> dict:
        valid_moves = {}
        if player.bar.size() > 0:
            valid_moves["bar"] = self.calculate_legal_moves(player.bar.index, list_of_moves, player)
        else:
            for spike in self._board[1:-1]:
                if spike.size() >= 1:
                    if spike.get_stone().color == player.color:
                        moves = self.calculate_legal_moves(spike.index, list_of_moves, player)
                        if len(moves) != 0:
                            valid_moves[spike.index] = moves
        return valid_moves
    
    def calculate_legal_moves(self, spike_index: int, list_of_moves: list, player: Player) -> list:
        possible_moves = [] 
        if len(set(list_of_moves)) == 1:                                           
            moves = [x * list_of_moves[0] for x in range(1, len(list_of_moves)+1)]
            for move in moves:
                if self.is_valid_move(spike_index + move, player):
                    possible_moves.append(spike_index + move)
                else:
                    break
        else:
            for move in list_of_moves:
                if self.is_valid_move(spike_index + move, player):
                    possible_moves.append(spike_index + move)
            if len(possible_moves) != 0:
                if self.is_valid_move(spike_index + sum(list_of_moves), player):
                    possible_moves.append(spike_index + sum(list_of_moves))
        return possible_moves

    def is_valid_move(self, stone_to: int, player: Player) -> bool:
        if stone_to < 0 or stone_to > len(self._board) - 1:
            return False
        if stone_to == player.home_index and self.can_go_home(player):
            return True
        elif not stone_to in [0, 25]:
            second_spike = self._board[stone_to]
            return second_spike.size() <= 1 or (player.color == second_spike.get_stone().color and second_spike.size() < 5)

    def can_go_home(self, player: Player) -> bool:
        for spike in self._board[1:-1]:
            if not spike.is_empty():
                if spike.get_stone().color == player.color:
                    if spike.index not in player.home_board:
                        return False
        return True

    def can_kick_stone(self, stone_color: str, stone_to: int) -> bool:
        second_spike = self._board[stone_to]
        return second_spike.size() == 1 and stone_color != second_spike.get_stone().color

    def kick_stone(self, position: int, player: Player) -> None:
        stone = self._board[position].pop_stone()
        player.bar.push_stone(stone)
        player.increase_number_of_stones_kicked()
        stone.add_positon_to_history("bar")
        print("STONE WAS MOVED TO BAR")

    def __str__(self) -> str:
        return "\n".join(str(spike) for spike in self._board)


if __name__ == "__main__":
    main()