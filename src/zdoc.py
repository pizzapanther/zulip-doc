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

MAX_IDLE_OPTION = typer.Option(default= 24 * 60 * 60)

def main(
    send_to: List[int] = typer.Argument(None),
    max_idle: int = MAX_IDLE_OPTION,
    config_file: Path = CONFIG_OPTION
  ):
  client = zulip.Client(config_file=config_file)

  now = time.time()
  idle_users = []

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
    result = client.send_message(request)

if __name__ == "__main__":
  typer.run(main)
