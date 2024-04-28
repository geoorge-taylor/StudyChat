from enum import Enum
from typing import Any, TypedDict, Union

from static.shared_types import *


class InboundCommands(Enum):
    RegisterResponse = 'register-response'
    VerifyResponse = 'verify-response'
    LoginResponse = 'login-response'
    LoadUserDetails = 'load-user-details'
    AskQuestionResponse = 'ask-question-response'
    AddPendingQuestion = 'add-pending-question'
    AddIncomingQuestion = 'add-incoming-question'
    CreateProfileViewer = 'create-profile-viewer'
    CreateNewChat = 'create-new-chat'
    CreateChatReply = 'create-chat-reply'
    DeletePendingQuestion = 'delete-pending-question'
    LoadFile = 'load-file'
    CreateManualUser = 'create-manual-user'
    UpdateQuestionStatistics = 'update-question-statistics'
    DeleteQuestionChat = 'delete-question-chat'
    DeleteIncomingQuestion = 'delete-incoming-question'
    DisplayRatingError = 'display-rating-error'

    @staticmethod
    def has_command(item: Any):
        return item in [v.value for v in InboundCommands.__members__.values()]


class OutboundCommands:
    @staticmethod
    def register(user_details: UserDetails) -> SocketCommand:
        return {'command_name': 'register', 'arguments': {'user_details': user_details}}
    
    @staticmethod
    def verify(code: str) -> SocketCommand:
        return {'command_name': 'verify', 'arguments': {'code': code}}

    @staticmethod
    def login(email: str, password: str) -> SocketCommand:
        return {'command_name': 'login', 'arguments': {'email': email, 'password': password}}

    @staticmethod
    def sign_out() -> SocketCommand:
        return {'command_name': 'sign-out', 'arguments': {}}

    @staticmethod
    def ask_question(question_details: QuestionDetails, manual_recipients: list[int] = []) -> SocketCommand:
        return {'command_name': 'ask-question', 'arguments': {'manual_recipients': manual_recipients, 'question_details': question_details}}
    
    @staticmethod
    def view_user_profile(user_id: int) -> SocketCommand:
        return {'command_name': 'view-user-profile', 'arguments': {'user_id': user_id}}
        
    @staticmethod
    def create_new_chat_request(question_id: int, user_id: int) -> SocketCommand:
        return {'command_name': 'create-new-chat-request', 'arguments': {'user_id': user_id, 'question_id': question_id}}
    
    @staticmethod
    def send_message_request(chat_id: int, body: str) -> SocketCommand:
        return {'command_name': 'send-message-request', 'arguments': {'chat_id': chat_id, 'body': body}}
    
    @staticmethod
    def send_file_request(chat_id: int, contents: str, file_name: str, file_size: int, end: bool) -> SocketCommand:
        return {'command_name': 'send-file-request', 'arguments': {'chat_id': chat_id, 'contents': contents, 'file_name': file_name, 'file_size': file_size, 'end': end}}
    
    @staticmethod
    def delete_pending_question_request(question_id: int) -> SocketCommand:
        return {'command_name': 'delete-pending-question-request', 'arguments': {'question_id': question_id}}
    
    @staticmethod
    def delete_incoming_question_request(question_id: int) -> SocketCommand:
        return {'command_name': 'delete-incoming-question-request', 'arguments': {'question_id': question_id}}

    @staticmethod
    def search_for_user(input: str) -> SocketCommand:
        return {'command_name': 'search-for-user', 'arguments': {'input': input}}
    
    @staticmethod
    def end_chat_request_as_publisher(chat_id: int, rating: str) -> SocketCommand:
        return {'command_name': 'end-chat-as-publisher', 'arguments': {'chat_id': chat_id, 'rating': rating}}
    
    @staticmethod
    def end_chat_request_as_recipient(chat_id: int) -> SocketCommand:
        return {'command_name': 'end-chat-as-recipient', 'arguments': {'chat_id': chat_id}}
    