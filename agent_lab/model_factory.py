"""Model construction helpers for AgentRunner."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

from smolagents.models import Model, OpenAIServerModel

from agent_lab.offline_model import OfflineFinalAnswerModel

ModelProvider = Literal["offline", "wq_openai_compatible", "openai_compatible"]

DEFAULT_WQ_BASE_URL = "http://wanqing.internal/api/gateway/v1/endpoints"
DEFAULT_WQ_MODEL_ID = "ep-1rl9f4-1783391033049812063"


@dataclass(frozen=True)
class ModelConfig:
    provider: ModelProvider = "offline"
    model_id: str = "offline-final-answer"
    api_base: str | None = None
    api_key_env: str | None = None
    flatten_messages_as_text: bool = False


def create_model(config: ModelConfig | None = None) -> Model:
    config = config or ModelConfig()
    if config.provider == "offline":
        return OfflineFinalAnswerModel(model_id=config.model_id)

    if config.provider in {"wq_openai_compatible", "openai_compatible"}:
        api_key = _read_api_key(config.api_key_env)
        return OpenAIServerModel(
            model_id=config.model_id,
            api_base=config.api_base,
            api_key=api_key,
            flatten_messages_as_text=config.flatten_messages_as_text,
        )

    raise ValueError(f"Unsupported model provider: {config.provider}")


def model_config_from_env(provider: str | None = None) -> ModelConfig:
    selected_provider = provider or os.environ.get("AGENT_MODEL_PROVIDER", "offline")
    if selected_provider == "offline":
        return ModelConfig(provider="offline")

    if selected_provider == "wq_openai_compatible":
        return ModelConfig(
            provider="wq_openai_compatible",
            model_id=os.environ.get("WQ_MODEL_ID", DEFAULT_WQ_MODEL_ID),
            api_base=os.environ.get("WQ_BASE_URL", DEFAULT_WQ_BASE_URL),
            api_key_env="WQ_API_KEY",
        )

    if selected_provider == "openai_compatible":
        return ModelConfig(
            provider="openai_compatible",
            model_id=_required_env("OPENAI_MODEL_ID"),
            api_base=os.environ.get("OPENAI_BASE_URL"),
            api_key_env="OPENAI_API_KEY",
        )

    raise ValueError(f"Unsupported model provider: {selected_provider}")


def create_model_from_env(provider: str | None = None) -> Model:
    return create_model(model_config_from_env(provider))


def _read_api_key(env_name: str | None) -> str | None:
    if not env_name:
        return None
    return os.environ.get(env_name)


def _required_env(env_name: str) -> str:
    value = os.environ.get(env_name)
    if not value:
        raise ValueError(f"Required environment variable is not set: {env_name}")
    return value
