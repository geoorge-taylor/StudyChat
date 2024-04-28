from typing import Any

import customtkinter
from PIL import Image, ImageTk
from static.shared_types import MessageDetails, QuestionDetails
from os import path


class Message(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkScrollableFrame, message: MessageDetails) -> None:
        super().__init__(master, height=50, fg_color='transparent', border_width=0)

        self.profile_picture = customtkinter.CTkLabel(self, fg_color='#674343', width=40, height=40, corner_radius=75, text='', anchor='center')
        self.content_holder = customtkinter.CTkFrame(self, fg_color='transparent', border_width=0)
        self.top_row = customtkinter.CTkFrame(self.content_holder, fg_color='transparent', border_width=0)
        self.name_label = customtkinter.CTkLabel(self.top_row, font=('Segoe UI', 16, 'bold'), text=f'{message["first_name"]} {message["last_name"]}', anchor='sw', text_color='#FFFFFF')
        self.date_sent_label = customtkinter.CTkLabel(self.top_row, font=('Segoe UI', 12, 'normal'), text=message["date_sent"], anchor='sw', text_color='#AEAEAE')
        self.message_label = customtkinter.CTkLabel(self.content_holder, font=('Segoe UI', 14, 'normal'), text=message["body"], anchor='nw', text_color='#FFFFFF')
        
        self.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, anchor=customtkinter.W, pady=(0, 8))
        self.profile_picture.pack(side=customtkinter.LEFT, fill=customtkinter.NONE, expand=False, padx=(0, 10), pady=(5, 0))
        self.content_holder.pack(side=customtkinter.LEFT, fill=customtkinter.X, expand=False)
        self.top_row.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True)
        self.name_label.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False)
        self.date_sent_label.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False, padx=(8, 0))
        self.message_label.pack(side=customtkinter.BOTTOM, fill=customtkinter.BOTH, expand=True, pady=(3, 0))


class File(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkScrollableFrame, file_name: str, size: str) -> None:
        super().__init__(master, height=75, width=350, fg_color='#2B2D31', border_width=0)
        self.content_holder = customtkinter.CTkFrame(self, fg_color='transparent', border_width=0)
        self.open_button = customtkinter.CTkButton(self.content_holder, font=('Segoe UI', 16, 'normal'), fg_color='transparent', anchor='sw', border_width=0, text=file_name, text_color='#2A6BE8')
        self.size_label = customtkinter.CTkLabel(self.content_holder, font=('Segoe UI', 14, 'normal'), text=f'File size: {size} Bytes', anchor='nw', text_color='#646464')
        self.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, anchor=customtkinter.W, pady=(0, 8))
        self.pack_propagate(False)
        self.content_holder.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True, padx=10)
        self.open_button.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True)
        self.size_label.pack(side=customtkinter.BOTTOM, fill=customtkinter.BOTH, expand=True, padx=5)




class QuestionReference(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, question_details: QuestionDetails) -> None:
        super().__init__(master, height=75, fg_color='#2B2D31', border_width=0, corner_radius=5)
        self.question_details = question_details
        self.title = customtkinter.CTkLabel(self, text='Question title:  '+ self.question_details['title'], text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), anchor='w')
        self.subject = customtkinter.CTkLabel(self, text='Question subject:  '+ self.question_details['subject'], text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), anchor='w')
        self.expires_date = customtkinter.CTkLabel(self, text='Question expires:  '+ self.question_details['expires_date'], text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), anchor='w')
        self.title.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False, pady=15, padx=20)
        self.subject.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False, pady=15, padx=(0, 20))
        self.expires_date.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False, pady=20)



class ChatFeed(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, first_name: str, last_name: str, question_details: QuestionDetails) -> None:
        super().__init__(master, fg_color='transparent', corner_radius=0)
        self.first_name, self.last_name = first_name, last_name
        self.send_icon_path = path.join(path.dirname(__file__), 'icons\\send.png')
        self.attatchment_icon = path.join(path.dirname(__file__), 'icons\\attatchment.png')
        self.send_icon = customtkinter.CTkImage(Image.open(self.send_icon_path), size=(25, 25))
        self.attatchment_icon = customtkinter.CTkImage(Image.open(self.attatchment_icon), size=(25, 25))
        self.question_details = question_details
        self.displaying = True
        self.create_widgets()
        self.create_layout()
        self.toggle_page(True)


    def create_widgets(self) -> None:
        self.top_navigation_bar = customtkinter.CTkFrame(self, height=30, fg_color='transparent', border_width=0)
        self.back_button = customtkinter.CTkButton(self.top_navigation_bar, height=30, width=30, fg_color='#2B2D31', text='<', font=('Segoe UI', 12, 'bold'), text_color='white')
        self.page_title = customtkinter.CTkLabel(self.top_navigation_bar, height=30, fg_color='transparent', text_color='#FFFFFF', font=('Segoe UI', 20, 'bold'), text=f'View Chats - {self.first_name} {self.last_name}', anchor='w')
        self.title_divider = customtkinter.CTkFrame(self, fg_color='#1F2123', height=2)
        self.question_reference = QuestionReference(self, self.question_details)
        self.message_scroll_frame = customtkinter.CTkScrollableFrame(self, fg_color='transparent', border_width=0, orientation='vertical', scrollbar_button_color='#26272B')
        self.bottom_bar = customtkinter.CTkFrame(self, fg_color='#383A40', border_width=0, corner_radius=5, height=45)
        self.message_entry = customtkinter.CTkEntry(self.bottom_bar, border_width=0, fg_color='transparent', height=45, font=('Segoe UI', 15, 'normal'), placeholder_text_color='#A5A5A5', placeholder_text='Click here to send a message')
        self.send_message_button = customtkinter.CTkButton(self.bottom_bar, fg_color='transparent', height=45, width=35, font=('Segoe UI', 15, 'bold'), image=self.send_icon, text='')
        self.send_file_button = customtkinter.CTkButton(self.bottom_bar, fg_color='transparent', height=45, width=35, font=('Segoe UI', 15, 'bold'), image=self.attatchment_icon, text='')


    def create_layout(self) -> None:
        self.pack(expand=True, fill=customtkinter.BOTH)
        self.top_navigation_bar.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=15, padx=20)
        self.back_button.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False, padx=(0, 10))
        self.page_title.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False)
        self.title_divider.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=0, padx=0)
        self.question_reference.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=20, padx=14)
        self.message_scroll_frame.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True, padx=20)
        self.bottom_bar.pack(side=customtkinter.BOTTOM, fill=customtkinter.X, expand=False, pady=(10, 30), padx=14)
        self.send_file_button.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False, padx=(10, 5))
        self.message_entry.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True)
        self.send_message_button.pack(side=customtkinter.RIGHT, fill=customtkinter.Y, expand=False, padx=(0, 10))

    
    def create_message(self, message_details: MessageDetails) -> None:
        Message(self.message_scroll_frame, message_details) 


    def create_file(self, file_name: str, file_size: str) -> File:
        file_widget = File(self.message_scroll_frame, file_name, file_size)
        return file_widget

    
    def get_message(self) -> str:
        message_body = self.message_entry.get()
        self.message_entry.delete(0, customtkinter.END)
        return message_body


    def toggle_page(self, hide: bool) -> None:
        if not hide: self.pack(expand=True,fill=customtkinter.BOTH)
        else: self.pack_forget()
        self.displaying = not hide