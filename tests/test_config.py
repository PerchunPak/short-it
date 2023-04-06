"""Tests for :mod:`short_it.config` module."""
import typing as t

import pytest
from faker import Faker

import short_it.config


class TestLinkSettings:
    """Tests for :class:`short_it.config.LinkSettings` class."""

    @pytest.mark.parametrize(
        "alias, expected",
        [
            ("github", "github"),
            ("gh", "github"),
            ("read-the-docs", "read-the-docs"),
            ("readthedocs", "read-the-docs"),
            ("rtd", "read-the-docs"),
            ("docs", "docs"),
            ("wiki", "docs"),
            ("random", None),
        ],
    )
    @pytest.mark.parametrize("aliases_are_set", [True, False])
    def test_add_builtin_aliases(
        self,
        faker: Faker,
        alias: t.Literal["random"] | str,
        expected: t.Literal["github", "read-the-docs", "docs"] | None,
        aliases_are_set: bool,
    ) -> None:
        """Test for :meth:`short_it.config.LinkSettings.add_builtin_aliases` method."""
        if aliases_are_set:
            expected_value = faker.pylist()
        else:
            expected_value = {
                "github": ["github", "gh", "git", "src", "sources", "source", "vcs"],
                "read-the-docs": ["rtd", "readthedocs", "read-the-docs", "docs", "wiki"],
                "docs": ["docs", "wiki", "documentation"],
                None: None,
            }[expected]

        instance = short_it.config.LinkSettings(aliases=expected_value if aliases_are_set else None)
        instance.add_builtin_aliases(alias if alias != "random" else faker.word())
        assert instance.aliases == expected_value
