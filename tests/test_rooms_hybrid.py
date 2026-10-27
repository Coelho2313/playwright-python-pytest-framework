"""Testes híbridos: estado criado via API, validado na UI já autenticada."""
import pytest
from playwright.sync_api import BrowserContext

from api.rooms_client import RoomsClient
from pages.admin_rooms_page import AdminRoomsPage
from config.settings import Settings
from utils.data_factory import Room


@pytest.mark.hybrid
@pytest.mark.smoke
def test_room_created_via_api_is_listed_in_ui(
    logged_context: BrowserContext, settings: Settings, room: Room
) -> None:
    """Quarto criado pela API aparece na UI sem nenhum login manual."""
    page = logged_context.new_page()
    admin = AdminRoomsPage(page, settings.base_url).open()
    admin.expect_room_visible(room.room_name)


@pytest.mark.hybrid
@pytest.mark.regression
def test_room_deleted_via_api_disappears_from_ui(
    logged_context: BrowserContext,
    settings: Settings,
    rooms_api: RoomsClient,
    room: Room,
) -> None:
    """Após remover via API, o quarto não deve mais ser listado."""
    room_id = rooms_api.find_room_id(room.room_name)
    assert room_id is not None
    rooms_api.delete_room(room_id)

    page = logged_context.new_page()
    admin = AdminRoomsPage(page, settings.base_url).open()
    admin.expect_room_absent(room.room_name)


@pytest.mark.api
def test_created_room_is_returned_by_api(rooms_api: RoomsClient, room: Room) -> None:
    """Valida o contrato básico da API de quartos."""
    assert rooms_api.find_room_id(room.room_name) is not None
