from pathlib import Path


def test_source_does_not_expose_recovery_key_api() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in Path("src/ghost_wave").glob("*.py")
    )
    forbidden = "get_" + "recovery_key"
    assert forbidden not in source


def test_simulator_contains_no_network_client_imports() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in Path("src/ghost_wave").glob("*.py")
    )
    for token in ("requests", "socket", "paramiko", "scapy"):
        assert f"import {token}" not in source
        assert f"from {token}" not in source
