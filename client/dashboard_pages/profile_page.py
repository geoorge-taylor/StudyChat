from typing import Any

import customtkinter


class OptionWidget(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkScrollableFrame, option_title: str, option_value: str, can_edit: bool = True) -> None:
        super().__init__(master, height=40, width=750, fg_color='#2B2D31', border_width=0)
        self.title = customtkinter.CTkLabel(self, text=option_title, text_color='#787878', font=('Segoe UI', 16, 'normal'), anchor='w')
        self.edit_button = customtkinter.CTkButton(self, width=40, text='Edit', text_color='#248046', font=('Segoe UI', 16, 'normal'), anchor='w', fg_color='transparent', hover_color='#35383D')
        self.option_value = customtkinter.CTkLabel(self, text=option_value, text_color='#FFFFFF', font=('Segoe UI', 16, 'normal'), anchor='e')

        self.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, anchor=customtkinter.W, pady=(0, 8))
        self.title.pack(side=customtkinter.LEFT, fill=customtkinter.NONE, expand=False, padx=(15, 0))
        if can_edit: self.edit_button.pack(side=customtkinter.RIGHT, fill=customtkinter.NONE, expand=False, padx=(0, 15))
        self.option_value.pack(side=customtkinter.RIGHT, fill=customtkinter.NONE, expand=False, padx=(0, 5))
        self.pack_propagate(False)



class ProfilePage(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, hide: bool = False) -> None:
        super().__init__(master, fg_color='transparent', corner_radius=0)
        self.displaying = True
        self.create_widgets()
        self.create_layout(hide)
 

    def create_widgets(self) -> None:
        self.pageTitle = customtkinter.CTkLabel(self, height=30, fg_color='transparent', text_color='#FFFFFF', font=('Segoe UI', 20, 'bold'), text='View profile', anchor='w')
        self.titleDivider = customtkinter.CTkFrame(self, fg_color='#1F2123', height=2)
        self.options_scroll_frame = customtkinter.CTkScrollableFrame(self, width=750, fg_color='transparent', orientation='vertical', scrollbar_button_color='#313338')
        self.user_id_widget = OptionWidget(self.options_scroll_frame, option_title='User id', option_value='None', can_edit=False)
        self.points_widget = OptionWidget(self.options_scroll_frame, option_title='Points', option_value='None', can_edit=False)
        self.first_name_widget = OptionWidget(self.options_scroll_frame, option_title='First name', option_value='None')
        self.last_name_widget = OptionWidget(self.options_scroll_frame, option_title='Last name', option_value='None')
        self.linked_email_widget = OptionWidget(self.options_scroll_frame, option_title='Linked email', option_value='None')
        self.option_one_widget = OptionWidget(self.options_scroll_frame, option_title='Subject option one', option_value='None')
        self.option_two_widget = OptionWidget(self.options_scroll_frame, option_title='Subject option two', option_value='None')
        self.option_three_widget = OptionWidget(self.options_scroll_frame, option_title='Subject option three', option_value='None')
        self.option_four_widget = OptionWidget(self.options_scroll_frame, option_title='Subject option four', option_value='None')
        self.tutor_group_widget = OptionWidget(self.options_scroll_frame, option_title='Tutor group', option_value='None')


    def create_layout(self, hide: bool) -> None:
        self.pack(expand=True, fill=customtkinter.BOTH)
        self.pageTitle.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=15, padx=20)
        self.titleDivider.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=0, padx=0)
        self.options_scroll_frame.pack(side=customtkinter.TOP, fill=customtkinter.Y, expand=True, padx=20, pady=14, anchor=customtkinter.NW)
        if hide: self.toggle_page(True)


    def toggle_page(self, hide: bool) -> None:
        if not hide: self.pack(expand=True, fill=customtkinter.BOTH)
        else: self.pack_forget()
        self.displaying = not hide