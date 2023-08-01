#!/usr/bin/env python3

import datetime
import os
import time

from pathlib import Path
from typing import List

import humanize
import typer
import zulip

CONFIG_FILE_PATH = Path(os.environ['HOME']) / '.zuliprc'
CONFIG_OPTION = typer.Option(
  default=CONFIG_FILE_PATH,
  exists=True,
  file_okay=True,
  dir_okay=False,
  writable=False,
  readable=True,
  resolve_path=True,
  envvar="CONFIG_FILE",
)

MAX_IDLE_OPTION = typer.Option(default= 24 * 60 * 60, envvar="MAX_IDLE")
IGNORE_WEEKENDS_OPTION = typer.Option(True, envvar="IGNORE_WEEKENDS")


def main(
    send_to: List[int] = typer.Argument(None),
    max_idle: int = MAX_IDLE_OPTION,
    ignore_weekends: bool = IGNORE_WEEKENDS_OPTION,
    config_file: Path = CONFIG_OPTION
  ):
  client = zulip.Client(config_file=config_file)

  now = time.time()
  today = datetime.date.today()
  idle_users = []

  if ignore_weekends:
    if today.weekday() in [6, 5]:
      # don't run check on Sat and Sun
      return

    elif today.weekday() == 0:
      # on Monday ignore Sat and Sun
      max_idle = (2 * 24 * 60 * 60) + max_idle

  result = client.get_realm_presence()
  for user, p in result["presences"].items():
    presence = p["aggregated"]
    if presence["status"] == "idle":
      old = now - presence['timestamp']
      if old > max_idle:
        idle_users.append(user)

  if idle_users:
    timeframe = humanize.naturaldelta(datetime.timedelta(seconds=max_idle))
    users = ", ".join(idle_users)
    request = {
      "type": "private",
      "to": send_to,
      "content": f"**The following user have been offline for more than {timeframe}:**\n{users}",
    }
    print(f"Sending Idle Users: {len(idle_users)}")
    result = client.send_message(request)

  else:
    print("No Idle Users")

def app():
  typer.run(main)

if __name__ == "__main__":
  typer.run(main)
