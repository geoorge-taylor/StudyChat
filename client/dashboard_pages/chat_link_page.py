from typing import Any, Union

import customtkinter


class ChatLink(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkScrollableFrame, first_name: str, second_name: str) -> None:
        super().__init__(master, height=85, fg_color='#2B2D31', border_width=0)
        self.first_name, self.last_name = first_name, second_name
        self.showing_rating_input = False
        self.error_created = False
        self.create_widgets()
        self.create_layout()


    def create_widgets(self) -> None:
        self.top_row = customtkinter.CTkFrame(self, fg_color='transparent', border_width=0, height=30)
        self.bottom_row = customtkinter.CTkFrame(self, fg_color='transparent', border_width=0, height=30)
        self.profile_picture = customtkinter.CTkLabel(self.top_row, fg_color='#674343', width=35, height=35, corner_radius=100, text='')
        self.accent = customtkinter.CTkFrame(self, fg_color='#248046', width=5, corner_radius=5)
        self.name_label = customtkinter.CTkLabel(self.top_row, font=('Segoe UI', 16, 'normal'), text=f'{self.first_name} {self.last_name}', anchor='w', text_color='#FFFFFF')
        self.view_chat_button = customtkinter.CTkButton(self.top_row, width=125, text='View chat', fg_color='#248046', border_width=0, hover_color='#1B5C33')
        self.end_chat_button = customtkinter.CTkButton(self.top_row, width=85, text='Stop answering', fg_color='#3E4046', border_width=0, hover_color='#2F3236')
        self.view_profile_button = customtkinter.CTkButton(self.top_row, width=85, text='View users profile', fg_color='#3E4046', border_width=0, hover_color='#2F3236')
        self.rating_entry = customtkinter.CTkEntry(self.bottom_row, width=175, border_width=0, fg_color='#3E4046', height=45, font=('Segoe UI', 13, 'normal'), placeholder_text_color='#A5A5A5', placeholder_text='Enter a rating out of 5')
        self.rate_user_button = customtkinter.CTkButton(self.bottom_row, width=75, text='Complete user rating', fg_color='#3E4046', border_width=0, hover_color='#2F3236')
        self.error_label = customtkinter.CTkLabel(self.bottom_row, width=550, font=('Segoe UI', 13, 'normal'), anchor='nw', text_color='#F26C6C')


    def create_layout(self) -> None:
        self.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, anchor=customtkinter.W, pady=(0, 7), padx=(0, 10))
        self.pack_propagate(False)
        self.accent.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False, padx=(0, 2))
        self.top_row.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, padx=(20, 20))
        self.profile_picture.pack(side=customtkinter.LEFT, fill=customtkinter.NONE, expand=False, padx=(0, 12))
        self.name_label.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False, padx=(0, 7))
        self.view_chat_button.pack(side=customtkinter.RIGHT, fill=customtkinter.Y, expand=False, padx=(8, 0), pady=25)
        self.end_chat_button.pack(side=customtkinter.RIGHT, fill=customtkinter.Y, expand=False, padx=(8, 0), pady=25)
        self.view_profile_button.pack(side=customtkinter.RIGHT, fill=customtkinter.Y, expand=False, pady=25)
        self.rating_entry.pack(side=customtkinter.LEFT, fill=customtkinter.NONE, expand=False, padx=(0, 12))
        self.rate_user_button.pack(side=customtkinter.LEFT, fill=customtkinter.NONE, expand=False)

    
    def toggle_rating_input(self) -> None:
        if not self.showing_rating_input: 
            self.bottom_row.pack(
                side=customtkinter.TOP, fill=customtkinter.X, 
                expand=False, padx=(20, 20), pady=(0, 15)
            )
            self.configure(height=125)
            self.end_chat_button.configure(text='Hide feedback rating section')
            self.showing_rating_input = True
        else: 
            self.bottom_row.pack_forget()
            self.end_chat_button.configure(text='View feedback rating section')
            self.configure(height=85)
            self.showing_rating_input = False


    def get_question_feedback(self) -> str:
        return self.rating_entry.get()
    

    def display_rating_error(self, error_message: str) -> None:
        if self.error_created: self.error_label.configure(text=error_message); return
        self.error_label = customtkinter.CTkLabel(self.bottom_row, width=550, font=('Segoe UI', 13, 'normal'), text_color='#F26C6C')
        self.error_label.pack(side=customtkinter.LEFT, fill=customtkinter.X, pady=(0, 0), padx=(20, 0))
        self.error_label.configure(text=error_message)
        self.error_created = True



class ChatLinkPage(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, hide: bool = True) -> None:
        super().__init__(master, fg_color='transparent', corner_radius=0)
        self.displaying = True
        self.empty = True
        self.create_widgets()
        self.create_layout(hide)
 

    def create_widgets(self) -> None:
        self.page_title = customtkinter.CTkLabel(self, height=30, fg_color='transparent', text_color='#FFFFFF', font=('Segoe UI', 20, 'bold'), text='View Chats', anchor='w')
        self.title_divider = customtkinter.CTkFrame(self, fg_color='#1F2123', height=2)
        self.chat_links_scroll_frame = customtkinter.CTkScrollableFrame(self, fg_color='transparent', border_width=0, orientation='vertical', scrollbar_button_color='#26272B')
        self.info_text = customtkinter.CTkLabel(self.chat_links_scroll_frame, fg_color='transparent', text_color='#B3B3B3', font=('Segoe UI', 15, 'normal'), text='You currently have no acitve chats with anyone. To start a chat, you must accept a question asked by any user in the pending questions page', anchor='nw')


    def create_layout(self, hide: bool) -> None:
        self.pack(expand=True, fill=customtkinter.BOTH)
        self.page_title.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=15, padx=20)
        self.title_divider.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=0, padx=0)
        self.chat_links_scroll_frame.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True, pady=14, padx=14)
        self.info_text.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=0)


    def create_chat_link(self, first_name: str, last_name: str) -> ChatLink:
        if self.empty: self.info_text.pack_forget(); self.empty = False
        return ChatLink(self.chat_links_scroll_frame, first_name, last_name)

    
    def toggle_page(self, hide: bool) -> None:
        if not hide: self.pack(expand=True,fill=customtkinter.BOTH)
        else: self.pack_forget()
        self.displaying = not hide