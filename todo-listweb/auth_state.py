import reflex as rx
from typing import Optional

class AuthState(rx.State):
    username: str = ""
    password: str = ""
    is_authenticated: bool = False
    login_error: str = ""
    
    def redirect_to_login(self):
        return rx.redirect("/")
    
    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/")
    
    
    def login(self):
        # Hard coded username and password, you can change it to whatever
        if self.username == "admin" and self.password == "password":
            self.is_authenticated = True
            self.login_error = ""
            return rx.redirect("/todo")
        else:
            self.login_error = "Wrong Username or Password"

    
    def logout(self):
        self.is_authenticated = False 
        self.username = ""
        self.password = ""
        return rx.redirect("/")    