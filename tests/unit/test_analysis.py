"""Cost estimation and run log analysis tests."""

from __future__ import annotations

import json
from pathlib import Path

from src.analysis.logs import load_run_logs, summarize_runs
from src.run_log import _usage_payload, write_run_log
from src.shared.cost import estimate_cost_usd


def test_estimate_cost_gpt41_mini() -> None:
    cost = estimate_cost_usd("gpt-4.1-mini", prompt_tokens=100_000, completion_tokens=20_000)
    assert 0.07 < cost < 0.08


def test_usage_payload_from_object() -> None:
    class Usage:
        total_tokens = 100
        prompt_tokens = 70
        completion_tokens = 30
        successful_requests = 6

        def model_dump(self) -> dict:
            return {
                "total_tokens": self.total_tokens,
                "prompt_tokens": self.prompt_tokens,
                "completion_tokens": self.completion_tokens,
                "successful_requests": self.successful_requests,
            }

    class Result:
        token_usage = Usage()

    data = _usage_payload(Result())
    assert data is not None
    assert data["total_tokens"] == 100


def test_summarize_runs_from_fixture(tmp_path: Path) -> None:
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    payload = {
        "timestamp": "2026-06-13T10:00:00Z",
        "topic": "test topic",
        "success": True,
        "model": "gpt-4.1-mini",
        "tasks": [{"output_chars": 4000}] * 6,
    }
    (log_dir / "run_test.json").write_text(json.dumps(payload), encoding="utf-8")
    rows = summarize_runs(load_run_logs(log_dir))
    assert len(rows) == 1
    assert rows[0]["cost_usd"] > 0


def test_write_results_report(tmp_path: Path, monkeypatch) -> None:
    from src.analysis.report import write_results_report

    charts = tmp_path / "charts"
    monkeypatch.setattr("src.analysis.report.CHARTS_DIR", charts)
    rows = [
        {
            "timestamp": "2026-06-13T10:00:00Z",
            "topic": "Topic A",
            "success": True,
            "model": "gpt-4.1-mini",
            "prompt_tokens": 1000,
            "completion_tokens": 500,
            "total_tokens": 1500,
            "estimated": True,
            "output_chars": 6000,
            "cost_usd": 0.01,
            "source": "run_a.json",
        },
        {
            "timestamp": "2026-06-13T11:00:00Z",
            "topic": "Topic B",
            "success": True,
            "model": "gpt-4.1-mini",
            "prompt_tokens": 2000,
            "completion_tokens": 800,
            "total_tokens": 2800,
            "estimated": False,
            "output_chars": 3200,
            "cost_usd": 0.02,
            "source": "run_b.json",
        },
    ]
    out = write_results_report(rows, out_md=tmp_path / "results.md")
    text = out.read_text(encoding="utf-8")
    assert "Topic A" in text
    assert (charts / "run_cost_comparison.png").is_file()


def test_write_run_log_includes_model(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.run_log.LOG_DIR", tmp_path)
    path = write_run_log(topic="t", success=True, model="gpt-4.1-mini")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["model"] == "gpt-4.1-mini"
