"""Cmdline"""
import click
from click import Context

from crawl_foreign_business_data import __version__
from crawl_foreign_business_data.runer import (australia_runer, russia_runer,
                                               spain_runer)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-V', '--version', is_flag=True, help='Show version and exit.')
def main(ctx: Context, version: str):
    """Main commands"""

    if version:
        click.echo(__version__)

    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.option(
    '-n', '--name',
    help='选择要抓取的国家名称 Russia（俄罗斯）、Spain（西班牙）、Australia（新西兰和澳大利亚）')
def crawl(name: str):
    """
    open crawler  "crawler --help"  show more help
    """
    if 'Australia' in name:
        australia_runer()

    if 'Russia' in name:
        russia_runer()

    if 'Spain' in name:
        spain_runer()


if __name__ == '__main__':
    main()
