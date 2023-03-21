"""Parse config (human friendly data) to machine data."""
import typing as t

import omegaconf.errors

import short_it.config as config_module
import short_it.utils as utils


class ParseConfigToMachineData(metaclass=utils.Singleton):
    """Parse config (human friendly data) to machine data.

    This actually creates a dict, where multiple keys point to one value.
    So aliases handled easily. The class itself is Singleton, so performance
    is ok.
    """

    def __init__(self) -> None:
        self._config = config_module.Config()
        self._data: dict[str, dict[str, str]] = self._parse_config()
        #                ^^^       ^^^  ^^^
        #              project    link  destination
        #               name      type

    def get_url(self, project_name: str, link_type: str) -> str | None:
        """Get the redirected URL.

        Returns:
            :class:`str`: if URL is found, :class:`None` if 404.
        """
        if project_name not in self._data.keys():
            return None

        project_links = self._data[project_name]
        if link_type not in project_links.keys():
            return None

        return project_links[link_type]

    def _parse_config(self) -> dict[str, dict[str, str]]:
        """Parse config into the :class:`dict` with multiple keys to one value.

        This code is soooo bad, but IDK how to do it better.
        """
        result: dict[str, dict[str, str]] = {}
        for project_name, project_links in self._config.projects.items():
            result[project_name] = {}

            for link_name, link_settings in project_links.items():
                aliases: list[str] = [link_name]

                # omegaconf raises an error on accessing undefined attribute, even if it's ok
                # to be undefined. the code below, just tries to do try-except, so nothing
                # will crash
                for get_optional_field_value in [
                    lambda: link_settings.aliases,
                    lambda: link_settings.additional_aliases,
                ]:
                    try:
                        optional_field_value = t.cast(t.Callable[[], list[str]], get_optional_field_value)()
                    except omegaconf.errors.ConfigAttributeError:
                        pass
                    else:
                        for value in optional_field_value:
                            aliases.append(value)

                result[project_name].update(
                    dict.fromkeys(
                        aliases,
                        link_settings.to,
                    )
                )

        return result
