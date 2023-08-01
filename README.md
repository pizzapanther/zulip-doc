# Zulip Duty of Care Service

A small script to check user presence in Zulip. If a user hasn't been around for a while it will send you a message in Zulip so you can check up on them and see if they are ok.

## Install

`pipx install zulip-doc`

## Usage

```
Usage: zdoc [OPTIONS] [SEND_TO]...

Arguments:
  [SEND_TO]...

Options:
  --max-idle INTEGER              [env var: MAX_IDLE; default: 86400]
  --ignore-weekends / --no-ignore-weekends
                                  [env var: IGNORE_WEEKENDS; default: ignore-
                                  weekends]
  --config-file FILE              [env var: CONFIG_FILE; default:
                                  /home/{username}/.zuliprc]
  --help                          Show this message and exit.
```

Example: `zdoc 12 22`
