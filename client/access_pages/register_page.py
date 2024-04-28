from typing import Any, Optional, Tuple, Union

import customtkinter


class RegisterPage(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, options: list[str], hide: bool = True) -> None:
        super().__init__(master, width=650, fg_color='transparent', corner_radius=0)
        self.displaying = True
        self.options = options
        self.error_created = False
        self.create_widgets()
        self.create_layout(hide)
        

    def create_widgets(self) -> None:
        # Information text blocks
        self.info_text_one = customtkinter.CTkLabel(self, width=650, text='Welcome to study chat. Please create an account to start asking your questions', text_color='#B3B3B3', font=('Segoe UI', 14, 'normal'), anchor='w')
        self.info_text_two = customtkinter.CTkLabel(self, text='Select the subjects you are currently studying', text_color='#B3B3B3', font=('Segoe UI', 14, 'normal'), anchor='w')
        self.info_text_three = customtkinter.CTkLabel(self, text='One you have registered, a verification email will be sent to the email provided', text_color='#B3B3B3', font=('Segoe UI', 14, 'normal'), anchor='w')
        self.info_text_four = customtkinter.CTkLabel(self, text='This email should be registered to the @thomas-hardye.net domain', text_color='#B3B3B3', font=('Segoe UI', 14, 'normal'), anchor='w')
        self.title_label = customtkinter.CTkLabel(self, font=('Segoe UI', 27, 'bold'), text='Start asking with Study Chat', anchor='w', text_color='#FFFFFF')
        self.first_name_entry = customtkinter.CTkEntry(self, height=42, fg_color='#2B2D31', placeholder_text='First name', placeholder_text_color='#787878', border_width=0, font=('Segoe UI', 13, 'normal'), text_color='#FFFFFF')

        # Entrys for user inputs
        self.last_name_entry = customtkinter.CTkEntry(self, height=42, fg_color='#2B2D31', placeholder_text='Last name', placeholder_text_color='#787878', border_width=0, font=('Segoe UI', 13, 'normal'), text_color='#FFFFFF')
        self.email_address_entry = customtkinter.CTkEntry(self,height=42, fg_color='#2B2D31', placeholder_text='Email address', placeholder_text_color='#787878', border_width=0, font=('Segoe UI', 13, 'normal'), text_color='#FFFFFF')
        self.password_entry = customtkinter.CTkEntry(self, height=42, fg_color='#2B2D31', placeholder_text='Password', placeholder_text_color='#787878', border_width=0, font=('Segoe UI', 13, 'normal'), text_color='#FFFFFF', show='*')
        self.tutor_group_entry = customtkinter.CTkEntry(self, height=42, fg_color='#2B2D31', placeholder_text='Enter your current tutor group', placeholder_text_color='#787878', border_width=0, font=('Segoe UI', 13, 'normal'), text_color='#FFFFFF')        

        # Widgets for the option entrys
        self.option_row = customtkinter.CTkFrame(self, height=42, fg_color='transparent')
        self.option_one = customtkinter.CTkOptionMenu(self.option_row, fg_color='#2B2D31', dropdown_fg_color='#2B2D31', values=self.options, font=('Segoe UI', 13, 'normal'), button_color='#2B2D31', text_color='#787878', button_hover_color='#36383D')
        self.option_two = customtkinter.CTkOptionMenu(self.option_row, fg_color='#2B2D31', dropdown_fg_color='#2B2D31', values=self.options, font=('Segoe UI', 13, 'normal'), button_color='#2B2D31', text_color='#787878', button_hover_color='#36383D')
        self.option_three = customtkinter.CTkOptionMenu(self.option_row, fg_color='#2B2D31', dropdown_fg_color='#2B2D31', values=self.options, font=('Segoe UI', 13, 'normal'), button_color='#2B2D31', text_color='#787878', button_hover_color='#36383D')        
        self.option_four = customtkinter.CTkOptionMenu(self.option_row, fg_color='#2B2D31', dropdown_fg_color='#2B2D31', values=self.options, font=('Segoe UI', 13, 'normal'), button_color='#2B2D31', text_color='#787878', button_hover_color='#36383D')        

        # Buttons
        self.register_button = customtkinter.CTkButton(self, height=38, text='Register Account', text_color='#FFFFFF', fg_color='#248046', border_width=0, hover_color='#1B5C33', font=('Segoe UI', 15, 'bold'))
        self.toggle_button = customtkinter.CTkButton(self, height=20, text='Login to an account', text_color='#FFFFFF', fg_color='transparent', border_width=0, hover_color='#2F3236', font=('Segoe UI', 14, 'normal'), anchor='e')


    def create_layout(self, hide: bool) -> None:
        self.place(anchor=customtkinter.CENTER, relx=.5, rely=.5)
        self.pack_propagate(True)
        # Pack the lables
        self.title_label.pack(side=customtkinter.TOP, fill=customtkinter.X)
        self.info_text_one.pack(side=customtkinter.TOP, fill=customtkinter.X)
        self.first_name_entry.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(15, 0))
        self.last_name_entry.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(8, 0))
        self.info_text_four.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(15, 0))
        self.email_address_entry.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(4, 15))
        self.password_entry.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(8, 0))
        self.tutor_group_entry.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(8, 0))
        self.info_text_two.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(12, 0))
        self.option_row.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(4, 0))
        self.option_one.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True, padx=(0, 8))
        self.option_two.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True, padx=(0, 8))
        self.option_three.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True, padx=(0, 8))
        self.option_four.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True)
        self.info_text_three.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(22, 0))
        self.register_button.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(4, 0))
        self.toggle_button.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(8, 0))
        self.option_row.pack_propagate(False)
        if hide: self.toggle_page(True)

    
    def display_register_error(self, error_message: str) -> None:
        if self.error_created: self.error_label.configure(text=error_message); return
        self.error_label = customtkinter.CTkLabel(self, width=550, font=('Segoe UI', 13, 'normal'), anchor='nw', text_color='#F26C6C')
        self.error_label.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(5, 0))
        self.error_label.configure(text=error_message)
        self.error_created = True

            
    def toggle_freeze_page(self, freeze: bool) -> None:
        if freeze: self.register_button.configure(state='disabled', fg_color='#525252', text='Registering Account...')
        else: self.register_button.configure(state='normal', fg_color='#248046', text='Register Account')


    def toggle_page(self, hide: bool) -> None:
        if not hide: self.place(anchor='c', relx=.5, rely=.5)
        else: self.place_forget()
        self.displaying = not hide