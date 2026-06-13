"""Run log JSON helpers."""

from __future__ import annotations

from types import SimpleNamespace

from src.run_log import log_failure, write_run_log


class _FakeOutput:
    def __init__(self, raw: str, role: str | None = None) -> None:
        self.raw = raw
        self.agent = SimpleNamespace(role=role) if role else None


class _FakeResult:
    def __init__(self, outputs: list[_FakeOutput]) -> None:
        self.tasks_output = outputs


def test_write_run_log_success(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run_log.LOG_DIR", tmp_path)
    result = _FakeResult([_FakeOutput("brief", "Researcher"), _FakeOutput("plan", "Planner")])
    path = write_run_log(topic="t", success=True, result=result, artifacts={"pdf": "x"})
    data = path.read_text(encoding="utf-8")
    assert '"success": true' in data
    assert (tmp_path / "latest.json").is_file()


def test_log_failure_marks_last_task(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run_log.LOG_DIR", tmp_path)
    result = _FakeResult([_FakeOutput("ok", "Researcher")])
    path = log_failure("topic", RuntimeError("boom"), result)
    assert '"success": false' in path.read_text(encoding="utf-8")
