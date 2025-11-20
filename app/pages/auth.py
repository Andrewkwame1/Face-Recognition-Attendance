import reflex as rx
from app.states.auth_state import AuthState


def auth_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("scan-face", class_name="w-12 h-12 text-teal-500 mb-4 mx-auto"),
                rx.el.h2(
                    "Attendify",
                    class_name="text-3xl font-bold text-center text-gray-800 font-['Lora'] mb-8",
                ),
                content,
                class_name="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100",
            ),
            class_name="min-h-screen flex items-center justify-center bg-gray-50 p-4",
        ),
        class_name="font-['Lora']",
    )


def login_page() -> rx.Component:
    return auth_layout(
        rx.el.div(
            rx.el.h3(
                "Welcome Back",
                class_name="text-xl font-semibold text-gray-700 mb-6 text-center",
            ),
            rx.cond(
                AuthState.error_message != "",
                rx.el.div(
                    AuthState.error_message,
                    class_name="bg-red-50 text-red-500 p-3 rounded-lg text-sm mb-4 border border-red-100 text-center",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Email Address",
                    class_name="block text-sm font-medium text-gray-600 mb-1",
                ),
                rx.el.input(
                    type="email",
                    placeholder="you@example.com",
                    on_change=AuthState.set_login_email,
                    class_name="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all bg-gray-50 focus:bg-white",
                    default_value=AuthState.login_email,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    class_name="block text-sm font-medium text-gray-600 mb-1",
                ),
                rx.el.input(
                    type="password",
                    placeholder="••••••••",
                    on_change=AuthState.set_login_password,
                    class_name="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all bg-gray-50 focus:bg-white",
                    default_value=AuthState.login_password,
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Sign In",
                on_click=AuthState.login,
                class_name="w-full bg-teal-500 hover:bg-teal-600 text-white font-medium py-3 rounded-lg transition-colors shadow-md hover:shadow-lg",
            ),
            rx.el.div(
                rx.el.span("Don't have an account? ", class_name="text-gray-500"),
                rx.el.a(
                    "Register",
                    href="/register",
                    class_name="text-teal-600 font-semibold hover:underline",
                ),
                class_name="mt-6 text-center text-sm",
            ),
        )
    )


def register_page() -> rx.Component:
    return auth_layout(
        rx.el.div(
            rx.el.h3(
                "Create Account",
                class_name="text-xl font-semibold text-gray-700 mb-6 text-center",
            ),
            rx.cond(
                AuthState.error_message != "",
                rx.el.div(
                    AuthState.error_message,
                    class_name="bg-red-50 text-red-500 p-3 rounded-lg text-sm mb-4 border border-red-100 text-center",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Full Name",
                    class_name="block text-sm font-medium text-gray-600 mb-1",
                ),
                rx.el.input(
                    type="text",
                    placeholder="John Doe",
                    on_change=AuthState.set_register_name,
                    class_name="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all bg-gray-50 focus:bg-white",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Email Address",
                    class_name="block text-sm font-medium text-gray-600 mb-1",
                ),
                rx.el.input(
                    type="email",
                    placeholder="you@example.com",
                    on_change=AuthState.set_register_email,
                    class_name="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all bg-gray-50 focus:bg-white",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    class_name="block text-sm font-medium text-gray-600 mb-1",
                ),
                rx.el.input(
                    type="password",
                    placeholder="••••••••",
                    on_change=AuthState.set_register_password,
                    class_name="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all bg-gray-50 focus:bg-white",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "I am a...",
                    class_name="block text-sm font-medium text-gray-600 mb-2",
                ),
                rx.el.div(
                    rx.el.label(
                        rx.el.input(
                            type="radio",
                            name="role",
                            value="student",
                            default_checked=True,
                            on_change=lambda: AuthState.set_register_role("student"),
                            class_name="sr-only peer",
                        ),
                        rx.el.span("Student", class_name="block w-full text-center"),
                        class_name="cursor-pointer py-2 px-4 rounded-lg border border-gray-200 peer-checked:bg-teal-50 peer-checked:border-teal-500 peer-checked:text-teal-700 text-gray-600 transition-all",
                    ),
                    rx.el.label(
                        rx.el.input(
                            type="radio",
                            name="role",
                            value="teacher",
                            on_change=lambda: AuthState.set_register_role("teacher"),
                            class_name="sr-only peer",
                        ),
                        rx.el.span("Teacher", class_name="block w-full text-center"),
                        class_name="cursor-pointer py-2 px-4 rounded-lg border border-gray-200 peer-checked:bg-teal-50 peer-checked:border-teal-500 peer-checked:text-teal-700 text-gray-600 transition-all",
                    ),
                    class_name="grid grid-cols-2 gap-4",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Sign Up",
                on_click=AuthState.register,
                class_name="w-full bg-teal-500 hover:bg-teal-600 text-white font-medium py-3 rounded-lg transition-colors shadow-md hover:shadow-lg",
            ),
            rx.el.div(
                rx.el.span("Already have an account? ", class_name="text-gray-500"),
                rx.el.a(
                    "Login",
                    href="/login",
                    class_name="text-teal-600 font-semibold hover:underline",
                ),
                class_name="mt-6 text-center text-sm",
            ),
        )
    )