"""Write the FastAPI OpenAPI document to packages/contracts/openapi.yaml.

Usage (from apps/api): uv run python scripts/export_openapi.py [output_path]
"""

import sys
from pathlib import Path

import yaml
from pydantic import SecretStr

from app.core.config import Settings
from app.main import create_app

DEFAULT_OUT = Path(__file__).resolve().parents[3] / "packages" / "contracts" / "openapi.yaml"


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    # Schema generation never connects anywhere; placeholder URLs keep settings valid.
    settings = Settings(
        database_url=SecretStr("postgresql+asyncpg://unused/unused"),
        valkey_url=SecretStr("redis://unused"),
    )
    spec = create_app(settings).openapi()
    out.write_text(yaml.safe_dump(spec, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
