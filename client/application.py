import base64
import os
from tkinter import filedialog
from typing import Any, Union

import customtkinter
from networking import client_socket
from scenes.access import Access
from scenes.dashboard import Dashboard
from scenes.profile_viewer import ProfileViewer
from static.commands import InboundCommands, OutboundCommands
from static.shared_types import (
    MessageDetails,
    QuestionDetails,
    QuestionStatistics,
    SocketCommand,
)

MAX_FILE_SIZE = 100_000 # Bytes
BUFFER_CHUNK_SIZE = 200


class Application(customtkinter.CTk) :
    def __init__(self, socket_settings: dict[str, Any], app_settings: dict[str, Any]) -> None:
        super().__init__()
        self.running = True
        self.incoming_questions = dict()
        self.pending_questions = dict()
        self.chat_links = dict()
        self.chat_feeds = dict()
        self.file_buffers = dict()
        self.manual_user_widgets = dict()
        self.selected_manual_ids = list()

        # Create the server socket
        self.client_socket = client_socket.ClientSocket(
            port=socket_settings['port'], format=socket_settings['format'], backlog=socket_settings['backlog'], 
            header_size=socket_settings['header_size'], client_private_key_path=socket_settings['client_private_key'],
            server_public_key_path=socket_settings['server_public_key'], recv_callback=self.recv_command, 
            connect_to_server=socket_settings['connect_to_server']
        )

        self.title(app_settings['window_title'])
        self.geometry(f"{app_settings['window_width']}x{app_settings['window_height']}")
        self.minsize(width=app_settings['window_min_width'], height=app_settings['window_min_height'])
        self.resizable(app_settings['window_resizable'], app_settings['window_resizable'])

        self.profile_viewer = ProfileViewer(master=self)
        self.container = customtkinter.CTkFrame(self, fg_color=app_settings['light_grey'])  
        self.container.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True)

        # For the sub root ui elements
        self.dashboard = Dashboard(master=self.container, options=app_settings['options'], hide=True)
        self.access = Access(master=self.container, options=app_settings['options'], hide=False)

        self.frames = {"dashboard": self.dashboard, "access": self.access}
        self.protocol('WM_DELETE_WINDOW', func=self.exit)
        if app_settings['testing_mode']: self.login_testing_account()

        self.command_map = {
            InboundCommands.RegisterResponse.value: self.handle_register_response,
            InboundCommands.VerifyResponse.value: self.handle_verify_response,
            InboundCommands.LoadUserDetails.value: self.dashboard.load_user_details,
            InboundCommands.LoginResponse.value: self.handle_login_response,
            InboundCommands.AskQuestionResponse.value: self.handle_ask_question_response,
            InboundCommands.AddPendingQuestion.value: self.handle_add_pending_question,
            InboundCommands.AddIncomingQuestion.value: self.handle_add_incoming_question,
            InboundCommands.CreateProfileViewer.value: self.profile_viewer.show_profile,
            InboundCommands.CreateNewChat.value: self.handle_create_chat,
            InboundCommands.CreateChatReply.value: self.handle_create_chat_reply,
            InboundCommands.LoadFile.value: self.receive_file,
            InboundCommands.CreateManualUser.value: self.handle_add_manual_recipients,
            InboundCommands.UpdateQuestionStatistics.value: self.update_question_statistics,
            InboundCommands.DeleteIncomingQuestion.value: self.delete_incoming_question,
            InboundCommands.DeleteQuestionChat.value: self.delete_question_chat,
            InboundCommands.DeletePendingQuestion.value: self.delete_pending_question,
            InboundCommands.DisplayRatingError.value: self.display_rating_error
        }

        self.bind_buttons()
        self.mainloop()


    def login_testing_account(self) -> None:
        command = OutboundCommands.login(email='testing', password='1234')
        self.client_socket.send_command(command)


    def login_user(self) -> None:
        self.access.login_page.toggle_freeze_page(freeze=True)
        email, password = self.access.get_login_details()
        command = OutboundCommands.login(email, password)
        self.client_socket.send_command(command)


    def register_user(self) -> None:
        self.access.register_page.toggle_freeze_page(freeze=True)
        register_details = self.access.get_register_details()
        command = OutboundCommands.register(user_details=register_details)
        self.client_socket.send_command(command)
        

    def verify_user(self) -> None:
        self.access.verification_page.toggle_freeze_page(freeze=True)
        code_entered = self.access.verification_page.get_verification_code()
        command = OutboundCommands.verify(code=code_entered)
        self.client_socket.send_command(command)


    def handle_verify_response(self, accepted: bool, reason: str) -> None:
        if not accepted: self.access.verification_page.display_verification_error(reason)
        else: self.switch_frame('dashboard')
        self.access.verification_page.toggle_freeze_page(freeze=False)


    def handle_register_response(self, accepted: bool, reason: str) -> None:
        if not accepted: self.access.register_page.display_register_error(reason)
        else: self.access.switch_page('verification')
        self.access.register_page.toggle_freeze_page(freeze=False)

    
    def handle_login_response(self, accepted: bool, reason: str) -> None:
        if not accepted: self.access.login_page.display_login_error(reason)
        else: self.switch_frame('dashboard')
        self.access.login_page.toggle_freeze_page(freeze=False)


    def handle_ask_question_response(self, accepted: bool, reason: str) -> None:
        if not accepted: self.dashboard.ask_question_page.display_error(reason)
        else: self.dashboard.switch_page('pending-questions-page'); self.dashboard.clear_question_details()
        self.dashboard.ask_question_page.toggle_freeze_page(freeze=False)

    
    def request_question_deletion(self, question_id: int) -> None:
        command = OutboundCommands.delete_pending_question_request(question_id)
        self.client_socket.send_command(command)

    
    def delete_pending_question(self, question_id: int) -> None:
        if not self.pending_questions.get(question_id): return
        pending_question = self.pending_questions[question_id]
        pending_question.pack_forget()
        del self.pending_questions[question_id]

    
    def handle_add_pending_question(self, question_id: int, question_details: QuestionDetails, question_statistics: QuestionStatistics) -> None:
        pending_question = self.dashboard.pending_questions_page.create_pending_question(question_details, question_statistics)
        pending_question.toggle_description_button.configure(command=pending_question.toggle_description)
        pending_question.delete_question_button.configure(command=lambda: self.request_question_deletion(question_id))
        pending_question.toggle_statistics_button.configure(command=pending_question.toggle_statistics)
        self.pending_questions[question_id] = pending_question


    def handle_add_incoming_question(self, question_id: int, publisher_id: int, first_name: str, last_name: str, question_details: QuestionDetails) -> None:
        incoming_question = self.dashboard.incoming_questions_page.create_incoming_question(publisher_id, first_name, last_name, question_details)
        self.incoming_questions[question_id] = incoming_question
        view_profile_command = OutboundCommands.view_user_profile(publisher_id)
        delete_question_command = OutboundCommands.delete_incoming_question_request(question_id)
        create_chat_command = OutboundCommands.create_new_chat_request(question_id, publisher_id)
        incoming_question.view_profile_button.configure(command=lambda: self.client_socket.send_command(view_profile_command))
        incoming_question.delete_button.configure(command=lambda: self.client_socket.send_command(delete_question_command))
        incoming_question.awnser_question_button.configure(command=lambda: self.client_socket.send_command(create_chat_command))
        incoming_question.toggle_description_button.configure(command=incoming_question.toggle_description)

    
    def display_rating_error(self, chat_id: int, reason: str) -> None:
        if not self.chat_links.get(chat_id): return 
        chat_link = self.chat_links[chat_id]
        chat_link.display_rating_error(reason)

    
    def delete_incoming_question(self, question_id: int) -> None:
        if not self.incoming_questions.get(question_id): return 
        incoming_question = self.incoming_questions[question_id]
        incoming_question.pack_forget()
        del self.incoming_questions[question_id]


    def handle_add_manual_recipients(self, user_id: int, first_name: str, last_name: str, status: str) -> None:
        self.dashboard.ask_question_page.toggle_empty_label(True)
        user_widget = self.dashboard.ask_question_page.add_user_to_results(first_name, last_name, status)
        self.manual_user_widgets[user_id] = {'widget': user_widget, 'selected': False}
        user_widget.add_button.configure(command=lambda: self.toggle_manual_user_selection(user_id))


    def toggle_manual_user_selection(self, user_id: int) -> None:
        widget = self.manual_user_widgets[user_id]
        if widget['selected']:
            widget['widget'].toggle_user_widget(False)
            widget['selected'] = False
            self.selected_manual_ids.remove(user_id)
        else:
            widget['widget'].toggle_user_widget(True)
            widget['selected'] = True
            self.selected_manual_ids.append(user_id)

    
    def search_for_user(self) -> None:
        input = self.dashboard.ask_question_page.get_user_search_entry()
        self.dashboard.ask_question_page.clear_user_search_entry()
        for widget in self.manual_user_widgets.values(): 
            widget['widget'].destroy()

        self.manual_user_widgets.clear()
        self.dashboard.ask_question_page.toggle_empty_label(False)
        command = OutboundCommands.search_for_user(input)
        self.client_socket.send_command(command)


    def handle_create_chat_reply(self, chat_id: int, message_details: MessageDetails) -> None:
        if not self.chat_feeds.get(chat_id): return 
        self.chat_feeds[chat_id].create_message(message_details)


    def send_message(self, chat_id: int) -> None:
        if not self.chat_feeds.get(chat_id): return
        message_body = self.chat_feeds[chat_id].get_message()
        command = OutboundCommands.send_message_request(chat_id, message_body)
        self.client_socket.send_command(command)

    
    def receive_file(self, chat_id: int, file_name: str, contents: str, file_size: int, end: bool) -> None:
        if not self.chat_feeds.get(chat_id): return
        if end: 
            with open(file_name, 'wb') as file:
                file.write(self.file_buffers[file_name])
            file_widget = self.chat_feeds[chat_id].create_file(file_name, file_size)
            file_widget.open_button.configure(command=lambda: os.system(f'start {file_name}'))
            del self.file_buffers[file_name]
        else:
            base64_decoded = base64.b64decode(contents)
            if not self.file_buffers.get(file_name):
                self.file_buffers[file_name] = b""
            self.file_buffers[file_name] += base64_decoded

    
    def send_file(self, chat_id: int) -> None:
        file_path = filedialog.askopenfilename(initialdir="/Documents", title="Browse")
        file_size, file_name = os.path.getsize(file_path), os.path.basename(file_path)
        if file_size > MAX_FILE_SIZE or ' ' in file_name: return

        with open(file_path, 'rb') as file:
              while True:
                data = file.read(BUFFER_CHUNK_SIZE)
                base64_encoded = base64.b64encode(data)
                base64_string = base64_encoded.decode('utf-8')

                if not data:
                    self.client_socket.send_command(
                        OutboundCommands.send_file_request(
                            chat_id=chat_id, contents='', end=True,
                            file_name=file_name, file_size=file_size
                        )
                    )
                    break       
                self.client_socket.send_command(
                    OutboundCommands.send_file_request(
                        chat_id=chat_id, contents=base64_string,
                        file_name=file_name, file_size=file_size,
                        end=False
                    )
                )
    
    
    def end_chat_as_recipient(self, chat_id: int) -> None:
        command = OutboundCommands.end_chat_request_as_recipient(chat_id)
        self.client_socket.send_command(command)


    def end_chat_as_publisher(self, chat_id: int, rating: str) -> None:
        command = OutboundCommands.end_chat_request_as_publisher(chat_id, rating)
        self.client_socket.send_command(command)

    
    def handle_create_chat(self, chat_id: int, user_id: int, first_name: str, last_name: str, question_details: QuestionDetails, question_publisher: bool) -> None:
        view_profile_command = OutboundCommands.view_user_profile(user_id)
        chat_feed = self.dashboard.chat_page.create_chat_feed(first_name, last_name, question_details)
        chat_link = self.dashboard.chat_page.chat_link_page.create_chat_link(first_name, last_name)
        self.chat_feeds[chat_id], self.chat_links[chat_id] = chat_feed, chat_link

        chat_feed.back_button.configure(command=lambda: self.close_question_chat(chat_id))
        chat_link.view_chat_button.configure(command=lambda: self.open_question_chat(chat_id))
        chat_link.view_profile_button.configure(command=lambda: self.client_socket.send_command(view_profile_command))
        chat_feed.send_message_button.configure(command=lambda: self.send_message(chat_id))
        chat_feed.send_file_button.configure(command=lambda: self.send_file(chat_id))
        chat_feed.message_entry.bind('<Return>', command=lambda _: self.send_message(chat_id))

        if not question_publisher: 
            chat_link.end_chat_button.configure(
                command=lambda: self.end_chat_as_recipient(chat_id)
            ); return
        
        else:
            chat_link.accent.configure(fg_color='#245480')
            chat_link.end_chat_button.configure(text='End chat and review user')
            chat_link.end_chat_button.configure(command=chat_link.toggle_rating_input)
            chat_link.rate_user_button.configure(
                command=lambda: self.end_chat_as_publisher(
                    chat_id, chat_link.get_question_feedback()
                )
            )

    
    def delete_question_chat(self, chat_id: int) -> None:
        if not self.chat_links.get(chat_id) or not self.chat_feeds.get(chat_id): 
            return 
        self.chat_links[chat_id].pack_forget()
        self.chat_feeds[chat_id].pack_forget()
        del self.chat_links[chat_id]
        del self.chat_feeds[chat_id]


    def ask_question(self) -> None:
        self.dashboard.ask_question_page.toggle_freeze_page(freeze=True)
        question_details = self.dashboard.get_question_details()
        manual_searching = self.dashboard.ask_question_page.manual_searching
        command: Union[SocketCommand, None] = None

        if manual_searching: command = OutboundCommands.ask_question(question_details, self.selected_manual_ids)
        else: command =  OutboundCommands.ask_question(question_details)
        self.client_socket.send_command(command)

    
    def update_question_statistics(self, question_id: int, question_statistics: QuestionStatistics) -> None:
        pending_question = self.pending_questions.get(question_id)
        if not pending_question: return
        pending_question.update_statistics(question_statistics)

    
    def sign_out_user(self) -> None:
        command = OutboundCommands.sign_out()
        self.client_socket.send_command(command)
        self.switch_frame('access')


    # Other application methods
    def recv_command(self, command: SocketCommand) -> None:
        command_name, arguments = command.get('command_name'), command.get('arguments')
        if not InboundCommands.has_command(command_name): return
        try: self.command_map[command_name](**arguments)
        except (KeyError, TypeError) as err: print(f'Could not map command: {err}')

    
    def bind_buttons(self) -> None:
        self.access.register_page.register_button.configure(command=lambda: self.register_user())
        self.access.verification_page.verify_button.configure(command=lambda: self.verify_user())
        self.access.login_page.login_button.configure(command=lambda: self.login_user())
        self.dashboard.ask_question_page.ask_question_button.configure(command=lambda: self.ask_question())
        self.dashboard.ask_question_page.manual_user_search.bind('<Return>', command=lambda _: self.search_for_user())


    def open_question_chat(self, question_id: int) -> None:
        if not question_id in self.chat_feeds.keys(): return
        self.dashboard.chat_page.chat_link_page.toggle_page(hide=True)
        self.chat_feeds[question_id].toggle_page(False)

    
    def close_question_chat(self, question_id: int) -> None:
        if not question_id in self.chat_feeds.keys(): return
        self.chat_feeds[question_id].toggle_page(True)
        self.dashboard.chat_page.chat_link_page.toggle_page(hide=False)

    
    def switch_frame(self, _to: str) -> None:
        if not self.frames[_to].displaying: 
            for frame in self.frames.values():
                if frame.displaying: frame.toggle_frame(True)
            self.frames[_to].toggle_frame(False)


    def exit(self) -> None:
        self.running = False
        if self.client_socket.connected:
            self.client_socket.close()
        self.destroy()

 