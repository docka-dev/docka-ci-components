from pathlib import Path


def embedded_python(template: str) -> str:
    marker = "      python - <<'PY'\n"
    start = template.index(marker) + len(marker)
    end = template.index("      PY\n", start)
    lines = template[start:end].splitlines()
    return "\n".join(line[6:] if line.startswith("      ") else line for line in lines) + "\n"


template = Path("templates/deploy.yml").read_text(encoding="utf-8")
for required in (
    "aud: https://api.docka.dev/ci",
    "DOCKA_ID_TOKEN",
    "Idempotency-Key",
    "/api/v1/ci/exchange",
    "/api/v1/apps/",
    "dotenv: docka.env",
):
    assert required in template, required
compile(embedded_python(template), "templates/deploy.yml", "exec")
