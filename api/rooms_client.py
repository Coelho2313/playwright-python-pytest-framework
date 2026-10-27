"""Client de API que encapsula os endpoints usados no setup/teardown."""
from playwright.sync_api import APIRequestContext

from utils.data_factory import Room


class RoomsClient:
    """Operacoes de autenticacao e de quartos via APIRequestContext."""

    def __init__(self, request: APIRequestContext) -> None:
        self._request = request
        self._headers: dict[str, str] = {}

    def login(self, username: str, password: str) -> str:
        """Autentica e retorna o token (corpo da resposta ou Set-Cookie)."""
        response = self._request.post(
            "auth/login", data={"username": username, "password": password}
        )
        assert response.ok, f"Login via API falhou: {response.status} {response.text()}"

        token = ""
        try:
            body = response.json()
            if isinstance(body, dict):
                token = str(body.get("token", ""))
        except Exception:
            pass

        if not token:
            for header in response.headers_array():
                if header["name"].lower() == "set-cookie" and header["value"].startswith("token="):
                    token = header["value"].split(";", 1)[0].split("=", 1)[1]
                    break

        assert token, (
            f"Token nao encontrado. status={response.status} "
            f"body={response.text()!r} headers={response.headers_array()}"
        )
        self._headers = {"Cookie": f"token={token}"}
        return token

    def create_room(self, room: Room) -> None:
        """Cria um quarto."""
        response = self._request.post("room", data=room.to_payload(), headers=self._headers)
        assert response.ok, f"Criacao de quarto falhou: {response.status} {response.text()}"

    def list_rooms(self) -> list[dict]:
        """Lista os quartos existentes."""
        response = self._request.get("room", headers=self._headers)
        assert response.ok, f"Listagem falhou: {response.status}"
        return response.json().get("rooms", [])

    def find_room_id(self, room_name: str) -> int | None:
        """Retorna o id do quarto pelo nome, ou None."""
        for item in self.list_rooms():
            if item.get("roomName") == room_name:
                return item.get("roomid")
        return None

    def delete_room(self, room_id: int) -> None:
        """Remove um quarto (teardown)."""
        self._request.delete(f"room/{room_id}", headers=self._headers)
