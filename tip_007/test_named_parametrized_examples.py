import re

import pytest

REDIRECT_REGEX = r"(^/([A-Za-z0-9#&?=]+|$)|^https://my.domain\.com/[A-Za-z0-9#&?=/]*$)"


def is_valid_success_url(url: str) -> bool:
    return bool(re.match(REDIRECT_REGEX, url))


@pytest.mark.parametrize(
    "success_url",
    [
        pytest.param(
            "/",
            id="relative_root",
        ),
        pytest.param(
            "/some/path",
            id="relative_path",
        ),
        pytest.param(
            "/?foo=bar",
            id="relative_root_with_query_param",
        ),
        pytest.param(
            "/?foo=bar",
            id="relative_path_with_query_param",
        )
    ]
)
def test_is_valid_success_url(success_url: str):

    assert is_valid_success_url(success_url) is True


@pytest.mark.parametrize(
    "success_url",
    [
        pytest.param(
            "https://somewhere-else.com",
            id="non_whitelisted_domain",
        ),
        pytest.param(
            "https://somewhere-else.com",
            id="non_whitelisted_domain",
        ),
        pytest.param(
            "https://mydomain.com@bad-boy.com/",
            id="domain_change",
        ),
        pytest.param(
            "https://mydomain.com/settings>\r\nBCC:hrtstjyww456yeh@gsd.com\r\npda: m",
            id="malicious_url",
        ),
        pytest.param(
            "//settings",
            id="double_slash",
        ),
    ]
)
def test_not_valid_success_url(success_url: str):

    assert is_valid_success_url(success_url) is False