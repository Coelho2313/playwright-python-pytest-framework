# playwright-python-pytest-framework

Framework de automação híbrida (API + UI) com Python, Pytest, Playwright e pytest-xdist.
Alvo: Restful Booker Platform (https://automationintesting.online).

## Arquitetura
- `api/`: clients de API (setup/teardown de massa)
- `pages/`: Page Objects
- `tests/`: testes por domínio
- `config/`, `utils/`: settings (pydantic-settings) e fábrica de dados
- `conftest.py`: fixtures (API, contexto logado por cookie, quarto único com teardown)

## Estratégia híbrida
Login e criação de massa via `APIRequestContext`; o token retornado é injetado como
cookie no contexto do browser, então a UI abre já autenticada.

## Execução
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install
pytest -n auto                                   # paralelo
pytest -n 4 --browser chromium --browser firefox # cross-browser
pytest -m smoke
pytest --headed --slowmo 300                     # depuração
```
Artefatos de falha (trace, vídeo, screenshot) e `report.html` ficam em `outputs/`.
Ver trace: `playwright show-trace outputs/artifacts/<teste>/trace.zip`.

## Auto-waiting
Sem `time.sleep`: locators e `expect(...)` aguardam automaticamente o elemento ficar
visível/estável, com retry até o timeout.
