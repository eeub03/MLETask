from pathlib import Path
from typing import Any

from omegaconf import DictConfig, ListConfig, OmegaConf


def _get_config_path() -> Path:
    config_dir = Path(__file__).resolve().parents[1]
    return config_dir / "config"  # return absolute path to config directory in claims_pipeline/config


def _load_config(filename: str) -> DictConfig | ListConfig:
    # Relative path to the file inside the config directory
    config_file = _get_config_path() / filename
    config = OmegaConf.load(config_file)

    return config


def load_config_for_env(filename: str, env: str) -> Any:  # noqa: ANN401
    """Load configuration from a YAML file for a specific environment.

    Merges the base configuration with the environment-specific configuration.
    """
    base_config = _load_config(f"base/{filename}")
    env_config = _load_config(f"{env}/{filename}")
    merged_config = OmegaConf.merge(base_config, env_config)
    return merged_config
