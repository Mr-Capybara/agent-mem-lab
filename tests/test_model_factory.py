import os

from smolagents.models import OpenAIServerModel

from agent_lab.model_factory import (
    DEFAULT_WQ_BASE_URL,
    DEFAULT_WQ_MODEL_ID,
    create_model,
    model_config_from_env,
)
from agent_lab.offline_model import OfflineFinalAnswerModel


def test_offline_model_is_default(monkeypatch) -> None:
    monkeypatch.delenv("AGENT_MODEL_PROVIDER", raising=False)

    config = model_config_from_env()
    model = create_model(config)

    assert config.provider == "offline"
    assert isinstance(model, OfflineFinalAnswerModel)


def test_wq_model_config_uses_environment(monkeypatch) -> None:
    monkeypatch.setenv("AGENT_MODEL_PROVIDER", "wq_openai_compatible")
    monkeypatch.setenv("WQ_API_KEY", "test-key")
    monkeypatch.delenv("WQ_BASE_URL", raising=False)
    monkeypatch.delenv("WQ_MODEL_ID", raising=False)

    config = model_config_from_env()
    model = create_model(config)

    assert config.provider == "wq_openai_compatible"
    assert config.api_base == DEFAULT_WQ_BASE_URL
    assert config.model_id == DEFAULT_WQ_MODEL_ID
    assert isinstance(model, OpenAIServerModel)
    assert model.model_id == DEFAULT_WQ_MODEL_ID


def test_wq_model_config_allows_endpoint_override(monkeypatch) -> None:
    monkeypatch.setenv("WQ_API_KEY", "test-key")
    monkeypatch.setenv("WQ_BASE_URL", "http://example.internal/v1")
    monkeypatch.setenv("WQ_MODEL_ID", "custom-endpoint")

    config = model_config_from_env("wq_openai_compatible")

    assert config.api_base == "http://example.internal/v1"
    assert config.model_id == "custom-endpoint"
    assert os.environ["WQ_API_KEY"] == "test-key"
