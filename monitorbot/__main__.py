# -*- coding: utf-8 -*-
"""Entry point of the monitor cli."""
import click

from . import (DEFAULT_CMD,
               DEFAULT_METRIC,
               DEFAULT_THRESHOLD,
               HOOKURL)

from .monitorbot import run


@click.command()
@click.option('--url', '-u',
              default=HOOKURL, show_default=False,
              help="URL for the Teams' webhook."
              )
@click.option('--cmd', '-c',
              default=DEFAULT_CMD, show_default=True,
              help='Command to execute, should return a number.'
              )
@click.option('--threshold', '-t',
              default=DEFAULT_THRESHOLD, show_default=True,
              help='Threshold to raise an alarm and send a message.'
              )
@click.option('--metric', '-m',
              default=DEFAULT_METRIC, show_default=True,
              help='Metric to watch.'
              )
def main(url: str, cmd: str, threshold: float, metric: str):
    """CLI for monitoring.

    Parameters
    ----------
    url:  str
        URL for the Teams' webhook.
    cmd : str
        Command to execute using subprocess, should return a float.
    threshold : float
        Threshold to send a message, if the output of `cmd` is higher than the threshold.
    metric : str, default 'Metric'
        Metric being watched, used in the message to send.

    Examples
    --------
    $ monitor
    """
    # Remove the escaped character.
    cmd = cmd.replace('\\', '')
    run(url, cmd, threshold, metric)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
