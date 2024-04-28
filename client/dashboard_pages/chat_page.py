from typing import Any

import customtkinter
from dashboard_pages import chat_feed, chat_link_page
from static.shared_types import QuestionDetails


class ChatPage(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, hide: bool = True):
        super().__init__(master, fg_color='transparent', corner_radius=0)
        self.chat_link_page = chat_link_page.ChatLinkPage(self, hide=False)
        self.displaying = True
        self.create_layout(hide)
       

    def create_layout(self, hide: bool) -> None:
        self.pack(expand=True, fill=customtkinter.BOTH)
        if hide: self.toggle_page(True)


    def create_chat_feed(self, first_name: str, last_name: str, question_details: QuestionDetails) -> chat_feed.ChatFeed:
        return chat_feed.ChatFeed(self, first_name, last_name, question_details)
    

    def toggle_page(self, hide: bool) -> None:
        if not hide: self.pack(expand=True,fill=customtkinter.BOTH)
        else: self.pack_forget()
        self.displaying = not hide