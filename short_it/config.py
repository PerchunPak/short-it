"""File for the main config."""
import dataclasses
import pathlib
import typing as t
from enum import IntEnum

import omegaconf
import typing_extensions as te

from short_it import utils

BASE_DIR = pathlib.Path(__file__).parent.parent


class LogLevel(IntEnum):
    """Log level for the app."""

    TRACE = 5
    """Use only for tracing error without a debugger."""
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


@dataclasses.dataclass
class LoggingConfigSection:
    """Part of config for logging."""

    level: LogLevel = LogLevel.INFO
    """Log level for the app."""
    json: bool = False
    """Transform logs into JSON."""


@dataclasses.dataclass
class LinkSettings:
    """Settings for a one project link."""

    to: str = "..."
    aliases: list[str] | None = None
    additional_aliases: list[str] | None = None

    def add_builtin_aliases(self, link_type: str) -> None:
        """Add pre-defined aliases, if user set some often used link type."""
        if self.aliases is not None:
            return

        match link_type:
            case "github" | "gh":
                self.aliases = ["github", "gh", "git", "src", "sources", "source", "vcs"]
            case "read-the-docs" | "readthedocs" | "rtd":
                self.aliases = ["rtd", "readthedocs", "read-the-docs", "docs", "wiki"]
            case "docs" | "wiki":
                self.aliases = ["docs", "wiki", "documentation"]


@dataclasses.dataclass
class Config(metaclass=utils.Singleton):
    """The main config that holds everything in itself."""

    domain: str = "..."
    projects: dict[str, dict[str, LinkSettings]] = dataclasses.field(default_factory=dict)
    logging: LoggingConfigSection = dataclasses.field(default_factory=LoggingConfigSection)

    @classmethod
    def _setup(cls) -> te.Self:
        """Set up the config.

        It is just load config from file, also it is rewrite config with merged data.

        Returns:
            :py:class:`.Config` instance.
        """
        config_path = BASE_DIR / "data" / "config.yml"
        config_path.parent.mkdir(exist_ok=True)
        cfg = omegaconf.OmegaConf.structured(cls)

        if config_path.exists():
            loaded_config = omegaconf.OmegaConf.load(config_path)
            cfg = omegaconf.OmegaConf.merge(cfg, loaded_config)

        with open(config_path, "w") as config_file:
            omegaconf.OmegaConf.save(cfg, config_file)

        return t.cast(te.Self, cfg)
