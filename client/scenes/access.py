import customtkinter
from access_pages import login_page, register_page, verification_page
from static.shared_types import UserDetails


class Access(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, options: list[str], hide: bool = True) -> None:
        super().__init__(master, fg_color='transparent', corner_radius=0)
        self.pack(expand=True, fill=customtkinter.BOTH)
        if hide: self.toggle_frame(True)
        self.displaying = True 

        self.register_page = register_page.RegisterPage(self, options=options, hide=False)
        self.verification_page = verification_page.VerificationPage(self, hide=True)
        self.login_page = login_page.LoginPage(self, hide=True)
        self.access_pages = {'register': self.register_page, 'login': self.login_page,
                            'verification': self.verification_page}
        
        self.bind_buttons()

    
    def bind_buttons(self) -> None:
        self.register_page.toggle_button.bind('<Button-1>', lambda _: self.switch_page(_to='login'))
        self.login_page.toggle_button.bind('<Button-1>', lambda _: self.switch_page(_to='register'))
        self.verification_page.toggle_button.bind('<Button-1>', lambda _: self.switch_page(_to='register'))

    
    def get_register_details(self) -> UserDetails:
        return {
            'first_name': self.register_page.first_name_entry.get(),
            'last_name': self.register_page.last_name_entry.get(),
            'email': self.register_page.email_address_entry.get(),
            'tutor_group': self.register_page.tutor_group_entry.get(),
            'password': self.register_page.password_entry.get(),
            'option_one': self.register_page.option_one.get(),
            'option_two': self.register_page.option_two.get(),
            'option_three': self.register_page.option_three.get(),
            'option_four': self.register_page.option_four.get(),
            'points': 0
        }
    

    def get_login_details(self) -> tuple[str, str]:
        email = self.login_page.email_address_entry.get()
        password = self.login_page.password_entry.get()
        return email, password


    def switch_page(self, _to: str) -> None:
        if not self.access_pages[_to].displaying: 
            for page in self.access_pages.values():
                if page.displaying: page.toggle_page(True)
            self.access_pages[_to].toggle_page(False)


    def toggle_frame(self, hide: bool) -> None:
        if not hide: self.pack(expand=True, fill=customtkinter.BOTH)
        else: self.pack_forget()
        self.displaying = not hide