import io
from typing import BinaryIO, Optional

import pytest

from scaraplate.strategies import PythonTemplateHash, TemplateHash
from scaraplate.template import TemplateMeta


@pytest.mark.parametrize(
    "template, target, is_git_dirty, out",
    [
        (
            "from template!",
            None,
            False,
            "from template!\n"
            "# Generated by https://github.com/rambler-digital-solutions/scaraplate\n"
            "# From https://github.com/rambler-digital-solutions/scaraplate-example-template"
            "/commit/1111111111111111111111111111111111111111\n",
        ),
        (
            "from template!",
            "from target!",
            False,
            "from template!\n"
            "# Generated by https://github.com/rambler-digital-solutions/scaraplate\n"
            "# From https://github.com/rambler-digital-solutions/scaraplate-example-template"
            "/commit/1111111111111111111111111111111111111111\n",
        ),
        (
            "from template!",
            "from target!\n"
            "# Generated by https://github.com/rambler-digital-solutions/scaraplate\n"
            "# From https://github.com/rambler-digital-solutions/scaraplate-example-template"
            "/commit/1111111111111111111111111111111111111111\n",
            False,
            "from target!\n"
            "# Generated by https://github.com/rambler-digital-solutions/scaraplate\n"
            "# From https://github.com/rambler-digital-solutions/scaraplate-example-template"
            "/commit/1111111111111111111111111111111111111111\n",
        ),
        (
            "from template!",
            "from target!\n"
            "# Generated by https://github.com/rambler-digital-solutions/scaraplate\n"
            "# From https://github.com/rambler-digital-solutions/scaraplate-example-template"
            "/commit/0000000000000000000000000000000000000000\n",
            False,
            "from template!\n"
            "# Generated by https://github.com/rambler-digital-solutions/scaraplate\n"
            "# From https://github.com/rambler-digital-solutions/scaraplate-example-template"
            "/commit/1111111111111111111111111111111111111111\n",
        ),
        (
            "from template!",
            "from target!\n"
            "# Generated by https://github.com/rambler-digital-solutions/scaraplate\n"
            "# From (dirty) https://github.com/rambler-digital-solutions/scaraplate-example-template"
            "/commit/1111111111111111111111111111111111111111\n",
            True,
            "from template!\n"
            "# Generated by https://github.com/rambler-digital-solutions/scaraplate\n"
            "# From (dirty) https://github.com/rambler-digital-solutions/scaraplate-example-template"
            "/commit/1111111111111111111111111111111111111111\n",
        ),
    ],
)
def test_template_hash(template, target, is_git_dirty, out):
    if target is not None:
        target_contents: Optional[BinaryIO] = io.BytesIO(target.encode())
    else:
        target_contents = None

    template_contents = io.BytesIO(template.encode())

    strategy = TemplateHash(
        target_contents=target_contents,
        template_contents=template_contents,
        template_meta=TemplateMeta(
            gitlab_project_url="https://github.com/rambler-digital-solutions/scaraplate-example-template",
            commit_hash="1111111111111111111111111111111111111111",
            commit_url=(
                "https://github.com/rambler-digital-solutions/scaraplate-example-template"
                "/commit/1111111111111111111111111111111111111111"
            ),
            is_git_dirty=is_git_dirty,
        ),
    )

    assert out == strategy.apply().read().decode()


@pytest.mark.parametrize(
    "template, target, out",
    [
        (
            "from template!",
            None,
            "from template!\n"
            "# Generated by https://github.com/rambler-digital-solutions/scaraplate\n"
            "# From https://github.com/rambler-digital-solutions/scaraplate-example-template"
            "/commit/1111111111111111111111111111111111111111  # noqa\n",
        )
    ],
)
def test_python_template_hash(template, target, out):
    if target is not None:
        target_contents: Optional[BinaryIO] = io.BytesIO(target.encode())
    else:
        target_contents = None

    template_contents = io.BytesIO(template.encode())

    strategy = PythonTemplateHash(
        target_contents=target_contents,
        template_contents=template_contents,
        template_meta=TemplateMeta(
            gitlab_project_url="https://github.com/rambler-digital-solutions/scaraplate-example-template",
            commit_hash="1111111111111111111111111111111111111111",
            commit_url=(
                "https://github.com/rambler-digital-solutions/scaraplate-example-template"
                "/commit/1111111111111111111111111111111111111111"
            ),
            is_git_dirty=False,
        ),
    )

    assert out == strategy.apply().read().decode()
