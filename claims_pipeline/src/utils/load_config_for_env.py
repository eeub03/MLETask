from omegaconf import OmegaConf, DictConfig
from pathlib import Path
from typing import Any


def _get_config_path() -> Path:
    config_dir = Path(__file__).resolve().parents[1]
    return config_dir / "config"


def _load_config(filename: str) -> DictConfig | list[DictConfig]:
    # Relative path to the file inside the config directory
    config_file = _get_config_path() / filename
    config = OmegaConf.load(config_file)

    return config


def load_config_for_env(filename: str, env: str) -> Any:
    """
    Load configuration from a YAML file for a specific environment.
    Merges the base configuration with the environment-specific configuration.

    Args:
        filename (str): The path to the YAML configuration file.
        env (str): The environment for which to load the configuration.

    Returns:
        OmegaConf: The loaded configuration object.
    """
    base_config = _load_config(f"base/{filename}")
    env_config = _load_config(f"{env}/{filename}")
    merged_config = OmegaConf.merge(base_config, env_config)
    return merged_config
