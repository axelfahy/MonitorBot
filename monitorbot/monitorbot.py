# -*- coding: utf-8 -*-
"""Bot for monitoring.

This module get the wanted information and reports it.

For example, recover the RAM or SWAP usage and
send a warning on the channel if the threshold is exceeded.
"""
from datetime import datetime
import logging
import time
import subprocess

import pymsteams

from . import (HOSTNAME,
               SLEEP_BETWEEN_MSG,
               SLEEP_TIME)

LOGGER = logging.getLogger(__name__)


def format_date(date_str: str) -> str:
    """
    Parse the date from a given format to another.

    Used to send a correct format of date in the message.

    Parameters
    ----------
    date_str : str
        Date from the JSON, format: '%Y-%m-%dT%H:%M:%S%z'

    Returns
    -------
    str
        Date formatted for the message, format: '%Y-%m-%d %H:%M:%S UTC'
    """
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S UTC')


def run(hookurl: str, cmd: str, threshold: float, metric: str = 'Metric') -> None:
    """
    Scan the wanted information every X minutes and report any issues on the channel.

    Parameters
    ----------
    hookurl : str
        URL of the Teams webhook.
    cmd : str
        Command to execute using subprocess, should return a float.
        Symbol such as '|', '$' must be escaped using '\'. The escape character will be removed
        afterwars so it must not be in the final command.
    threshold : float
        Threshold to send a message, if the output of `cmd` is higher than the threshold.
    metric : str, default 'Metric'
        Metric being watched, used in the message to send.
    """
    while True:
        ps = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        out = ps.communicate()[0].decode('utf-8')

        try:
            value = float(out)
        except ValueError as e:
            LOGGER.error(f'Value {out} is not a number: {e}')
        else:
            # If RAM or SWAP above given percentage, send message.
            if value > threshold:
                msg = f'*{HOSTNAME}*: {metric} is above threshold (*{value}*/{threshold})'
                status = send_message(hookurl, msg)
                LOGGER.info(f'Sent message {msg} with status {status}')
                time.sleep(SLEEP_BETWEEN_MSG)
        time.sleep(SLEEP_TIME)


def send_message(hookurl: str, text: str) -> int:

    """
    Send a message on the channel of the Teams.

    The HTTP status is returned.

    parameters
    ----------
    hookurl : str
        URL for the hook to the Teams' channel.
    text : str
        text to send.

    returns
    -------
    int
        HTTP status from the sent message.
    """
    msg = pymsteams.connectorcard(hookurl)
    msg.text(text)
    msg.send()
    return msg.last_http_status.status_code
