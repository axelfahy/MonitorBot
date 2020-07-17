# -*- coding: utf-8 -*-
"""Telegram bot for monitoring.

This module get the wanted information and reports it.

For example, recover the RAM or SWAP usage and
send a warning on the channel if the threshold is exceeded.
"""
from datetime import datetime
import logging
import time
import subprocess
from typing import Optional, Sequence

import telegram

from . import (HOSTNAME,
               TELEGRAM_KEY,
               SLEEP_BETWEEN_MSG,
               SLEEP_TIME)

LOGGER = logging.getLogger(__name__)


def delete_messages(bot: telegram.bot, messages: Sequence[telegram.Message]) -> None:
    """
    Delete all the messages sent.

    Parameters
    ----------
    bot: telegram.bot
        Bot used to remove the messages.
    messages : Sequence of messages
        List of messages to delete.
    """
    for msg in messages:
        bot.deleteMessage(chat_id=msg.chat.id, message_id=msg.message_id)


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


def run(channel: str, cmd: str, threshold: float, metric: str = 'Metric') -> None:
    """
    Scan the wanted information every X minutes and report any issues on the channel.

    Parameters
    ----------
    channel : str
        Channel's ID to send the messages to.
    cmd : str
        Command to execute using subprocess, should return a float.
        Symbol such as '|', '$' must be escaped using '\'. The escape character will be removed
        afterwars so it must not be in the final command.
    threshold : float
        Threshold to send a message, if the output of `cmd` is higher than the threshold.
    metric : str, default 'Metric'
        Metric being watched, used in the message to send.
    """
    bot = telegram.Bot(token=TELEGRAM_KEY)
    messages = []

    while True:
        ps = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        out = ps.communicate()[0].decode('utf-8')
        print(out)

        try:
            value = float(out)
        except ValueError as e:
            LOGGER.error(f'Value {out} is not a number: {e}')
        else:
            # If RAM or SWAP above given percentage, send message.
            if value > threshold:
                messages.append(
                    send_message(
                        bot,
                        channel,
                        f'*{HOSTNAME}*: {metric} is above threshold (*{value}*/{threshold})'))
                time.sleep(SLEEP_BETWEEN_MSG)
        time.sleep(SLEEP_TIME)


def send_message(bot: telegram.Bot, channel: str, text: str,
                 parse_mode: str = 'Markdown') -> Optional[telegram.Message]:
    """
    Send a message on the channel.

    Handles possible exception and return the send message.

    Parameters
    ----------
    bot : telegram.Bot
        Bot object containing the API key.
    channel : str
        Channel's ID to send the messages to.
    text : str
        Text to send.
    parse_mode : str, default `Markdown`
        Mode for the parsing.

    Returns
    -------
    telegram.Message
        The message object from the telegram api, containing the chat and message id.
    """
    try:
        msg = bot.sendMessage(
            chat_id=channel,
            text=text,
            parse_mode=parse_mode)
    except (telegram.vendor.ptb_urllib3.urllib3.exceptions.ReadTimeoutError,
            telegram.error.TimedOut) as e:
        LOGGER.error(f'Error when sending message {text} on channel {channel}: {e}')
        return None
    else:
        return msg
