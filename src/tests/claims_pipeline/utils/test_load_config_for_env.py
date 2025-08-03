from pathlib import Path

import pytest
from omegaconf import OmegaConf

from claims_pipeline.utils.load_config_for_env import _get_config_path, _load_config, load_config_for_env


@pytest.fixture
def mock__get_config_path() -> Path:
    return Path(__file__).resolve().parents[2] / "fixtures/config"


def test__load_config(mocker, mock__get_config_path: Path):
    _get_config_path_mock = mocker.patch("claims_pipeline.utils.load_config_for_env._get_config_path")
    _get_config_path_mock.return_value = mock__get_config_path
    _load_config_value = mock__get_config_path / "dev/pipeline.yml"

    assert _load_config("dev/pipeline.yml") == OmegaConf.load(_load_config_value)


envs = ["dev", "pre-prod", "prod"]


@pytest.mark.parametrize("env", envs)
def test_load_config_for_envs(env):
    load_config_for_env("training_pipeline.yml", env=env)
    assert load_config_for_env
