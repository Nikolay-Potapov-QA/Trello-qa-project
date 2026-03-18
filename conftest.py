import pytest
from api_client import TrelloClient
from faker import Faker
fake = Faker()
@pytest.fixture
def api():
    return TrelloClient()

@pytest.fixture
def test_board(api):
    board_name = f"AQA_Board{fake.word()}"
    response = api.create_board(board_name)
    board_id = response.json()["id"]
    print(f"\n[SETUP] Temporary board created: {board_id}")

    yield board_id
    print(f"\n[TEARDOWN] Deleting temporary board: {board_id}")
    api.delete_board(board_id)


@pytest.fixture
def test_list(api, test_board):
    board_id = test_board
    list_name = f"AQA_List_{fake.word()}"
    response = api.create_list(list_name, board_id)
    list_data = response.json()
    list_id = list_data["id"]
    yield list_id

@pytest.fixture
def test_card(api, test_list):
    list_id = test_list
    card_name = f"AQA_Card_{fake.word()}"
    response = api.create_card(list_id, card_name)
    card_id = response.json()["id"]
    print(f"\n[SETUP] Temporary card created: {card_id}")
    yield {"card_id": card_id, "list_id": list_id}



