"""
Module for managing different env of configuration
"""
from enum import Enum
from pathlib import Path


class _Config:
    """
    Class for managing the basic configuration
    """
    WORKING_DIRECTORY = Path(__file__).parent.absolute().parent.absolute()
    IMAGES_DIR = str(Path(WORKING_DIRECTORY, "images"))
    FONTS_DIR = str(Path(WORKING_DIRECTORY, "fonts"))

    PORT = 8080
    HOST = "localhost"
    API_BASE_PATH = "/api/v1"
    API_BASE_URL = f"http://{HOST}:{PORT}{API_BASE_PATH}"

    DEBUG = False
    TESTING = False


class _DevConfig(_Config):
    """
    Class for managing dev environment configuration
    """
    DEBUG = True


class _TestConfig(_Config):
    """
    Class for managing test environment configuration
    """
    TESTING = True


class ConfigName(Enum):
    """
    Class member of environment configuration
    """
    DEV = "dev"
    TEST = "test"


def get_config(env):
    """
    Get specific environment specific config
    """
    switch = {
        ConfigName.DEV.value: _DevConfig,
        ConfigName.TEST.value: _TestConfig,
    }
    return switch[env]
