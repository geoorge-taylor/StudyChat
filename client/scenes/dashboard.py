import customtkinter
from dashboard_pages import (
    ask_question_page,
    chat_page,
    incoming_questions_page,
    pending_questions_page,
    profile_page,
)
from static.shared_types import QuestionDetails, UserDetails


class Dashboard(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, options: list[str], hide: bool = False) -> None:
        super().__init__(master, fg_color="transparent", corner_radius=0)
        self.displaying = True
        self.create_widgets()
        self.create_layout(hide)
        self.bind_sidebar_buttons()

        self.chat_page = chat_page.ChatPage(self.page_content, hide=True)
        self.ask_question_page = ask_question_page.AskQuestionPage(self.page_content, options=options, hide=True)
        self.profile_page = profile_page.ProfilePage(self.page_content, hide=True)
        self.pending_questions_page = pending_questions_page.PendingQuestionsPage(self.page_content, hide=True)
        self.incoming_questions_page = incoming_questions_page.IncomingQuestionsPage(self.page_content, hide=False)

        self.pages = {
            "chat-page": self.chat_page,
            "ask-question-page": self.ask_question_page,
            "profile-page": self.profile_page,
            "pending-questions-page": self.pending_questions_page,
            "incoming-questions-page": self.incoming_questions_page,
        }


    def create_widgets(self) -> None:
        # Create all the  widgets used for this frame. Main UI Element
        self.side_nav_bar = customtkinter.CTkFrame(self, fg_color="#2B2D31", corner_radius=0, width=240)
        self.page_content = customtkinter.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.profile_widget = customtkinter.CTkFrame(self.side_nav_bar, fg_color="#232428", corner_radius=0, width=240, height=75)
        self.profile_picture = customtkinter.CTkLabel(self.profile_widget, fg_color="#674343", width=30, height=30, corner_radius=100, text="")
        self.profile_name = customtkinter.CTkLabel(self.profile_widget, font=("Segoe UI", 15, "normal"), text="~~~", height=85, anchor="w", text_color="#FFFFFF", width=50)
        self.status = customtkinter.CTkLabel(self.profile_widget, font=("Segoe UI", 15, "normal"), text="~~~", anchor="w", text_color="#248046")
        self.search_buttons_entry = customtkinter.CTkEntry(self.side_nav_bar, fg_color="#1E1F22", height=30, placeholder_text="Search here...", placeholder_text_color="#7E848C", border_width=0)
        self.side_navbar_divider = customtkinter.CTkFrame(self.side_nav_bar, fg_color="#1F2123", height=2)

        # Page buttons for side bar
        self.chats_button = customtkinter.CTkButton(self.side_nav_bar, height=35, fg_color="#313338", text_color="#949BA4", font=("Segoe UI", 15, "normal"), hover_color="#404249", text="View chats", anchor="w")
        self.incoming_questions_button = customtkinter.CTkButton( self.side_nav_bar, height=35, fg_color="#313338", text_color="#949BA4", font=("Segoe UI", 15, "normal"), hover_color="#404249", text="View Incoming Questions", anchor="w",)
        self.ask_question_button = customtkinter.CTkButton( self.side_nav_bar, height=35, fg_color="#313338", text_color="#949BA4", font=("Segoe UI", 15, "normal"), hover_color="#404249", text="Ask a question", anchor="w")
        self.pending_questions_button = customtkinter.CTkButton( self.side_nav_bar, height=35, fg_color="#313338", text_color="#949BA4", font=("Segoe UI", 15, "normal"), hover_color="#404249", text="View pending questions", anchor="w")
        self.profile_button = customtkinter.CTkButton( self.side_nav_bar, height=35, fg_color="#313338", text_color="#949BA4", font=("Segoe UI", 15, "normal"), hover_color="#404249", text="View profile", anchor="w")


    def create_layout(self, hide: bool) -> None:
        self.pack(expand=True, fill=customtkinter.BOTH)
        # Main UI holders and widgets
        self.side_nav_bar.pack(side=customtkinter.LEFT, fill=customtkinter.Y)
        self.page_content.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True)
        self.profile_widget.pack(side=customtkinter.BOTTOM, fill=customtkinter.X, expand=False)
        self.profile_picture.pack(side=customtkinter.LEFT, fill=None, expand=False, padx=(20, 10))
        self.profile_name.pack(side=customtkinter.LEFT, fill=customtkinter.NONE, expand=False, padx=(0, 8))
        self.status.pack(side=customtkinter.LEFT, fill=customtkinter.NONE, expand=False)
        self.search_buttons_entry.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, padx=16, pady=15)
        self.side_navbar_divider.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, padx=0, pady=0)
        self.chats_button.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, padx=16, pady=(20, 0))
        self.incoming_questions_button.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, padx=16, pady=(12, 0))
        self.ask_question_button.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, padx=16, pady=(12, 0))
        self.pending_questions_button.pack( side=customtkinter.TOP, fill=customtkinter.X, expand=False, padx=16, pady=(12, 0))
        self.profile_button.pack( side=customtkinter.TOP, fill=customtkinter.X, expand=False, padx=16, pady=(12, 0))
        self.side_nav_bar.pack_propagate(False)
        self.profile_widget.pack_propagate(False)
        if hide: self.toggle_frame(True)


    def load_user_details(self, user_id: int, user_details: UserDetails, user_status: str) -> None:
        self.profile_name.configure(text=f'{user_details["first_name"]} {user_details["last_name"]}')
        self.status.configure(text=user_status)
        self.profile_page.user_id_widget.option_value.configure(text=user_id)
        self.profile_page.points_widget.option_value.configure(text=user_details['points'])
        self.profile_page.first_name_widget.option_value.configure(text=user_details["first_name"])
        self.profile_page.last_name_widget.option_value.configure(text=user_details["last_name"])
        self.profile_page.linked_email_widget.option_value.configure(text=user_details["email"])
        self.profile_page.option_one_widget.option_value.configure(text=user_details['option_one'])
        self.profile_page.option_two_widget.option_value.configure(text=user_details['option_two'])
        self.profile_page.option_three_widget.option_value.configure(text=user_details['option_three'])
        self.profile_page.option_four_widget.option_value.configure(text=user_details['option_four'])
        self.profile_page.tutor_group_widget.option_value.configure(text=user_details["tutor_group"])



    def get_question_details(self) -> QuestionDetails:
        return {
            'title': self.ask_question_page.title_entry.get(),
            'subject': self.ask_question_page.subject_entry.get(),
            'description': self.ask_question_page.description_entry.get("0.0", "end"),
            'expires_date': self.ask_question_page.expires_entry.get(),
            'second_year_content': True if self.ask_question_page.second_year_content_option.get() == 'Yes' else False
        }
    
    
    def clear_question_details(self) -> None:
        self.ask_question_page.title_entry.delete(0, customtkinter.END)
        self.ask_question_page.expires_entry.delete(0, customtkinter.END)
        self.ask_question_page.description_entry.delete(0.0, customtkinter.END)
        self.ask_question_page.subject_entry.set('None')


    def bind_sidebar_buttons(self) -> None:
        self.chats_button.bind("<Button-1>", lambda _: self.switch_page(_to="chat-page"))
        self.ask_question_button.bind("<Button-1>", lambda _: self.switch_page(_to="ask-question-page"))
        self.profile_button.bind("<Button-1>", lambda _: self.switch_page(_to="profile-page"))
        self.pending_questions_button.bind("<Button-1>", lambda _: self.switch_page(_to="pending-questions-page"))
        self.incoming_questions_button.bind("<Button-1>", lambda _: self.switch_page(_to="incoming-questions-page"))


    def switch_page(self, _to: str) -> None:
        if not self.pages[_to].displaying:
            for page in self.pages.values():
                if page.displaying:
                    page.toggle_page(True)
            self.pages[_to].toggle_page(False)


    def toggle_frame(self, hide: bool) -> None:
        if not hide: self.pack(expand=True, fill=customtkinter.BOTH)
        else: self.pack_forget()
        self.displaying = not hide
