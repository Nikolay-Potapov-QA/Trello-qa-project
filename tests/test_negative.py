import pytest
import allure
pytestmark = [
    allure.epic("Trello API Framework"),
    allure.feature("Negative tests (Security, Validation")
]
@allure.story("Boards managing")
@allure.title("Creating board with invalid token")
@pytest.mark.negative
def test_create_board_with_invalid_token(api):
    api.token = "invalid_token_123456"
    response = api.create_board("Hacker Board")
    assert response.status_code == 401
    assert "invalid app token" in response.text.lower()

@allure.story("Boards managing")
@allure.title("Creating board with giant name")
@pytest.mark.negative
def test_create_board_with_giant_name(api):
    giant_name = "A" * 20000
    response = api.create_board(giant_name)
    assert response.status_code == 414

@allure.story("Cards managing")
@allure.title("Creating card in fake list")
@pytest.mark.negative
def test_create_card_in_fake_list(api):
    fake_list_id = "1" * 24
    response = api.create_card(fake_list_id, "Ghost Card")
    assert response.status_code == 404

