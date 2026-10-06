"""Validate renamed package/DocType wiring without needing a Frappe bench."""

import ast
import json
import pathlib
import re
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]
APP = ROOT / "fibersoft_reports"

assert APP.is_dir() and not (ROOT / "lumen_reports").exists()
project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
assert project["project"]["name"] == "fibersoft_reports"
assert "Lumen Solutions" in (ROOT / "license.txt").read_text(encoding="utf-8")

python_count = 0
for source in APP.rglob("*.py"):
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    python_count += 1
    for node in ast.walk(tree):
        modules = []
        if isinstance(node, ast.ImportFrom) and node.module:
            modules = [node.module]
        elif isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        for module in modules:
            assert not module.startswith("lumen_reports"), (source, module)
            if module.startswith("fibersoft_reports"):
                target = ROOT.joinpath(*module.split("."))
                assert target.with_suffix(".py").exists() or target.is_dir(), (source, module)

doctypes = {}
for source in APP.rglob("*.json"):
    data = json.loads(source.read_text(encoding="utf-8"))
    if data.get("doctype") != "DocType":
        continue
    assert data["module"] == "Fibersoft Reports", source
    assert data["name"].startswith("Fibersoft "), source
    assert source.stem == data["name"].lower().replace(" ", "_"), source
    controller = ast.parse(source.with_suffix(".py").read_text(encoding="utf-8"))
    expected_class = data["name"].replace(" ", "")
    assert any(isinstance(node, ast.ClassDef) and node.name == expected_class for node in controller.body), source
    doctypes[data["name"]] = data

assert len(doctypes) == 9, len(doctypes)
for name, data in doctypes.items():
    for field in data.get("fields", []):
        target = field.get("options", "")
        if field.get("fieldtype") in ("Link", "Table", "Table MultiSelect") and target.startswith("Fibersoft "):
            assert target in doctypes, (name, target)

hooks = (APP / "hooks.py").read_text(encoding="utf-8")
assert 'app_name = "fibersoft_reports"' in hooks
assert 'app_title = "Fibersoft Reports"' in hooks
assert '"route": "/fibersoft"' in hooks
assert (APP / "www/fibersoft.py").exists()
license_code = (APP / "licensing.py").read_text(encoding="utf-8")
assert 'CONFIG_KEY = "sk_lumen_reports"' in license_code
assert "marketplace.get_subscription_info" in license_code
for html_path in (APP / "www/fibersoft.html", APP / "public/frontend/index.html"):
    html = html_path.read_text(encoding="utf-8")
    assert "<title>Fibersoft Reports</title>" in html
    assert "/assets/lumen_reports/" not in html
    for asset in re.findall(r'(?:src|href)="(/assets/fibersoft_reports/[^\"]+)"', html):
        target = APP / "public" / asset.removeprefix("/assets/fibersoft_reports/")
        assert target.is_file(), (html_path, asset)
print(f"Validated {python_count} Python modules, 9 DocTypes, imports, hooks and subscription wiring.")
