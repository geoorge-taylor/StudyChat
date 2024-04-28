from typing import Any

import customtkinter
from static.shared_types import QuestionDetails, QuestionStatistics

STATISTICS_TEXT = "This question is currently in {} user's inboxes. {} users have responded to your question"


class PendingQuestionFrame(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkScrollableFrame, question_details: QuestionDetails, question_statistics: QuestionStatistics) -> None:
        super().__init__(master, height=120, fg_color='#2B2D31', border_width=0)
        self.recipient_ammount = question_statistics['recipient_ammount']
        self.recipient_awnsers = question_statistics['recipient_awnsers']
        self.question_details = question_details
        self.showing_description = False
        self.showing_statistics = False
        self.create_widgets()
        self.create_layout()


    def create_widgets(self) -> None:
        self.question_labels_holder = customtkinter.CTkFrame(self, fg_color='transparent', border_width=0, height=30)
        self.question_buttons_holder = customtkinter.CTkFrame(self, fg_color='transparent', border_width=0, height=30)
        self.question_title = customtkinter.CTkLabel(self.question_labels_holder, text='Question title: '+ self.question_details['title'], text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), anchor='w')
        self.question_subject = customtkinter.CTkLabel(self.question_labels_holder, text='Question subject: '+ self.question_details['subject'], text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), anchor='w')
        self.question_expires = customtkinter.CTkLabel(self.question_labels_holder, text='Question expires: '+ self.question_details['expires_date'], text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), anchor='w')
        self.toggle_statistics_button = customtkinter.CTkButton(self.question_buttons_holder, height=30, text='View statistics', fg_color='#248046', border_width=0, hover_color='#1B5C33')
        self.toggle_description_button = customtkinter.CTkButton(self.question_buttons_holder, height=30, text='View description', fg_color='#3E4046', border_width=0, hover_color='#2F3236')
        self.delete_question_button = customtkinter.CTkButton(self.question_buttons_holder, height=30, text='Delete question', fg_color='#3E4046', border_width=0, hover_color='#2F3236')
        self.question_description = customtkinter.CTkLabel(self, text_color='grey', font=('Segoe UI', 13, 'normal'), text=self.question_details['description'], fg_color='transparent', anchor='nw')
        self.statistics_label = customtkinter.CTkLabel(self, text_color='grey', font=('Segoe UI', 13, 'normal'), text=STATISTICS_TEXT.format(self.recipient_ammount, self.recipient_awnsers), fg_color='transparent', anchor='nw')


    def create_layout(self) -> None:
        self.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, anchor=customtkinter.W, pady=(0, 10), padx=(0, 10))
        self.pack_propagate(False)
        self.question_labels_holder.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True, padx=20, pady=(10, 6))
        self.question_buttons_holder.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True, padx=20, pady=(6, 10))
        self.question_title.pack(side=customtkinter.LEFT, anchor=customtkinter.S, padx=(0, 12))
        self.question_subject.pack(side=customtkinter.LEFT, anchor=customtkinter.S, padx=(0, 12))
        self.question_expires.pack(side=customtkinter.LEFT, anchor=customtkinter.S, padx=(0, 12))
        self.toggle_statistics_button.pack(side=customtkinter.LEFT, anchor=customtkinter.N, padx=(0, 10))
        self.toggle_description_button.pack(side=customtkinter.LEFT, anchor=customtkinter.N, padx=(0, 10))
        self.delete_question_button.pack(side=customtkinter.LEFT, anchor=customtkinter.N, padx=(0, 10))


    def update_statistics(self, question_statistics: QuestionStatistics) -> None:
        self.recipient_ammount = question_statistics['recipient_ammount']
        self.recipient_awnsers = question_statistics['recipient_awnsers']
        self.statistics_label.configure(text=STATISTICS_TEXT.format(
            self.recipient_ammount, self.recipient_awnsers)
        )

    
    def toggle_description(self) -> None:
        if not self.showing_description: 
            self.question_description.pack(
                side=customtkinter.TOP, 
                fill=customtkinter.BOTH, 
                expand=True, padx=20, 
                pady=(3, 0)
            )
            self.configure(height=175)
            self.toggle_description_button.configure(text='Hide description')
            self.showing_description = True
        else: 
            self.question_description.pack_forget()
            self.toggle_description_button.configure(text='View description')
            self.configure(height=120)
            self.showing_description = False


    def toggle_statistics(self) -> None:
        if not self.showing_statistics: 
            self.statistics_label.pack(
                side=customtkinter.TOP, 
                fill=customtkinter.BOTH, 
                expand=True, padx=20, 
                pady=(3, 0)
            )
            self.configure(height=175)
            self.toggle_statistics_button.configure(text='Hide statistics')
            self.showing_statistics = True
        else: 
            self.statistics_label.pack_forget()
            self.toggle_statistics_button.configure(text='View statistics')
            self.configure(height=120)
            self.showing_statistics = False




class PendingQuestionsPage(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, hide: bool = False) -> None:
        super().__init__(master, fg_color='transparent', corner_radius=0)
        self.displaying = True
        self.empty = True
        self.create_widgets()
        self.create_layout(hide)
 

    def create_widgets(self) -> None:
        self.page_title = customtkinter.CTkLabel(self, height=30, fg_color='transparent', text_color='#FFFFFF', font=('Segoe UI', 20, 'bold'), text='View pending questions', anchor='w')
        self.title_divider = customtkinter.CTkFrame(self, fg_color='#1F2123', height=2)
        self.pending_questions_holder = customtkinter.CTkScrollableFrame(self, fg_color='transparent', border_width=0, orientation='vertical', scrollbar_button_color='#26272B')
        self.info_text = customtkinter.CTkLabel(self.pending_questions_holder, fg_color='transparent', text_color='#B3B3B3', font=('Segoe UI', 15, 'normal'), text='It appears that no one has asked you any questions yet. When a user asks you a question, it will appear here', anchor='nw')


    def create_layout(self, hide: bool) -> None:
        self.pack(expand=True, fill=customtkinter.BOTH)
        self.page_title.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=15, padx=20)
        self.title_divider.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=0, padx=0)
        self.pending_questions_holder.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True, pady=14, padx=14)
        self.info_text.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False)
        if hide: self.toggle_page(True)


    def create_pending_question(self, question_details: QuestionDetails, question_statistcs: QuestionStatistics) -> PendingQuestionFrame:
        pending_question = PendingQuestionFrame(self.pending_questions_holder, question_details, question_statistcs)
        if self.empty: self.info_text.pack_forget(); self.empty = False
        return pending_question


    def toggle_page(self, hide: bool) -> None:
        if not hide: self.pack(expand=True,fill=customtkinter.BOTH)
        else: self.pack_forget()
        self.displaying = not hide