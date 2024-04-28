import json
import logging
from application import Application


def load_json_file(filename: str) -> dict:
    with open(filename, 'r') as file:
        contents = file.read()
        return json.loads(contents)
    

def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    
    # Load the settings for the application
    socket_settings = load_json_file("C:/Users/George Taylor/Documents/StudyChat/client/socket_settings.json")
    app_settings = load_json_file("C:/Users/George Taylor/Documents/StudyChat/client/app_settings.json")
    
    # Start the application
    Application(socket_settings=socket_settings, app_settings=app_settings)
    

if __name__ == '__main__':
    main()
