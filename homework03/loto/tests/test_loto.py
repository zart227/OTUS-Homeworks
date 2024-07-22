import pytest
from unittest.mock import patch
from loto.loto import Card, Player, Game


def test_card_generation():
    card = Card()
    numbers = [num for row in card.grid for num in row if num != "-"]
    assert len(numbers) == 15
    assert len(card.grid) == 3
    for row in card.grid:
        assert len(row) == 9


def test_mark_number():
    card = Card()
    number = card.grid[0][0]
    assert card.mark_number(number) == True
    assert card.grid[0][0] == "-"


def test_player_has_won():
    player = Player("Test")
    for row in player.card.grid:
        for i in range(len(row)):
            row[i] = "-"
    assert player.has_won() == True


def test_game_initialization():
    players = [Player("Player1"), Player("Player2", is_computer=True)]
    game = Game(players)
    assert len(game.players) == 2
    assert len(game.barrels) == 90


@patch("builtins.input", side_effect=["y", "y"])
@patch(
    "random.sample", return_value=[49, 30, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
)
@patch(
    "random.shuffle", lambda x: None
)  # Prevent shuffling to ensure predictable order
def test_game_play(mock_input, mock_sample, capsys):
    players = [Player("Player1"), Player("Player2", is_computer=True)]
    game = Game(players)
    game.play()
    captured = capsys.readouterr()
    assert "Let's play Lotto!" in captured.out
    assert "Цифры 90 нет на вашей карточке. Вы проиграли!" in captured.out
