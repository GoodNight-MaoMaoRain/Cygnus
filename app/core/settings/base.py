from enum import Enum


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"

class RestartType(str, Enum):
    software = "software"
    hardware = "hardware"

class LogType(str, Enum):
    python = "python"
    go = "Go"
    product = "product"
    hardware = "hardware"
    frontend = "frontend"
    null = ""


class BaseAppSettings:
    app_env: AppEnvTypes = AppEnvTypes.prod

    # class Config:
    #     env_file = ".env"
