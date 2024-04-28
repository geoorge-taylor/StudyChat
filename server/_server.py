import base64
import logging
from datetime import datetime
from typing import Any, Optional, Union

from database import chats, database_connector, questions, users_table
from networking.server_socket import ServerSocket, User
from services.mail import EmailManager
from static import utils
from static.commands import InboundCommands, OutboundCommands
from static.shared_types import (
    MessageDetails,
    QuestionDetails,
    QuestionStatistics,
    SocketCommand,
    UserDetails,
)

SPACE = " "
EMPTY = ""
FORMAT = '%Y-%m-%d'
MESSAGE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
USER_STATUS_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
SPECIAL_CHARACTERS = "!@#$%^&*()-+?_=,<>/"


# Prevent boiler plate code above most server methods
def session_active(func):
    def wrapper(_, user: User, *args, **kwargs):
        if user.session_active: 
            return func(_, user, *args, **kwargs)
        else: return
    return wrapper


class Server:
    def __init__(self, server_settings: dict[str, Any], socket_settings: dict[str, Any],
                 database_connector_settings: dict[str, Any], mail_settings: dict[str, Any]) -> None:
        
        # Initiate attributes
        self.settings = server_settings
        self.file_buffers: dict[int, dict[str, bytes]] = dict()

        # Create the map for the clients commands to their respective methods
        self.command_map = {
            InboundCommands.Register.value: self.handle_register_request,
            InboundCommands.Verify.value: self.handle_verify_request,
            InboundCommands.Login.value: self.handle_login_request,
            InboundCommands.AskQuestion.value: self.handle_question_request,
            InboundCommands.ViewUserProfile.value: self.handle_view_profile_request,
            InboundCommands.CreateNewChatRequest.value: self.handle_create_chat_request,
            InboundCommands.SendMessageRequest.value: self.handle_message_request,
            InboundCommands.DeletePendingQuestionRequest.value: self.handle_delete_pending_question_request,
            InboundCommands.SendFileRequest.value: self.handle_send_file_request,
            InboundCommands.SearchForUser.value: self.handle_search_for_user_request,
            InboundCommands.EndChatAsPublisher.value: self.handle_end_chat_as_publisher_request,
            InboundCommands.EndChatAsRecipient.value: self.handle_end_chat_as_recipient_request,
            InboundCommands.DeleteIncomingQuestionRequest.value: self.handle_delete_incoming_question_request
        }

        # Create the email manager used for sending verification emails
        self.email_manager = EmailManager(
            smtp_port=mail_settings['smtp_port'], 
            smtp_server=mail_settings['smtp_server'], 
            sender_email=mail_settings['sender_email'],
            password=mail_settings['password'], 
            code_pool_size=mail_settings['code_pool_size'],
            valid_domain=mail_settings['valid_domain']
        )

        # Create the connection to the mysql database
        database_connector.DatabaseConnector.init_cursor(
            settings=database_connector_settings, 
            cursor_commit=True
        )

        # Create the server socket to allow connections and data transfer between clients
        self.server_socket = ServerSocket(
            server_private_key_path=socket_settings['server_private_key_path'], 
            client_public_key_path=socket_settings['client_public_key_path'],
            port=socket_settings['port'], 
            format=socket_settings['format'], 
            backlog=socket_settings['backlog'], 
            header_size=socket_settings['header_size'], 
            recv_callback=self.recv_command,
            user_disconnect_callback=self.handle_user_on_disconnect
        )


    def recv_command(self, user: User, command: SocketCommand) -> None:
        command_name, arguments = command.get("command_name"), command.get("arguments")
        if command_name and InboundCommands.has_command(command_name):
            try:
                self.command_map[command_name](user, **arguments)
            except (KeyError, TypeError) as err:
                print(err)


    @session_active
    def handle_send_file_request(self, user: User, chat_id: int, contents: str, file_name: str, file_size: int, end: bool) -> None:
        if not chats.check_user_in_chat(chat_id, user.user_id): return
        user_file_buffer = self.file_buffers[user.user_id]
        users_in_chat = chats.get_users_in_chat(chat_id)

        for user_in_chat in users_in_chat:
            for online_user in self.server_socket.user_connections.values():
                if online_user.user_id != user_in_chat[0]: continue
                command = OutboundCommands.load_file(chat_id, file_name, contents, file_size, end)
                online_user.send_command(command)

        if end:
            del user_file_buffer[file_name]
        else:
            base64_decoded = base64.b64decode(contents)
            if not user_file_buffer.get(file_name):
                user_file_buffer[file_name] = b""
            user_file_buffer[file_name] += base64_decoded


    @session_active
    def handle_delete_pending_question_request(self, user: User, question_id: int) -> None:
        # The user cannot delete a question that they have not created
        if not questions.check_user_published_question(question_id, user.user_id): return

        # Delete incoming questions for users with this question
        users_with_incoming_question = questions.get_question_recipients(question_id)
        for user_with_incoming_question in users_with_incoming_question:
            for online_user in self.server_socket.user_connections.values():
                if online_user.user_id != user_with_incoming_question[0]: continue
                delete_incoming_question = OutboundCommands.delete_incoming_question(question_id)
                online_user.send_command(delete_incoming_question)


        # Delete chats for users with this question
        users_with_question_chat = chats.get_users_from_question(question_id)
        for user_with_question_chat in users_with_question_chat:
            for online_user in self.server_socket.user_connections.values():
                if online_user.user_id != user_with_question_chat[0]: continue
                delete_question_chat = OutboundCommands.delete_question_chat(user_with_question_chat[1])
                online_user.send_command(delete_question_chat)


        # Delete pending question for the publisher + clean up database
        delete_pending_question = OutboundCommands.delete_pending_question(question_id)
        user.send_command(delete_pending_question)
        chats.delete_question_chats(question_id)
        questions.delete_question(question_id)

    
    @session_active
    def handle_delete_incoming_question_request(self, user: User, question_id: int) -> None:
        if not questions.check_user_has_question(question_id, user.user_id): return
        
        # only need to delete question from requesters inbox
        questions.delete_question_from_inbox(question_id)
        command = OutboundCommands.delete_incoming_question(question_id)
        user.send_command(command)

        publisher_id_result = questions.get_question_publisher(question_id)
        question_recipients = questions.get_question_recipients(question_id)
        question_awnsers = questions.get_question_awnsers(question_id)
        statistics: QuestionStatistics = {'recipient_ammount': len(question_recipients), 
                                          'recipient_awnsers': question_awnsers[0]}  
        
        # update statistics for person who made it
        update_command = OutboundCommands.update_question_statistics(question_id, statistics)
        for online_user in self.server_socket.user_connections.values():
            if online_user.user_id == publisher_id_result[0]: 
                online_user.send_command(update_command) 


    @session_active
    def handle_end_chat_as_recipient_request(self, user: User, chat_id: int) -> None:
        delete_chat = OutboundCommands.delete_question_chat(chat_id)
        if not chats.check_user_in_chat(chat_id, user.user_id): return
        elif chats.check_user_published_question(chat_id, user.user_id): return
        
        recipient_id = int()
        users_in_chat = chats.get_users_in_chat(chat_id)
        for user_id in users_in_chat:
            if not user_id[0] == user.user_id:
                recipient_id = user_id[0]
        
        for online_user in self.server_socket.user_connections.values():
            if online_user.user_id == recipient_id: 
                online_user.send_command(delete_chat)

        # tell the recipient to finally delete the chat        
        user.send_command(delete_chat)
        chats.delete_chat(chat_id)
        

    @session_active
    def handle_end_chat_as_publisher_request(self, user: User, chat_id: int, rating: str) -> None:
        delete_chat = OutboundCommands.delete_question_chat(chat_id)
        if not rating.isnumeric(): 
            user.send_command(OutboundCommands.display_rating_error(
                chat_id=chat_id, reason='Your rating must be a number')
            )
            return
        elif int(rating) > 5 or int(rating) < 0:
            user.send_command(OutboundCommands.display_rating_error(
                chat_id=chat_id, reason='Rating must be between 0 and 5')
            )
            return
        elif not chats.check_user_in_chat(chat_id, user.user_id):
            user.send_command(OutboundCommands.display_rating_error(
                chat_id=chat_id, reason='You are no longer part of this chat')
            )
            return
        elif not chats.check_user_published_question(chat_id, user.user_id):
            user.send_command(OutboundCommands.display_rating_error(
                chat_id=chat_id, reason='You did not publish this question')
            )
            return
        
        recipient_id = int()
        users_in_chat = chats.get_users_in_chat(chat_id)
        for user_id in users_in_chat:
            if not user_id[0] == user.user_id:
                recipient_id = user_id[0]

        for online_user in self.server_socket.user_connections.values():
            if online_user.user_id == recipient_id: 
                online_user.send_command(delete_chat)

        user.send_command(delete_chat)
        chats.delete_chat(chat_id)
        print(recipient_id)
        users_table.increment_users_points(recipient_id, int(rating))


    @session_active
    def handle_message_request(self, user: User, chat_id: int, body: str) -> None:
        # sanity checks first
        valid_user_in_chat = chats.check_user_in_chat(chat_id, user.user_id)
        if not valid_user_in_chat or body == EMPTY: return
        elif len(body) > self.settings['message_max_length']: return 

        chats.add_reply_to_chat(chat_id, user.user_id, body)
        users_in_chat = chats.get_users_in_chat(chat_id)
        date_now = datetime.now().strftime(MESSAGE_DATE_FORMAT)

        for user_in_chat in users_in_chat:
            for online_user in self.server_socket.user_connections.values():
                if online_user.user_id != user_in_chat[0]: continue
                command = OutboundCommands.create_chat_reply(chat_id, {
                    'first_name': user.user_details['first_name'],
                    'last_name': user.user_details['last_name'],
                    'date_sent': date_now, 'body': body
                })
                online_user.send_command(command)
                

    @session_active
    def load_user_messages(self, user: User) -> None:
        chat_ids = chats.get_users_chat_ids(user.user_id)
        for chat_id in chat_ids:
            messages = chats.get_chat_replies(chat_id[0])
            for message in messages:
                message_details: MessageDetails = {
                    'first_name': message[0], 'last_name': message[1],
                    'date_sent': message[2].strftime("%Y-%m-%d %H:%M:%S"), 
                    'body': message[3]
                }
                user.send_command(
                    OutboundCommands.create_chat_reply(
                        chat_id[0], message_details
                    )
                )


    @session_active
    def load_user_chats(self, user: User) -> None:
        chat_details_list = chats.load_user_chats(user.user_id)
        if chat_details_list:
            for chat_details in chat_details_list:
                user_id = chat_details[0]
                first_name = chat_details[1]
                last_name = chat_details[2]
                chat_id = chat_details[3]

                question = chats.get_chat_question(chat_id)
                has_published = questions.check_user_published_question(
                    question[0], user.user_id
                )
                question_details: QuestionDetails = {
                    'title': question[1],
                    'subject': question[2],
                    'description': question[3],
                    'expires_date': question[4].strftime(FORMAT),
                    'second_year_content': question[5]
                }

                user.send_command(
                    OutboundCommands.create_new_chat(
                        chat_id, user_id, first_name, 
                        last_name, question_details, has_published
                    )
                )


    @session_active
    def handle_create_chat_request(self, user: User, user_id: int, question_id: int) -> None:
        # 1. check if the user is valid to have a conversation with (has asked a question to them)
        # 2. insert their values into the converstaions table
        requester_has_question = questions.check_user_has_question(question_id, user.user_id)
        if not requester_has_question: return

        # get all the details for the question and chats
        chat_id = chats.create_new_chat(user_one=user.user_id, user_two=user_id, question_id=question_id)
        first_name, last_name = users_table.get_user_full_name(user_id)
        question = questions.get_question(question_id)
        questions.remove_incoming_question(question_id, user.user_id)

        question_details: QuestionDetails = {
            'title': question[2],
            'subject': question[3],
            'description': question[4],
            'expires_date': question[5].strftime(FORMAT),
            'second_year_content': question[6]
        }
        
        question_recipients = questions.get_question_recipients(question_id)
        question_awnsers = questions.get_question_awnsers(question_id)
        statistics: QuestionStatistics = {'recipient_ammount': len(question_recipients), 
                                          'recipient_awnsers': question_awnsers[0]}  
        

        for online_user in self.server_socket.user_connections.values():
            if not online_user.user_id == user_id: continue
            online_user.send_command(
                OutboundCommands.create_new_chat(
                    chat_id, user.user_id, 
                    user.user_details['first_name'], 
                    user.user_details['last_name'], 
                    question_details, True
                )
            )

            # Tell the user to update the info regarding their pending question
            online_user.send_command(
                OutboundCommands.update_question_statistics(
                    question_id=question_id, question_statistics=statistics
                )
            )

        # Tell the user to create a new chat
        user.send_command(
            OutboundCommands.create_new_chat(
                chat_id, user_id, first_name, 
                last_name, question_details, False
            )
        )
        user.send_command(
            OutboundCommands.delete_incoming_question(
                question_id=question_id
            )
        )


    @session_active
    def handle_view_profile_request(self, user: User, user_id: int) -> None:
        user_profile = users_table.get_user(user_id)
        if not user_profile: return
        user.send_command(
            OutboundCommands.create_profile_viewer(
                user_profile[0], user_profile[1]
            )
        )


    @session_active
    def handle_search_for_user_request(self, user: User, input: str) -> None:
        relavent_users = questions.get_users_from_input(input)
        for relavent_user in relavent_users:
            user.send_command(OutboundCommands.create_manual_user(
                user_id=relavent_user[0], first_name=relavent_user[1],
                last_name=relavent_user[2], user_status=relavent_user[3]
            ))


    @session_active
    def handle_question_request(self, user: User, manual_recipients: list[int], question_details: QuestionDetails) -> None:
        empty_feilds = utils.check_for_empty(question_details)
        if empty_feilds: 
            user.send_command(OutboundCommands.ask_question_response(
                accepted=False, reason='No empty fields allowed')
            )
            return
        elif not utils.validate_date(question_details['expires_date']):
            user.send_command(OutboundCommands.ask_question_response(
                accepted=False, reason='Date should be in format YYYY-MM-DD')
            )
            return   
        
        question_id: int = int()
        statistics: Optional[QuestionStatistics] = None

        # Logic for asking the queston
        if manual_recipients:
            question_id = questions.create_question_manual(
                user_ids=manual_recipients, publisher_id=user.user_id,
                details=question_details
            )

            question_recipients = questions.get_question_recipients(question_id)
            question_awnsers = questions.get_question_awnsers(question_id)
            statistics = {'recipient_ammount': len(question_recipients), 
                          'recipient_awnsers': question_awnsers[0]} 

            for user_affected in manual_recipients:
                if user_affected == user.user_id: continue
                for online_user in self.server_socket.user_connections.values():
                    if user_affected != online_user.user_id: continue
                    online_user.send_command(
                        OutboundCommands.add_incoming_question(
                            question_id=question_id,
                            publisher_id=user.user_id,
                            first_name=user.user_details['first_name'],
                            last_name=user.user_details['last_name'],
                            details=question_details
                        )
                    )
        else: 
            users_affected, question_id_result = questions.create_question_automatic(
                publisher_id=user.user_id, details=question_details
            )

            question_id = question_id_result[0] 
            question_recipients = questions.get_question_recipients(question_id)
            question_awnsers = questions.get_question_awnsers(question_id)
            statistics = {'recipient_ammount': len(question_recipients), 
                          'recipient_awnsers': question_awnsers[0]} 
            
            # send question commands to the users effected
            for user_affected in users_affected:
                # prevent sending question to the user who asked it
                if user_affected[0] == user.user_id: continue
                for online_user in self.server_socket.user_connections.values():
                    if user_affected[0] != online_user.user_id: continue
                    online_user.send_command(
                        OutboundCommands.add_incoming_question(
                            question_id=question_id,
                            publisher_id=user.user_id,
                            first_name=user.user_details['first_name'],
                            last_name=user.user_details['last_name'],
                            details=question_details
                        )
                    )

        user.send_command(OutboundCommands.ask_question_response())
        user.send_command(OutboundCommands.add_pending_question(
            question_id=question_id,
            details=question_details, 
            statistics=statistics)
        )


    @session_active
    def suggest_question_recipients(self, user: User) -> None:
        suggested_users = questions.get_suggested_users(user.user_id)
        for suggested_user in suggested_users:
            user.send_command(OutboundCommands.create_manual_user(
                user_id=suggested_user[0], first_name=suggested_user[1],
                last_name=suggested_user[2], user_status=suggested_user[3]
            ))


    @session_active
    def load_pending_questions(self, user: User) -> None:
        pending_questions = questions.get_pending_questions(user.user_id)
        if not pending_questions: self.__debug(user.address, 'No pending questions'); return 
        # send all the pending questions back to the user
        for question in pending_questions:
            question_details: QuestionDetails = {
                'title': question[2],
                'subject': question[3],
                'description': question[4],
                'expires_date': question[5].strftime(FORMAT),
                'second_year_content': question[6]
            }
            question_recipients = questions.get_question_recipients(question[0])
            question_awnsers = questions.get_question_awnsers(question[0])
            statistics: QuestionStatistics = {'recipient_ammount': len(question_recipients), 
                                              'recipient_awnsers': question_awnsers[0]} 
            
            user.send_command(
                OutboundCommands.add_pending_question(
                    question_id=question[0],
                    details=question_details,
                    statistics=statistics
                )
            )


    @session_active
    def load_incoming_questions(self, user: User) -> None:
        incoming_questions = questions.get_incoming_questions(user.user_id)
        if not incoming_questions: self.__debug(user.address, 'No incoming questions'); return 
        # send all the pending questions back to the user
        for question in incoming_questions:
            question_details: QuestionDetails = {
                'title': question[2],
                'subject': question[3],
                'description': question[4],
                'expires_date': question[5].strftime(FORMAT),
                'second_year_content': question[6]
            }
            publisher_full_name = users_table.get_user_full_name(question[1])
            user.send_command(
                OutboundCommands.add_incoming_question(
                    question_id=question[0],
                    publisher_id=question[1],
                    first_name=publisher_full_name[0],
                    last_name=publisher_full_name[1],
                    details=question_details
                )
            )


    def handle_user_on_disconnect(self, user: User) -> None:
        date_now = datetime.now().strftime(USER_STATUS_DATE_FORMAT)
        users_table.update_user_status(user.user_id, f'Last seen {date_now}')

    
    def handle_user_on_start(self, user: User, new_user: bool) -> None:
        user.send_command(
            OutboundCommands.load_user_details(
                user.user_id, user.user_details, user.user_status
            )
        )
        users_table.update_user_status(user.user_id, 'Online')
        self.file_buffers[user.user_id] = {}

        # Check if user is new
        if not new_user:
            self.load_pending_questions(user)
            self.load_user_chats(user)
            self.load_user_messages(user)
        else:
            # Give the user some questions if there is any
            questions.generate_questions(user.user_id)

        self.load_incoming_questions(user)
        self.suggest_question_recipients(user)


    def handle_login_request(self, user: User, email: str, password: str) -> None:
        # sanity checks for login
        if email == EMPTY or password == EMPTY:
            user.send_command(OutboundCommands.login_response(
                accepted=False, reason='Entry feilds cannot be empty')
            )
            return
        elif SPACE in email or SPACE in password:
            user.send_command(OutboundCommands.login_response(
                accepted=False, reason='Entry feilds cannot have spaces')
            )
            return
        elif not users_table.check_email_exists(email):
            user.send_command(OutboundCommands.login_response(
                accepted=False, reason='That email does not exist')
            )
            return
        elif not users_table.login_user(email, password):
            user.send_command(OutboundCommands.login_response(
                accepted=False, reason="That password does not match")
            )
            return
        else:
            # User has logged on
            user_id_result = users_table.get_user_id(email)
            user_profile = users_table.get_user(user_id_result[0])
            if not user_profile: return

            user.activate_user(user_id_result[0], user_profile[0])
            user.send_command(OutboundCommands.login_response())
            self.handle_user_on_start(user=user, new_user=False)
            self.__debug(user.address, 'User has logged in')


    def handle_verify_request(self, user: User, code: str) -> None:
        if not code.isdigit():
            user.send_command(OutboundCommands.verify_response(
                accepted=False, reason='Codes must be a four digit value')
            )
            return
        elif SPACE in code or code == EMPTY:
            user.send_command(OutboundCommands.verify_response(
                accepted=False, reason='Codes cannot be empty or contain spaces')
            )
            return
        elif not self.email_manager.check_verification_code(user.address, code):
            user.send_command(OutboundCommands.verify_response(
                accepted=False, reason='That code is invalid')
            )
            return
        else:
            # User has verified successfully
            if not user.cached_user_details: return
            users_table.register_user(user.cached_user_details)
            user_id_result = users_table.get_user_id(user.cached_user_details['email'])
            user.activate_user(user_id_result[0], user.cached_user_details)

            # send commands back to the client
            user.send_command(OutboundCommands.verify_response())
            self.handle_user_on_start(user=user, new_user=True)
            self.__debug(user.address, 'User has now been verified')


    def handle_register_request(self, user: User, user_details: UserDetails) -> None:
        # First check if there is any whitespace in the entrys apart from the#
        user_options_list = [
            user_details['option_one'], 
            user_details['option_two'],
            user_details['option_three'], 
            user_details['option_four']
        ]
        whitespace = utils.check_for_whitespace(items=user_details)
        empty = utils.check_for_empty(items=user_details)

        if whitespace or empty: user.send_command(
            OutboundCommands.register_response(
                accepted=False, reason='No whitespace or empty fields allowed')
            ); return

        if len(user_details['first_name']) > 25:
            user.send_command(OutboundCommands.register_response(
                accepted=False, reason='That first name is too large (max 25 characters)')
            )
            return 
        elif len(user_details['last_name']) > 25:
            user.send_command(OutboundCommands.register_response(
                accepted=False, reason='That last name is too large (max 25 characters)')
            )
            return 
        elif not user_details["tutor_group"] in self.settings['tutor_groups']:
            user.send_command(OutboundCommands.register_response(
                accepted=False, reason='That tutor group is invalid')
            )
            return 
        elif not self.email_manager.validate_email(user_details["email"]):
            user.send_command(OutboundCommands.register_response(
                accepted=False, reason='That email is invalid')
            )
            return 
        elif users_table.check_email_exists(user_details["email"]):
            user.send_command(OutboundCommands.register_response(
                accepted=False, reason='That email is already in use')
            )
            return 
        elif len(user_details['password']) < 8:
            user.send_command(OutboundCommands.register_response(
                accepted=False, reason='That password is too short (min 8 characters)')
            )
            return
        elif [x for x in user_options_list if x not in self.settings['options']]:
            user.send_command(OutboundCommands.register_response(
                accepted=False, reason='An option provided is invalid')
            )
            return 
        elif len([x for x in user_options_list if x == 'None']) > 3:
            user.send_command(OutboundCommands.register_response(
                accepted=False, reason='You must have at least one option')
            )
            return     
        elif utils.check_for_duplicates(user_options_list, exception='None'):
            user.send_command(OutboundCommands.register_response(
                accepted=False, reason='You cannot study the same option multiple times')
            )
            return 
    
        # passed registration checks
        user.cache_user_details(user_details)
        code = self.email_manager.init_verification_code(user.address)
        self.email_manager.send_verification_email(user_details["email"], str(code))
        user.send_command((OutboundCommands.register_response()))
        self.__debug(user.address, f'Verification code sent ({code})')


    def __debug(self, user_address: tuple, message: str) -> None:
        logging.debug(f"[server] handling user [{user_address}]: {message}")
