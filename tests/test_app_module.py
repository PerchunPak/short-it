"""Tests for :mod:`short_it.app` module."""
import fastapi
import pytest
from faker import Faker
from pytest_mock import MockerFixture

import short_it.app
import short_it.exc


class TestMainLogic:
    """Tests for :func:`short_it.app.find_and_redirect_to_the_link` function."""

    @pytest.mark.parametrize("link_type_is_none", [True, False])
    def test_success(self, mocker: MockerFixture, faker: Faker, link_type_is_none: bool) -> None:
        """Test for the success case."""
        mocked = mocker.patch("short_it.app.parse_config.ParseConfigToMachineData").return_value
        mocked_redirect_response = mocker.patch("fastapi.responses.RedirectResponse")
        mocked.get_url.return_value = faker.uri()
        project_name, link_type = faker.word(), None if link_type_is_none else faker.word()

        assert (
            short_it.app.find_and_redirect_to_the_link(project_name, link_type) == mocked_redirect_response.return_value
        )

        mocked.get_url.assert_called_once_with(project_name, link_type)
        mocked_redirect_response.assert_called_once_with(url=mocked.get_url.return_value)

    @pytest.mark.parametrize("link_type_is_none", [True, False])
    def test_not_found(self, mocker: MockerFixture, faker: Faker, link_type_is_none: bool) -> None:
        """Test for the case when something is not found."""
        mocked = mocker.patch("short_it.app.parse_config.ParseConfigToMachineData").return_value
        mocked.get_url.return_value = None
        project_name, link_type = faker.word(), None if link_type_is_none else faker.word()

        with pytest.raises(fastapi.HTTPException) as exception:
            short_it.app.find_and_redirect_to_the_link(project_name, link_type)
        assert exception.value.status_code == 404

        mocked.get_url.assert_called_once_with(project_name, link_type)

    @pytest.mark.parametrize("link_type_is_none", [True, False])
    def test_invalid_args_error(self, mocker: MockerFixture, faker: Faker, link_type_is_none: bool) -> None:
        """Test for the case when invalid args were specified."""
        mocked = mocker.patch("short_it.app.parse_config.ParseConfigToMachineData").return_value
        mocked_text_response = mocker.patch("fastapi.responses.PlainTextResponse")
        project_name, link_type, exception_msg = (
            faker.word(),
            None if link_type_is_none else faker.word(),
            faker.sentence(),
        )
        mocked.get_url.side_effect = short_it.exc.ShortItException(exception_msg)

        assert short_it.app.find_and_redirect_to_the_link(project_name, link_type) == mocked_text_response.return_value

        mocked.get_url.assert_called_once_with(project_name, link_type)
        mocked_text_response.assert_called_once_with(exception_msg)


class TestRoutes:
    """Tests for our routes."""

    def test_project_route(self, mocker: MockerFixture, faker: Faker) -> None:
        """Test for the project link route."""
        mocked = mocker.patch("short_it.app.find_and_redirect_to_the_link")
        project_name, link_type = faker.word(), faker.word()
        assert short_it.app.route_project_link(project_name, link_type) == mocked.return_value
        mocked.assert_called_once_with(project_name, link_type)

    def test_simple_route(self, mocker: MockerFixture, faker: Faker) -> None:
        """Test for the simple link route."""
        mocked = mocker.patch("short_it.app.find_and_redirect_to_the_link")
        link_type = faker.word()
        assert short_it.app.route_simple_link(link_type) == mocked.return_value
        mocked.assert_called_once_with(link_type, None)
