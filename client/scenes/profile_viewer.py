from typing import Any

import customtkinter
from static.shared_types import UserDetails


class ProfileViewer(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTk) -> None:
        super().__init__(master, width=375, fg_color='#2B2D31', corner_radius=0)
        self.displaying = True
        self.createWidgets()
        self.createLayout()
        self.pack_forget()


    def createWidgets(self) -> None:
        # Create all the  widgets used for this frame. Main UI Element
        self.top_row = customtkinter.CTkFrame(self, fg_color='transparent', border_width=0)
        self.page_title = customtkinter.CTkLabel(self.top_row, height=30, fg_color='transparent', text_color='#FFFFFF', font=('Segoe UI', 20, 'bold'), text='Profile Viewer', anchor='w')
        self.close_button = customtkinter.CTkButton(self.top_row, fg_color='transparent', width=50, font=('Segoe UI', 15, 'normal'), text='Close')
        self.divider = customtkinter.CTkFrame(self, fg_color='#1F2123', height=2)
        
        self.profile_holder = customtkinter.CTkFrame(self, fg_color='#313338', height=75, border_width=0, corner_radius=5)
        self.profile_details_holder = customtkinter.CTkFrame(self.profile_holder, fg_color='transparent', border_width=0)
        self.profile_picture = customtkinter.CTkLabel(self.profile_holder, fg_color="#674343", width=50, height=50, corner_radius=100, text="")
        self.full_name = customtkinter.CTkLabel(self.profile_details_holder, fg_color='transparent', text_color='#FFFFFF', font=('Segoe UI', 18, 'bold'), text='Users Full name', anchor='sw')
        self.status = customtkinter.CTkLabel(self.profile_details_holder, fg_color='transparent', text_color='#6B6B6B', font=('Segoe UI', 12, 'normal'), text='Users status', anchor='nw')
        
        self.email = customtkinter.CTkLabel(self, height=40, fg_color='#313338', text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), text='Email: None', anchor='w', corner_radius=3) 
        self.tutor_group = customtkinter.CTkLabel(self, height=40, fg_color='#313338', text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), text='Tutor group: None', anchor='w', corner_radius=3) 
        self.option_one = customtkinter.CTkLabel(self, height=40, fg_color='#313338', text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), text='Option one: None', anchor='w', corner_radius=3) 
        self.option_two = customtkinter.CTkLabel(self, height=40, fg_color='#313338', text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), text='Option two: None', anchor='w', corner_radius=3) 
        self.option_three = customtkinter.CTkLabel(self, height=40, fg_color='#313338', text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), text='Option three: None', anchor='w', corner_radius=3) 
        self.option_four = customtkinter.CTkLabel(self, height=40, fg_color='#313338', text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), text='Option four: None', anchor='w', corner_radius=3) 
        self.points_ammount = customtkinter.CTkLabel(self, height=40, fg_color='#376949', text_color='#FFFFFF', font=('Segoe UI', 15, 'normal'), text='Points: None', anchor='w', corner_radius=3) 
        self.close_button.configure(command=lambda: self.togglePage(hide=True))


    def createLayout(self) -> None:
        self.pack(expand=False, side=customtkinter.RIGHT, fill=customtkinter.Y)
        self.pack_propagate(False)
        self.top_row.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=15, padx=30)
        self.page_title.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False)
        self.close_button.pack(side=customtkinter.RIGHT, fill=customtkinter.Y, expand=False)
        self.divider.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=0, padx=0)

        self.profile_holder.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=(20, 0), padx=30)
        self.profile_holder.pack_propagate(False)
        self.profile_picture.pack(side=customtkinter.LEFT, fill=customtkinter.NONE, expand=False, padx=10, anchor='w')
        self.profile_details_holder.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False, anchor=customtkinter.CENTER)
        self.full_name.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True)
        self.status.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True)
        
        self.email.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=(35, 0), padx=30)
        self.tutor_group.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=(10, 0), padx=30)
        self.option_one.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=(10, 0), padx=30)
        self.option_two.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=(10, 0), padx=30)
        self.option_three.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=(10, 0), padx=30)
        self.option_four.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=(10, 0), padx=30)
        self.points_ammount.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=(10, 0), padx=30)


    def show_profile(self, user_details: UserDetails, user_status: str) -> None:
        self.full_name.configure(text=f'{user_details["first_name"]} {user_details["last_name"]}')
        self.email.configure(text=f'School email:  {user_details["email"]}')
        self.tutor_group.configure(text=f'Tutor group:  {user_details["tutor_group"]}')
        self.option_one.configure(text=f'Option one:  {user_details["option_one"]}')
        self.option_two.configure(text=f'Option two:  {user_details["option_two"]}')
        self.option_three.configure(text=f'Option three:  {user_details["option_three"]}')
        self.option_four.configure(text=f'Option four:  {user_details["option_four"]}')
        self.points_ammount.configure(text=f'Points: {user_details["points"]}')
        self.status.configure(text=user_status)
        if user_status == 'Online': self.status.configure(text_color='#248046')
        else: self.status.configure(text_color='#B18C2D')
        self.togglePage(hide=False)


    def togglePage(self, hide: bool) -> None:
        if not hide: self.pack(expand=False, side=customtkinter.RIGHT, fill=customtkinter.Y)
        else: self.pack_forget()
        self.displaying = not hide