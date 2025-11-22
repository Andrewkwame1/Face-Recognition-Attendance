import reflex as rx
import uuid
from typing import TypedDict, Optional


class User(TypedDict):
    id: str
    name: str
    email: str
    password: str
    role: str


class AuthState(rx.State):
    users: list[User] = [
        {
            "id": "t1",
            "name": "Prof. Albus Dumbledore",
            "email": "teacher@test.com",
            "password": "password",
            "role": "teacher",
        },
        {
            "id": "s1",
            "name": "Harry Potter",
            "email": "student@test.com",
            "password": "password",
            "role": "student",
        },
        {
            "id": "s2",
            "name": "Hermione Granger",
            "email": "hermione@test.com",
            "password": "password",
            "role": "student",
        },
    ]
    current_user: Optional[User] = None
    login_email: str = ""
    login_password: str = ""
    register_name: str = ""
    register_email: str = ""
    register_password: str = ""
    register_role: str = "student"
    error_message: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.current_user is not None

    @rx.var
    def user_role(self) -> str:
        return self.current_user["role"] if self.current_user else ""

    @rx.var
    def user_name(self) -> str:
        return self.current_user["name"] if self.current_user else ""

    @rx.event
    def login(self):
        user = next(
            (
                u
                for u in self.users
                if u["email"] == self.login_email
                and u["password"] == self.login_password
            ),
            None,
        )
        if user:
            self.current_user = user
            self.error_message = ""
            return rx.redirect("/")
        else:
            self.error_message = "Invalid email or password."

    @rx.event
    def register(self):
        if any((u["email"] == self.register_email for u in self.users)):
            self.error_message = "Email already exists."
            return
        new_user: User = {
            "id": str(uuid.uuid4()),
            "name": self.register_name,
            "email": self.register_email,
            "password": self.register_password,
            "role": self.register_role,
        }
        self.users.append(new_user)
        self.current_user = new_user
        self.error_message = ""
        return rx.redirect("/")

    @rx.event
    def logout(self):
        self.current_user = None
        return rx.redirect("/login")

    @rx.event
    def set_login_email(self, email: str):
        self.login_email = email

    @rx.event
    def set_login_password(self, password: str):
        self.login_password = password

    @rx.event
    def set_register_name(self, name: str):
        self.register_name = name

    @rx.event
    def set_register_email(self, email: str):
        self.register_email = email

    @rx.event
    def set_register_password(self, password: str):
        self.register_password = password

    @rx.event
    def set_register_role(self, role: str):
        self.register_role = role