import customtkinter
from typing import Union, Tuple, Optional, Any


class VerificationPage(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, hide: bool = True):
        super().__init__(master, fg_color='transparent', corner_radius=0)
        self.displaying = True
        self.error_created = False
        self.create_widgets()
        self.create_layout(hide)
        

    def create_widgets(self) -> None:
        # Information text blocks
        self.info_text_one = customtkinter.CTkLabel(self, width=650, text='Please enter the code sent to the email provided', text_color='#B3B3B3', font=('Segoe UI', 14, 'normal'), anchor='w')
        self.title_label = customtkinter.CTkLabel(self, font=('Segoe UI', 27, 'bold'), text='Verification', anchor='w', text_color='#FFFFFF')
        self.code_entry = customtkinter.CTkEntry(self,height=42, fg_color='#2B2D31', placeholder_text='Enter code', placeholder_text_color='#787878', border_width=0, font=('Segoe UI', 13, 'normal'), text_color='#FFFFFF')
        self.verify_button = customtkinter.CTkButton(self, height=38, text='Verify', text_color='#FFFFFF', fg_color='#248046', border_width=0, hover_color='#1B5C33', font=('Segoe UI', 15, 'bold'))
        self.toggle_button = customtkinter.CTkButton(self, height=20, text='Go back', text_color='#FFFFFF', fg_color='transparent', border_width=0, hover_color='#2F3236', font=('Segoe UI', 14, 'normal'), anchor='e')


    def create_layout(self, hide: bool) -> None:
        self.place(anchor=customtkinter.CENTER, relx=.5, rely=.5)
        self.title_label.pack(side=customtkinter.TOP, fill=customtkinter.X)
        self.info_text_one.pack(side=customtkinter.TOP, fill=customtkinter.X)
        self.code_entry.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(8, 0))
        self.verify_button.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(8, 0))
        self.toggle_button.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(8, 0))
        if hide: self.toggle_page(True)


    def display_verification_error(self, error_message: str) -> None:
        if self.error_created: self.error_label.configure(text=error_message); return
        self.error_label = customtkinter.CTkLabel(self, width=550, font=('Segoe UI', 13, 'normal'), anchor='nw', text_color='#F26C6C')
        self.error_label.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(5, 0))
        self.error_label.configure(text=error_message)
        self.error_created = True

    
    def toggle_freeze_page(self, freeze: bool) -> None:
        if freeze: self.verify_button.configure(state='disabled', fg_color='#525252', text='Verifying...')
        else: self.verify_button.configure(state='normal', fg_color='#248046', text='Verify')


    def toggle_page(self, hide: bool) -> None:
        if not hide: self.place(anchor=customtkinter.CENTER, relx=.5, rely=.5)
        else: self.place_forget()
        self.displaying = not hide


    def get_verification_code(self) -> str:
        return self.code_entry.get()
    