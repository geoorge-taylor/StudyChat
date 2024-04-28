import customtkinter


class UserWidget(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkScrollableFrame, first_name: str, last_name: str, status: str):
        super().__init__(master, fg_color='transparent', corner_radius=0)
        self.profile_holder = customtkinter.CTkFrame(self, fg_color="transparent", corner_radius=0, width=240, height=75)
        self.profile_picture = customtkinter.CTkLabel(self, fg_color="#674343", width=40, height=40, corner_radius=100, text="")
        self.profile_name = customtkinter.CTkLabel(self.profile_holder, font=("Segoe UI", 16, "normal"), text=f"{first_name} {last_name}", anchor="sw", text_color="#FFFFFF", width=50)
        self.status = customtkinter.CTkLabel(self.profile_holder, font=("Segoe UI", 13, "normal"), text=status, anchor="nw", text_color="#248046")
        self.add_button = customtkinter.CTkButton(self, width=100, height=30, fg_color='#248046', font=("Segoe UI", 12, "bold"), text='Add to recipients', anchor='c', text_color='#FFFFFF')
        
        self.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=(0, 5))
        self.profile_picture.pack(side=customtkinter.LEFT, fill=None, expand=False, padx=(20, 10))
        self.profile_holder.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False)
        self.profile_name.pack(side=customtkinter.TOP, fill=customtkinter.BOTH, expand=True)
        self.status.pack(side=customtkinter.BOTTOM, fill=customtkinter.BOTH, expand=True)
        self.add_button.pack(side=customtkinter.RIGHT, fill=customtkinter.NONE, expand=False, padx=(0, 20))

        if status == 'Online': self.status.configure(text_color='#248046')
        else: self.status.configure(text_color='#B18C2D')

    
    def toggle_user_widget(self, selected: bool) -> None:
        if selected: self.add_button.configure(fg_color='#525252', text='Remove user')
        else: self.add_button.configure(fg_color='#248046', text='Add to recipients')



