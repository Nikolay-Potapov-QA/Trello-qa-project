import requests
import os
from dotenv import load_dotenv
import allure
import json
load_dotenv()

class TrelloClient:
    def __init__(self):
        self.base_url = "https://api.trello.com/1"
        self.api_key = os.getenv("TRELLO_API_KEY")
        self.token = os.getenv("TRELLO_TOKEN")

        if not self.api_key or not self.token:
            raise ValueError ("Keys have not been set, check .env file")

    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        params = kwargs.pop("params", {})

        params["key"] = self.api_key
        params["token"] = self.token
        with allure.step(f"API Request: {method} {endpoint}"):
            safe_params = params.copy()
            safe_params["key"] = "***HIDDEN***"
            safe_params["token"] = "***HIDDEN***"
            allure.attach(
                json.dumps(safe_params, indent=4),
                name = "Request Params",
                attachment_type=allure.attachment_type.JSON,
            )
            response = requests.request(method, url, params=params, **kwargs)
            allure.attach(
                response.text,
                name = "Response Body",
                attachment_type=allure.attachment_type.JSON
            )
            return response

    def create_board(self, board_name, **kwargs):
        params = {"name": board_name}
        params.update(kwargs)
        return self._make_request("POST", "/boards", params=params)

    def create_list(self,name,idBoard):
        return self._make_request("POST", "/lists", params={"name":name, "idBoard":idBoard})

    def get_card(self, card_id):
        return self._make_request("GET", f"/cards/{card_id}")

    def create_card(self, idList, name, **kwargs):
        params = {"name": name, "idList": idList}
        params.update(kwargs)
        return self._make_request("POST", "/cards", params=params)

    def delete_board(self, idBoard):
        return self._make_request("DELETE", f"/boards/{idBoard}")

    def get_board_by_id(self, idBoard):
        return self._make_request("GET", f"/boards/{idBoard}")

    def archive_card(self, card_id):
        return self._make_request("PUT", f"/cards/{card_id}", params={"closed":"true"})

    def update_card(self, card_id, **kwargs):
        return self._make_request("PUT", f"/cards/{card_id}", params=kwargs)

    def create_checklist(self, card_id, name):
        return self._make_request("POST", f"/cards/{card_id}/checklists", params={"card_id": card_id, "name": name})

    def create_checkitem(self, checklist_id, name):
        return self._make_request("POST", f"/checklists/{checklist_id}/checkItems", params={"checklist_it":checklist_id,"name": name})