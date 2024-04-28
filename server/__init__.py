import json
import logging
from typing import Any

from _server import Server


def load_json(filename: str) -> dict[str, Any]:
    with open(filename, "r") as file:
        contents = file.read()
        return json.loads(contents)


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    settings = load_json("C:/Users/George Taylor/Documents/StudyChat/server/settings.json")
    Server(server_settings=settings['server'], socket_settings=settings['socket'], 
           database_connector_settings=settings['database_connector'], mail_settings=settings['mail'])


if __name__ == "__main__":
    main()
