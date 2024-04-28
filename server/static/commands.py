from enum import Enum
from typing import Any, TypedDict, Union

from static.shared_types import (
    MessageDetails,
    QuestionDetails,
    QuestionStatistics,
    SocketCommand,
    UserDetails,
)


class InboundCommands(Enum):
    Register = "register"
    Verify = "verify"
    Login = "login"
    AskQuestion = 'ask-question'
    ViewUserProfile = 'view-user-profile'
    CreateNewChatRequest = 'create-new-chat-request'
    SendMessageRequest = 'send-message-request'
    DeletePendingQuestionRequest = 'delete-pending-question-request'
    SendFileRequest = 'send-file-request'
    SearchForUser = 'search-for-user'
    EndChatAsPublisher = 'end-chat-as-publisher'
    EndChatAsRecipient = 'end-chat-as-recipient'
    DeleteIncomingQuestionRequest = 'delete-incoming-question-request'

    @staticmethod
    def has_command(item: Any):
        return item in [v.value for v in InboundCommands.__members__.values()]


class OutboundCommands:
    @staticmethod
    def register_response(accepted: bool = True, reason: str = '') -> SocketCommand:
        return {
            "command_name": "register-response",
            "arguments": {"accepted": accepted, "reason": reason},
        }

    @staticmethod
    def verify_response(accepted: bool = True, reason: str = '') -> SocketCommand:
        return {
            "command_name": "verify-response",
            "arguments": {"accepted": accepted, "reason": reason},
        }

    @staticmethod
    def login_response(accepted: bool = True, reason: str = '') -> SocketCommand:
        return { 
            "command_name": "login-response",
            "arguments": {"accepted": accepted, "reason": reason},
        }

    @staticmethod
    def ask_question_response(accepted: bool = True, reason: str = '') -> SocketCommand:
        return {
            "command_name": "ask-question-response",
            "arguments": {"accepted": accepted, "reason": reason},
        }
    
    @staticmethod
    def add_pending_question(question_id: int, details: QuestionDetails, statistics: QuestionStatistics) -> SocketCommand:
        return {
            "command_name": "add-pending-question",
            "arguments": {"question_id": question_id, "question_details": details, "question_statistics": statistics},
        }
  
    @staticmethod
    def add_incoming_question(question_id: int, publisher_id: int, first_name: str, last_name: str, details: QuestionDetails) -> SocketCommand:
        return {
            "command_name": "add-incoming-question",
            "arguments": {"question_id": question_id, "publisher_id": publisher_id, 
                          "first_name": first_name, "last_name": last_name, "question_details": details},
        }
    
    @staticmethod
    def load_user_details(user_id: Any, user_details: UserDetails, user_status: str) -> SocketCommand:
        return {
            "command_name": "load-user-details",
            "arguments": {"user_id": user_id, "user_details": user_details, "user_status": user_status},
        }

    @staticmethod
    def create_profile_viewer(user_details, user_status) -> SocketCommand:
        return {
            "command_name": "create-profile-viewer",
            "arguments": {"user_details": user_details, "user_status": user_status},
        } 
    
    @staticmethod
    def create_new_chat(chat_id, user_id, first_name, last_name, question_details: QuestionDetails, question_publisher: bool) -> SocketCommand:
        return {
            "command_name": "create-new-chat",
            "arguments": {"user_id": user_id, "chat_id": chat_id, "first_name": first_name, 
                          "last_name": last_name, "question_details": question_details, "question_publisher": question_publisher},
        } 
    
    @staticmethod
    def create_chat_reply(chat_id: int, message_details: MessageDetails) -> SocketCommand:
        return {
            "command_name": "create-chat-reply",
            "arguments": {"chat_id": chat_id, "message_details": message_details},
        } 

    @staticmethod
    def delete_pending_question(question_id: int) -> SocketCommand:
        return {
            "command_name": "delete-pending-question",
            "arguments": {"question_id": question_id},
        }  

    @staticmethod
    def delete_incoming_question(question_id: int) -> SocketCommand:
        return {
            "command_name": "delete-incoming-question",
            "arguments": {"question_id": question_id},
        }  

    @staticmethod
    def delete_question_chat(chat_id: int) -> SocketCommand:
        return {
            "command_name": "delete-question-chat",
            "arguments": {"chat_id": chat_id},
        }  
    
    @staticmethod
    def load_file(chat_id: int, file_name: str, contents: str, file_size: int, end: bool) -> SocketCommand:
        return {
            "command_name": "load-file",
            "arguments": {"chat_id": chat_id, "file_name": file_name, 
                          "contents": contents, 'file_size': file_size, 'end': end},
        }  
    
    @staticmethod
    def create_manual_user(user_id: int, first_name: str, last_name: str, user_status: str) -> SocketCommand:
        return {
            "command_name": "create-manual-user",
            "arguments": {"user_id": user_id, "first_name": first_name, 
                          "last_name": last_name, 'status': user_status},
        }  
    
    @staticmethod
    def update_question_statistics(question_id: int, question_statistics: QuestionStatistics) -> SocketCommand:
        return {
            "command_name": "update-question-statistics",
            "arguments": {"question_id": question_id, "question_statistics": question_statistics}
        }  

    
    @staticmethod
    def display_rating_error(chat_id: int, reason: str) -> SocketCommand:
        return {
            "command_name": "display-rating-error",
            "arguments": {"chat_id": chat_id, "reason": reason}
        }  