import streamlit as st
import random
import time

class GameEngine:
    def __init__(self):
        self.players = [HumanPlayer("Alice"), AiPlayer("AI Bot")]
        self.current_player_index = 0
        self.qwixx_dice = Dice()
        self.score_cards = {player.name: ScoreCard() for player in self.players}

    def switch_to_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    @st.cache(suppress_st_warning=True)
    def make_move(self):
        current_player = self.players[self.current_player_index]
        self.qwixx_dice.roll()  # Roll dice before displaying the turn
        st.write(f"{current_player.name} turn")
        st.write(f"Dice result: {self.qwixx_dice.format_results()}")
        selections = current_player.get_selections()
        self.display_score_card(current_player.name, selections)
        current_player.make_move(self.qwixx_dice, self.score_cards[current_player.name], selections)
        self.switch_to_next_player()

    def display_score_card(self, player_name, selections):
        score_card = self.score_cards[player_name]
        st.write(f"Current Score card for {player_name}:\n{score_card.format_results()}")
        total_score = score_card.calculate_score(selections)
        st.write(f"Total Score: {total_score}")

class ScoreCard:
    def __init__(self):
        self.score_card = {
            'R': [], 'Y': [], 'G': [], 'B': []
        }

    def get_score_card(self):
        return self.score_card

    def format_results(self):
        result = []
        for color in ['R', 'Y', 'G', 'B']:
            numbers = self.score_card.get(color, [])
            if not numbers:
                result.append(f"{color}:")
            else:
                bonus = "B" if len(numbers) >= 5 and 12 in numbers else ""
                result.append(f"{color}:{','.join(map(str, numbers))}{bonus}")
        return '\n'.join(result)

    @st.cache(suppress_st_warning=True)
    def calculate_score(self, selections):
        total_score = 0
        for color, numbers in self.score_card.items():
            for number in numbers:
                if f"{color}{number}" in selections:
                    total_score += number
        return total_score

    def add_selection(self, color, number):
        if color in self.score_card:
            self.score_card[color].append(number)

class Player:
    def __init__(self, name):
        self.name = name

    def make_move(self, dice_results, score_card, selections):
        pass

    def get_selections(self):
        pass

class HumanPlayer(Player):
    def make_move(self, dice_results, score_card, selections):
        pass

    def get_selections(self):
        st.write(f"Make your selections (e.g., R4,B12):")
        user_selections = st.text_input("Selections:")
        selections = user_selections.split(',')
        return selections

class AiPlayer(Player):
    def make_move(self, dice_results, score_card, selections):
        time.sleep(1)

    def get_selections(self):
        return []

class Dice:
    def __init__(self):
        self.colors = ['R', 'Y', 'G', 'B', 'W', 'W']
        self.results = []

    @st.cache(suppress_st_warning=True)
    def roll(self):
        self.results = [f"{color}{random.randint(1, 6)}" for color in self.colors]

    def format_results(self):
        return ' '.join(self.results)

# Streamlit app
st.title("Qwixx Game Simulator")

if "game_engine" not in st.session_state:
    st.session_state.game_engine = GameEngine()

game_engine = st.session_state.game_engine

if st.button("Next Turn"):
    game_engine.make_move()
