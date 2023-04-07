"""Tests for the :mod:`short_it.parse_config` module."""
import omegaconf
import pytest
from faker import Faker
from pytest_mock import MockerFixture

import short_it.config
import short_it.parse_config
import short_it.utils


@pytest.fixture
def instance(class_mocker: MockerFixture) -> short_it.parse_config.ParseConfigToMachineData:
    """Fixture for properly creating :class:`short_it.parse_config.ParseConfigToMachineData` instance."""
    mocked_parse_config = class_mocker.patch(
        "short_it.parse_config.ParseConfigToMachineData._parse_config", return_value={}
    )

    if short_it.parse_config.ParseConfigToMachineData in short_it.utils.Singleton._instances:
        del short_it.utils.Singleton._instances[short_it.parse_config.ParseConfigToMachineData]

    instance = short_it.parse_config.ParseConfigToMachineData()

    class_mocker.stop(mocked_parse_config)
    instance._config.projects = {}
    instance._config.simple = {}

    return instance


class TestGetUrl:
    """Tests for :meth:`short_it.parse_config.ParseConfigToMachineData.get_url` method."""

    def test_no_project_name(self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData) -> None:
        """Test for situation, when project name is not found."""
        assert instance.get_url(faker.word(), faker.word()) is None

    def test_no_link_type(self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData) -> None:
        """Test for situation, when link type is not found."""
        project_name = faker.word()
        instance._data[project_name] = {}
        assert instance.get_url(project_name, faker.word()) is None

    def test_simple_link(self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData) -> None:
        """Test for simple link success handling."""
        project_name, expected_value = faker.word(), faker.url()
        instance._data[project_name] = expected_value
        assert instance.get_url(project_name, None) == expected_value

    def test_simple_link_and_link_type_specified(
        self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData
    ) -> None:
        """Test for situation, when simple link and link type specified."""
        project_name = faker.word()
        instance._data[project_name] = faker.url()
        with pytest.raises(short_it.parse_config.OneLinkAndLinkTypeSpecifiedError):
            instance.get_url(project_name, faker.word())

    def test_no_link_type_and_project_link(
        self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData
    ) -> None:
        """Test for situation, when no link type specified and project has multiple links."""
        project_name = faker.word()
        instance._data[project_name] = {faker.word(): faker.url()}
        with pytest.raises(short_it.parse_config.MultipleLinksNoLinkTypeError):
            instance.get_url(project_name, None)

    def test_success(self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData) -> None:
        """Test for situation, when everything is success."""
        project_name, link_type, expected_value = faker.word(), faker.word(), faker.url()
        instance._data[project_name] = {link_type: expected_value}
        assert instance.get_url(project_name, link_type) == expected_value


