from enum import Enum
from typing import Any, TypedDict, Union


class UserStates(Enum):
    ONLINE = 'Online'
    OFFLINE = 'Offline'


class MessageDetails(TypedDict):
    first_name: str
    last_name: str
    date_sent: str
    body: str


class UserDetails(TypedDict):
    first_name: str
    last_name: str
    email: str
    password: str
    tutor_group: str
    option_one: str
    option_two: str
    option_three: str
    option_four: str
    points: int
    
    
class QuestionDetails(TypedDict):
    title: str
    subject: str
    description: str
    expires_date: str
    second_year_content: bool


class QuestionStatistics(TypedDict):
    recipient_ammount: int
    recipient_awnsers: int


class SocketCommand(TypedDict):
    command_name: str 
    arguments: dict[str, Any]