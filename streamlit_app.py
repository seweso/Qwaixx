import streamlit as st
import random
import time

class GameEngine:
    def __init__(self):
        self.players = [HumanPlayer("Alice"), AiPlayer("AI Bot")]
        self.current_player_index = 0
        self.qwixx_dice = Dice()
        self.score_card = ScoreCard()  # Create a single score card for the game

    def switch_to_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def make_move(self):
        current_player = self.players[self.current_player_index]
        self.qwixx_dice.roll()
        st.write(f"{current_player.name} turn")
        st.write(f"Dice result: {self.qwixx_dice.format_results()}")
        selections = current_player.get_selections(self.qwixx_dice, self.score_card)
        self.display_score_card(self.score_card)
        current_player.make_move(self.qwixx_dice, self.score_card, selections)
        self.switch_to_next_player()

    def display_score_card(self, score_card):
        st.write("Current Score card:")
        st.text(score_card.format_results())
        total_score = score_card.calculate_total_score()
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

    def calculate_total_score(self):
        total_score = 0
        for color, numbers in self.score_card.items():
            for number in numbers:
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

    def get_selections(self, dice_results, score_card):
        pass

class HumanPlayer(Player):
    def make_move(self, dice_results, score_card, selections):
        pass

    def get_selections(self, dice_results, score_card):
        st.write(f"Make your selections (e.g., R4,B12):")
        user_selections = st.text_input("Selections:")
        return user_selections

class AiPlayer(Player):
    def make_move(self, dice_results, score_card, selections):
        time.sleep(1)

        # AI player's selections
        ai_selections = self.get_selections(dice_results, score_card)

        # Update the score card with AI's selections
        for selection in ai_selections:
            color, number = selection[0], int(selection[1])
            score_card.add_selection(color, number)

    def get_selections(self, dice_results, score_card):
        selections = []

        for result in dice_results.results:
            color, number = result[0], int(result[1])
            if f"{color}{number}" in score_card.get_score_card():
                selections.append(f"{color}{number}")

        if not selections:
            for color in ['R', 'Y', 'G', 'B']:
                if color in score_card.get_score_card():
                    for i in range(2, 13):
                        if f"{color}{i}" not in selections:
                            selections.append(f"{color}{i}")
                            break

        return selections


class Dice:
    def __init__(self):
        self.colors = ['R', 'Y', 'G', 'B', 'W', 'W']
        self.results = []

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
