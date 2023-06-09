"""File for the main config."""
import dataclasses
import pathlib
import typing as t

import omegaconf
import typing_extensions as te

from short_it import utils

BASE_DIR = pathlib.Path(__file__).parent.parent


@dataclasses.dataclass
class SentryConfigSection:
    """Sentry config section."""

    enabled: bool = False
    dsn: str = "..."
    traces_sample_rate: float = 1.0


@dataclasses.dataclass
class LinkSettings:
    """Settings for a one project link."""

    to: str = "..."
    aliases: list[str] | None = None
    additional_aliases: list[str] | None = None

    def resolve_builtin_aliases(self, link_type: str) -> None:
        """Add pre-defined aliases, if user set some often used link type."""
        if (
            hasattr(self, "aliases") and self.aliases is not None
        ):  # omegaconf.errors.ConfigAttributeError: Missing key aliases
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

    projects: dict[str, dict[str, LinkSettings]] = dataclasses.field(default_factory=dict)
    simple: dict[str, str] = dataclasses.field(default_factory=dict)
    sentry: SentryConfigSection = dataclasses.field(default_factory=SentryConfigSection)

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

        for project in cfg.projects.values():
            for link_type, link_settings in project.items():
                LinkSettings.resolve_builtin_aliases(link_settings, link_type)

        return t.cast(te.Self, cfg)
