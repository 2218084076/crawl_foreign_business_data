"""Test cmdline"""
from typing import List

import pytest
from click.testing import CliRunner

from crawl_foreign_business_data import __version__, cmdline


@pytest.mark.parametrize(
    ['invoke_args', 'exit_code', 'output_keyword'],
    [
        ([''], 2, 'help'),
        (['--help'], 0, 'help'),
        (['--version'], 0, __version__),
        (['-V'], 0, __version__),
    ]
)
def test_main(
        clicker: CliRunner,
        invoke_args: List[str],
        exit_code: int,
        output_keyword: str
):
    """test_main"""
    result = clicker.invoke(cmdline.main, invoke_args)
    assert result.exit_code == exit_code
    assert output_keyword in result.output
