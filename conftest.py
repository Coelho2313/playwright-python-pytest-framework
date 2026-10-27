"""Fixtures globais: API autenticada, contexto logado e artefatos em falha.

Browser, contexto e pÃ¡gina vÃªm do pytest-playwright (isolados por teste, seguros
para xdist). Parametrize browsers com `--browser chromium --browser firefox`.
Traces/vÃ­deos/screenshots sÃ³ sÃ£o mantidos quando o teste falha.
"""
from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import APIRequestContext, BrowserContext, Playwright, expect

from api.rooms_client import RoomsClient
from config.settings import Settings, get_settings
from utils.data_factory import Room, unique_room

OUTPUTS = Path("outputs")


@pytest.fixture(scope="session")
def settings() -> Settings:
    """ConfiguraÃ§Ãµes do ambiente."""
    return get_settings()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, settings: Settings) -> dict:
    """Argumentos globais de contexto (viewport, base_url, vÃ­deo)."""
    return {
        **browser_context_args,
        "base_url": settings.base_url,
        "viewport": {"width": 1366, "height": 768},
    }


@pytest.fixture
def api_request(playwright: Playwright, settings: Settings) -> Generator[APIRequestContext, None, None]:
    """APIRequestContext isolado por teste (cookies de sessÃ£o prÃ³prios)."""
    ctx = playwright.request.new_context(base_url=settings.api_url + "/")
    yield ctx
    ctx.dispose()


@pytest.fixture
def rooms_api(api_request: APIRequestContext) -> RoomsClient:
    """Client de API jÃ¡ com o contexto de requisiÃ§Ãµes."""
    return RoomsClient(api_request)


@pytest.fixture
def auth_token(rooms_api: RoomsClient, settings: Settings) -> str:
    """Token de sessÃ£o obtido via API (sem passar pela UI)."""
    return rooms_api.login(settings.admin_user, settings.admin_password)


@pytest.fixture
def logged_context(context: BrowserContext, auth_token: str, settings: Settings) -> BrowserContext:
    """Contexto do browser logado: o token da API Ã© injetado como cookie."""
    domain = settings.base_url.split("//", 1)[1].split("/", 1)[0]
    context.add_cookies(
        [{"name": "token", "value": auth_token, "domain": domain, "path": "/"}]
    )
    return context


@pytest.fixture
def room(rooms_api: RoomsClient, auth_token: str) -> Generator[Room, None, None]:
    """Cria um quarto Ãºnico via API e o remove no teardown (idempotente)."""
    new_room = unique_room()
    rooms_api.create_room(new_room)
    yield new_room
    room_id = rooms_api.find_room_id(new_room.room_name)
    if room_id is not None:
        rooms_api.delete_room(room_id)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """ExpÃµe o resultado de cada fase no item (usado para decidir artefatos)."""
    outcome = yield
    setattr(item, f"rep_{call.when}", outcome.get_result())


expect.set_options(timeout=15_000)
