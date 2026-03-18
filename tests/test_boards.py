import pytest
from models import BoardModel, CardModel, ListModel
from faker import Faker
import allure
pytestmark = [
    allure.epic("Trello API Framework"),
    allure.feature("Positive tests (Boards, Lists, Cards")
]

fake = Faker()
@allure.story("Boards managing")
@allure.title("Creating new board")
def test_create_new_board(api):
    response = api.create_board("My Favorite Porn Models")
    assert response.status_code == 200
    data = response.json()
    validated_board = BoardModel(**data)
    assert validated_board.name == data["name"]
    assert validated_board.closed == False

@allure.story("Cards managing")
@allure.title("Creating new card")
def test_create_card(api, test_list):
    list_id = test_list
    card_name = fake.word()
    response = api.create_card(list_id, card_name)
    assert response.status_code == 200
    data = response.json()
    validated_card = CardModel(**data)
    assert validated_card.name == card_name
    assert validated_card.idList == list_id

@allure.story("Lists managing")
@allure.title("Creating new list")
def test_create_list(api, test_board):
    board_id = test_board
    list_name = fake.word()
    response = api.create_list(list_name, board_id)
    assert response.status_code == 200
    data = response.json()
    validated_list = ListModel(**data)
    assert validated_list.name == list_name

@allure.story("Boards managing")
@allure.title("Deleting new board")
def test_delete_board(api, test_board):
    board_id = test_board
    response = api.delete_board(board_id)
    assert response.status_code == 200
@allure.story("E2E test")
@allure.title("E2E test")
def test_e2e_workflow(api, test_board):
    board_id = test_board
    response_list = api.create_list("To do", board_id)
    list_id = response_list.json()["id"]
    response_card = api.create_card(list_id, "Play basketball")
    assert response_card.status_code == 200

@allure.story("Boards managing")
@allure.title("Creating colored boards")
@pytest.mark.parametrize("color", [
    "red",
    "green",
    "blue"
])
def test_create_colored_boards(api, color):
    response = api.create_board(board_name="Color Test", prefs_background=color)
    assert response.status_code == 200
    data = response.json()
    assert data["prefs"]["background"] == color
    api.delete_board(data["id"])

@allure.story("Boards managing")
@allure.title("Archiving cards")
def test_archive_card(api, test_card):
    card_id = test_card["card_id"]
    response = api.archive_card(card_id)
    assert response.status_code == 200
    data = response.json()
    assert data["closed"] == True

@allure.story("Boards managing")
@allure.title("Creating board with pydantic validation")
def test_create_board_pydantic_validation(api):
    response = api.create_board(board_name="Pydantic")
    assert response.status_code == 200
    board_data = response.json()
    valid_board = BoardModel(**board_data)
    assert valid_board.name == board_data["name"]
    api.delete_board(valid_board.id)

@allure.story("Cards managing")
@allure.title("Updating card")
def test_update_card(api, test_card):
    card_id = test_card["card_id"]
    new_name = "Fuck you??"
    response = api.update_card(card_id, name=new_name)
    assert response.status_code == 200
    response_data = response.json()
    valid_card = CardModel(**response_data)
    assert valid_card.name == new_name

@allure.story("Cards managing")
@allure.title("Creating checklist and item")
def test_create_checklist_and_item(api, test_card):
    card_id = test_card["card_id"]
    checklist_name = "Fuckable porn models"
    item_name = "Nicole Aniston"
    response_cl = api.create_checklist(card_id, checklist_name)
    assert response_cl.status_code == 200
    cl_id = response_cl.json()["id"]
    response_item = api.create_checkitem(cl_id, item_name)
    assert response_item.status_code == 200
    it_response = response_item.json()
    assert it_response["name"] == item_name