class AskQuestionPage(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkFrame, options: list[str], hide: bool = True):
        super().__init__(master, fg_color='transparent', corner_radius=0)
        self.error_created = False
        self.options = options
        self.displaying = True
        self.manual_searching = False
        self.create_widgets()
        self.create_layout(hide)


    def create_widgets(self) -> None:
        self.page_title = customtkinter.CTkLabel(self, height=30, fg_color='transparent', text_color='#FFFFFF', font=('Segoe UI', 20, 'bold'), text='Ask a question', anchor='w')
        self.title_divider = customtkinter.CTkFrame(self, fg_color='#1F2123', height=2)
        self.left_side = customtkinter.CTkFrame(self, fg_color='transparent', border_width=0)
        self.right_side = customtkinter.CTkFrame(self, fg_color='transparent', border_width=0)

        self.info_text_one = customtkinter.CTkLabel(self.left_side, height=40, width=750, fg_color='transparent', text='Pick a relevant subject for this question', text_color='#B3B3B3', font=('Segoe UI', 14, 'normal'), anchor='w')
        self.info_text_two = customtkinter.CTkLabel(self.left_side, height=40, width=750, fg_color='transparent', text='Does this question include second year content?', text_color='#B3B3B3', font=('Segoe UI', 14, 'normal'), anchor='w')
        self.info_text_three = customtkinter.CTkLabel(self.left_side, height=40, width=750, fg_color='transparent', text='Enter a date when this question will close', text_color='#B3B3B3', font=('Segoe UI', 14, 'normal'), anchor='w')
        self.info_text_four = customtkinter.CTkLabel(self.left_side, height=40, width=750, fg_color='transparent', text='Enter a title for your question. Make sure it is as brief and clear as possible', text_color='#B3B3B3', font=('Segoe UI', 14, 'normal'), anchor='w')
        self.info_text_five = customtkinter.CTkLabel(self.left_side, height=40, width=750, fg_color='transparent', text='Enter a description for your question. Give as much detail as possible.', text_color='#B3B3B3', font=('Segoe UI', 14, 'normal'), anchor='w')

        self.title_entry = customtkinter.CTkEntry(self.left_side, height=40, width=750, fg_color='#2B2D31', placeholder_text='Question title', placeholder_text_color='#787878', border_width=0, font=('Segoe UI', 15, 'normal'))
        self.subject_entry = customtkinter.CTkOptionMenu(self.left_side, height=40, width=750, fg_color='#2B2D31', dropdown_fg_color='#2B2D31', values=self.options, font=('Segoe UI', 15, 'normal'), button_color='#2B2D31', text_color='#787878', button_hover_color='grey')
        self.expires_entry = customtkinter.CTkEntry(self.left_side, height=40, width=750, fg_color='#2B2D31', placeholder_text='Use format YYYY-MM-DD', placeholder_text_color='#787878', border_width=0, font=('Segoe UI', 15, 'normal'))
        self.description_entry = customtkinter.CTkTextbox(self.left_side, height=200, width=750, fg_color='#2B2D31', font=('Segoe UI', 15, 'normal'))
        self.second_year_content_option= customtkinter.CTkOptionMenu(self.left_side, height=40, width=750, fg_color='#2B2D31', dropdown_fg_color='#2B2D31', values=['Yes', 'No'], font=('Segoe UI', 15, 'normal'), button_color='#2B2D31', text_color='#787878', button_hover_color='grey')
        self.ask_question_button = customtkinter.CTkButton(self.left_side, height=40, width=750, text='Ask question', text_color='#FFFFFF', fg_color='#248046', border_width=0, hover_color='#1B5C33', font=('Segoe UI', 17, 'bold'))
        self.toggle_manual_user_selection = customtkinter.CTkCheckBox(self.left_side, command=self.toggle_manual_user_search, width=750, height=40, fg_color='#313338', font=('Segoe UI', 14, 'normal'), text='Would you like to manually select the recipients of this question?', text_color='#B3B3B3')
        self.manual_user_search = customtkinter.CTkEntry(self.right_side, height=40, width=475, fg_color='#2B2D31', placeholder_text='Search users...', placeholder_text_color='#787878', border_width=0, font=('Segoe UI', 15, 'normal'))
        self.user_results = customtkinter.CTkScrollableFrame(self.right_side, width=450, height=400, fg_color='#2B2D31', border_width=0, orientation='vertical', scrollbar_button_color='#26272B')
        self.empty_label = customtkinter.CTkLabel(self.user_results, fg_color='transparent', text_color='#FFFFFF', font=('Segoe UI', 14, 'normal'), text='No users were found', anchor='w')


    def create_layout(self, hide: bool) -> None:
        self.pack(expand=True, fill=customtkinter.BOTH)
        self.page_title.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=15, padx=20)
        self.title_divider.pack(side=customtkinter.TOP, fill=customtkinter.X, expand=False, pady=0, padx=0)
        self.left_side.pack(side=customtkinter.LEFT, fill=customtkinter.Y, expand=False, pady=(12, 0), padx=20)
        self.info_text_four.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, anchor=customtkinter.W)
        self.title_entry.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, pady=(0, 12), anchor=customtkinter.W)
        self.info_text_one.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, anchor=customtkinter.W)
        self.subject_entry.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, pady=(0, 12), anchor=customtkinter.W)
        self.info_text_five.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, anchor=customtkinter.W)
        self.description_entry.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, pady=(0, 12), anchor=customtkinter.W)
        self.info_text_three.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, anchor=customtkinter.W)
        self.expires_entry.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, pady=(0, 10), anchor=customtkinter.W)
        self.info_text_two.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, anchor=customtkinter.W)
        self.second_year_content_option.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, pady=(0, 9), anchor=customtkinter.W)
        self.toggle_manual_user_selection.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, pady=(0, 9), anchor=customtkinter.W)
        self.ask_question_button.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, pady=(15, 0), anchor=customtkinter.W)
        self.manual_user_search.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, anchor=customtkinter.W, pady=(0, 12))
        self.user_results.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, anchor=customtkinter.W)
        self.empty_label.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, anchor=customtkinter.W)
        if hide: self.toggle_page(True)


    def display_error(self, error_message: str) -> None:
        if self.error_created: self.error_label.configure(text=error_message); return
        self.error_label = customtkinter.CTkLabel(self, width=550, font=('Segoe UI', 13, 'normal'), anchor='nw', text_color='#F26C6C')
        self.error_label.pack(side=customtkinter.TOP, fill=customtkinter.X, pady=(20, 0), padx=(20, 0))
        self.error_label.configure(text=error_message)
        self.error_created = True

            
    def toggle_freeze_page(self, freeze: bool) -> None:
        if freeze: self.ask_question_button.configure(state='disabled', fg_color='#525252', text='Asking question...')
        else: self.ask_question_button.configure(state='normal', fg_color='#248046', text='Ask question')

    
    def toggle_manual_user_search(self) -> None:
        if not self.manual_searching: 
            self.right_side.pack(
                side=customtkinter.LEFT, fill=customtkinter.Y, 
                expand=False, pady=(20, 0), padx=0, anchor=customtkinter.W
            ); self.manual_searching = True
        else: 
            self.right_side.pack_forget()
            self.manual_searching = False

    
    def get_user_search_entry(self) -> str:
        return self.manual_user_search.get()


    def clear_user_search_entry(self) -> None:
        self.manual_user_search.delete(0, customtkinter.END)

    
    def add_user_to_results(self, first_name: str, last_name: str, status: str) -> UserWidget:
        user_widget = UserWidget(self.user_results, first_name, last_name, status)
        return user_widget
    

    def toggle_empty_label(self, hide: bool) -> None:
        if not hide: self.empty_label.pack(side=customtkinter.TOP, fill=customtkinter.NONE, expand=False, anchor=customtkinter.W)
        else: self.empty_label.pack_forget()


    def toggle_page(self, hide: bool) -> None:
        if not hide: self.pack(expand=True,fill=customtkinter.BOTH)
        else: self.pack_forget()
        self.displaying = not hide