class TestParseConfig:
    """Tests for :meth:`short_it.parse_config.ParseConfigToMachineData._parse_config` method."""

    def test_no_projects(self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData) -> None:
        """Test for situation, when there are no projects in config."""
        instance._config.projects = {}
        assert instance._parse_config() == {}

    def test_no_links(self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData) -> None:
        """Test for situation, when there are no links in config."""
        project_name = faker.word()
        instance._config.projects = {project_name: {}}
        assert instance._parse_config() == {project_name: {}}

    def test_no_aliases(self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData) -> None:
        """Test for situation, when there are no aliases for links in config."""
        destination = faker.url()
        project_name, link_type, link_settings = (
            faker.word(),
            faker.word(),
            omegaconf.OmegaConf.structured({"to": destination}),
        )

        instance._config.projects = {project_name: {link_type: link_settings}}

        assert instance._parse_config() == {project_name: {link_type: destination}}

    def test_a_few_aliases(self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData) -> None:
        """Test for situation, when there are aliases for links in config."""
        destination, aliases = faker.url(), [faker.word() for _ in range(faker.pyint(min_value=3, max_value=10))]
        project_name, link_type, link_settings = (
            faker.word(),
            faker.word(),
            omegaconf.OmegaConf.structured({"to": destination, "aliases": aliases}),
        )

        instance._config.projects = {project_name: {link_type: link_settings}}

        assert instance._parse_config() == {
            project_name: {
                link_type: destination,
                **{alias: destination for alias in aliases},
            }
        }

    def test_additional_aliases(self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData) -> None:
        """Test for situation, when there are aliases and additional aliases for links in config."""
        destination, aliases, additional_aliases = (
            faker.url(),
            [faker.word() for _ in range(faker.pyint(min_value=3, max_value=10))],
            [faker.word() for _ in range(faker.pyint(min_value=3, max_value=10))],
        )
        project_name, link_type, link_settings = (
            faker.word(),
            faker.word(),
            omegaconf.OmegaConf.structured(
                {"to": destination, "aliases": aliases, "additional_aliases": additional_aliases}
            ),
        )

        instance._config.projects = {project_name: {link_type: link_settings}}

        assert instance._parse_config() == {
            project_name: {
                link_type: destination,
                **{alias: destination for alias in aliases},
                **{additional_alias: destination for additional_alias in additional_aliases},
            }
        }

    def test_only_additional_aliases(
        self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData
    ) -> None:
        """Test for situation, when there are only additional aliases for links in config."""
        destination, additional_aliases = faker.url(), [
            faker.word() for _ in range(faker.pyint(min_value=3, max_value=10))
        ]
        project_name, link_type, link_settings = (
            faker.word(),
            faker.word(),
            omegaconf.OmegaConf.structured({"to": destination, "additional_aliases": additional_aliases}),
        )

        instance._config.projects = {project_name: {link_type: link_settings}}

        assert instance._parse_config() == {
            project_name: {
                link_type: destination,
                **{additional_alias: destination for additional_alias in additional_aliases},
            }
        }

    def test_only_simple(self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData) -> None:
        """Test for situation, when there are no aliases for links in config."""
        simple_key, simple_value = (faker.word(), faker.word())

        instance._config.projects = {}
        instance._config.simple = {simple_key: simple_value}

        assert instance._parse_config() == {simple_key: simple_value}

    def test_simple_and_a_few_aliases(
        self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData
    ) -> None:
        """Test for situation, when there are aliases for links in config."""
        destination, aliases = faker.url(), [faker.word() for _ in range(faker.pyint(min_value=3, max_value=10))]
        simple_key, simple_value, project_name, link_type, link_settings = (
            faker.word(),
            faker.word(),
            faker.word(),
            faker.word(),
            omegaconf.OmegaConf.structured({"to": destination, "aliases": aliases}),
        )

        instance._config.projects = {project_name: {link_type: link_settings}}
        instance._config.simple = {simple_key: simple_value}

        assert instance._parse_config() == {
            project_name: {
                link_type: destination,
                **{alias: destination for alias in aliases},
            },
            simple_key: simple_value,
        }

    def test_simple_and_additional_aliases(
        self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData
    ) -> None:
        """Test for situation, when there are aliases and additional aliases for links in config."""
        simple_key, simple_value, destination, aliases, additional_aliases = (
            faker.word(),
            faker.word(),
            faker.url(),
            [faker.word() for _ in range(faker.pyint(min_value=3, max_value=10))],
            [faker.word() for _ in range(faker.pyint(min_value=3, max_value=10))],
        )
        project_name, link_type, link_settings = (
            faker.word(),
            faker.word(),
            omegaconf.OmegaConf.structured(
                {"to": destination, "aliases": aliases, "additional_aliases": additional_aliases}
            ),
        )

        instance._config.projects = {project_name: {link_type: link_settings}}
        instance._config.simple = {simple_key: simple_value}

        assert instance._parse_config() == {
            project_name: {
                link_type: destination,
                **{alias: destination for alias in aliases},
                **{additional_alias: destination for additional_alias in additional_aliases},
            },
            simple_key: simple_value,
        }

    def test_simple_and_only_additional_aliases(
        self, faker: Faker, instance: short_it.parse_config.ParseConfigToMachineData
    ) -> None:
        """Test for situation, when there are only additional aliases for links in config."""
        simple_key, simple_value, destination, additional_aliases = (
            faker.word(),
            faker.word(),
            faker.url(),
            [faker.word() for _ in range(faker.pyint(min_value=3, max_value=10))],
        )
        project_name, link_type, link_settings = (
            faker.word(),
            faker.word(),
            omegaconf.OmegaConf.structured({"to": destination, "additional_aliases": additional_aliases}),
        )

        instance._config.projects = {project_name: {link_type: link_settings}}
        instance._config.simple = {simple_key: simple_value}

        assert instance._parse_config() == {
            project_name: {
                link_type: destination,
                **{additional_alias: destination for additional_alias in additional_aliases},
            },
            simple_key: simple_value,
        }
