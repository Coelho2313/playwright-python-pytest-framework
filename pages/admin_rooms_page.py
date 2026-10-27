"""Page Object da area administrativa de quartos."""
from playwright.sync_api import Locator, Page, expect


class AdminRoomsPage:
    """Mapeia elementos e acoes da tela /admin."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self._url = f"{base_url}/admin/rooms"

    def open(self) -> "AdminRoomsPage":
        """Abre a area admin (ja autenticada via cookie injetado)."""
        self.page.goto(self._url)
        return self

    def room_by_name(self, name: str) -> Locator:
        """Localiza o quarto pelo nome exibido na lista."""
        return self.page.get_by_text(name, exact=True)

    def expect_room_visible(self, name: str) -> None:
        """Valida que o quarto aparece; o expect aguarda automaticamente."""
        expect(self.room_by_name(name)).to_be_visible()

    def expect_room_absent(self, name: str) -> None:
        """Valida que o quarto nao esta listado."""
        expect(self.room_by_name(name)).to_have_count(0)
