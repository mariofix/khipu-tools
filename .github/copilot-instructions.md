# Khipu Tools — Copilot Instructions

## Project Overview

Python SDK for Khipu's payment APIv3. Wraps REST endpoints (`/v3/payments`, `/v3/banks`, `/v3/predict`) into a typed, Stripe-style client. Supports Python 3.9–3.12, managed with Poetry.

## Commands

```bash
# Install dependencies
poetry install --all-extras

# Run all tests
poetry run pytest

# Run a single test file
poetry run pytest tests/test_payment.py

# Run a single test
poetry run pytest tests/test_payment.py::TestPayments::test_payments_create

# Run tests with coverage
poetry run coverage run -m pytest && poetry run coverage report

# Format
poetry run black khipu_tools tests

# Lint
poetry run pylint khipu_tools
```

## Architecture

### Dual-usage pattern

**Global (module-level):** set `khipu_tools.api_key` once, then call class methods directly.

```python
import khipu_tools
khipu_tools.api_key = "..."
payment = khipu_tools.Payments.create(amount="5000", currency="CLP", subject="...")
```

**Client instance:** instantiate `KhipuClient` for multi-tenant or explicit control.

```python
client = khipu_tools.KhipuClient(api_key="...")
```

### Class hierarchy

```
KhipuObject (dict subclass)
└── APIResource[T]
    ├── Payments     → POST/GET/DELETE/POST /v3/payments[/{id}[/refunds]]
    ├── Banks        → GET /v3/banks
    └── Predict      → GET /v3/predict
```

- `KhipuObject` extends `dict` — response fields are accessed as both attributes (`obj.payment_id`) and dict keys (`obj["payment_id"]`).
- `APIResource` builds the URL from two class variables: `OBJECT_PREFIX` (e.g. `"v3"`) and `OBJECT_NAME` (e.g. `"payments"`), producing `/v3/payments`.
- `_APIRequestor` is a singleton for global usage; `KhipuClient` creates its own instance for per-client usage.
- All API responses are deserialized into `KhipuObject` instances via `_util._convert_to_khipu_object`.

### Adding a new resource

1. Create `khipu_tools/_myresource.py` extending `APIResource[T]`.
2. Set `OBJECT_NAME` and `OBJECT_PREFIX = "v3"`.
3. Define inner `TypedDict`/`RequestOptions` param classes and `KhipuObject` response classes.
4. Expose via `khipu_tools/__init__.py`.
5. Add tests under `tests/test_myresource.py`.

## Key Conventions

### Testing
- Tests mock `_static_request` on the resource class (not the HTTP layer): `mocker.patch.object(Payments, "_static_request", return_value=...)`.
- Response mocks are `KhipuObject` subclasses with attributes set manually in `__init__`.
- `pytest-mock` is used; fixtures in each test class.

### Typing
- Method params use `Unpack[ClassName.ParamsClass]` with `**params` to preserve type hints.
- Response types are `KhipuObject["ResponseClass"]` — the generic param is a hint only, not enforced at runtime.
- `Optional[str]` fields in `RequestOptions`/`PaymentParams` mean the API accepts but doesn't require them.

### Error handling
- `khipu_tools._error` defines typed exception classes; `_api_requestor` raises them based on HTTP status codes.
- Always check `isinstance(result, KhipuObject)` after `_static_request` and raise `TypeError` if not — see existing resources for the pattern.

### Code style
- Line length: **119** characters (Black + isort both configured for this).
- All public methods and classes must have docstrings (in Spanish, matching the Khipu API docs).
- Module-level files use the `_` prefix (private) — only symbols re-exported in `__init__.py` are public API.

### Versioning
- Version is kept in two places: `pyproject.toml` (`version =`) and `khipu_tools/_version.py` (`VERSION =`). Keep them in sync.
- Version format: `YYYY.N.0` (e.g. `2025.2.0`).

## Git

- Branches: `claude/feature-name` (kebab-case, `claude/` prefix).
- Conventional commits: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`.
- Never commit directly to `main`; open a PR.
