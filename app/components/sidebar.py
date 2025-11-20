import reflex as rx
from app.states.auth_state import AuthState


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="w-5 h-5 mr-3"),
            rx.el.span(text, class_name="font-medium text-sm"),
            class_name="flex items-center px-4 py-3 text-gray-600 hover:bg-teal-50 hover:text-teal-600 rounded-lg transition-all duration-200",
        ),
        href=href,
        class_name="block mb-1",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("scan-face", class_name="w-8 h-8 text-teal-500 mr-2"),
                rx.el.h1(
                    "Attendify",
                    class_name="text-xl font-bold text-gray-800 tracking-tight",
                ),
                class_name="flex items-center px-4 py-6 mb-4 border-b border-gray-100",
            ),
            rx.el.nav(
                rx.cond(
                    AuthState.user_role == "teacher",
                    rx.el.div(
                        rx.el.p(
                            "TEACHER",
                            class_name="px-4 text-xs font-bold text-gray-400 mb-2 mt-4",
                        ),
                        sidebar_item("Dashboard", "layout-dashboard", "/"),
                        sidebar_item("My Classes", "book-open", "/"),
                        sidebar_item("Reports", "bar-chart-3", "/"),
                    ),
                ),
                rx.cond(
                    AuthState.user_role == "student",
                    rx.el.div(
                        rx.el.p(
                            "STUDENT",
                            class_name="px-4 text-xs font-bold text-gray-400 mb-2 mt-4",
                        ),
                        sidebar_item("Dashboard", "layout-dashboard", "/"),
                        sidebar_item("My Attendance", "history", "/"),
                        sidebar_item("Profile", "user", "/"),
                    ),
                ),
                class_name="flex-1 px-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("user_pen", class_name="w-10 h-10 text-gray-400"),
                        rx.el.div(
                            rx.el.p(
                                AuthState.user_name,
                                class_name="text-sm font-bold text-gray-800 truncate",
                            ),
                            rx.el.p(
                                AuthState.user_role.capitalize(),
                                class_name="text-xs text-gray-500",
                            ),
                            class_name="ml-3 overflow-hidden",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.button(
                        rx.icon(
                            "log-out",
                            class_name="w-5 h-5 text-gray-500 hover:text-red-500 transition-colors",
                        ),
                        on_click=AuthState.logout,
                        class_name="ml-auto p-2 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex items-center justify-between w-full",
                ),
                class_name="p-4 border-t border-gray-100 mt-auto bg-gray-50/50",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden md:block w-64 h-screen bg-white border-r border-gray-200 fixed left-0 top-0 shadow-lg z-10",
    )


def mobile_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("scan-face", class_name="w-6 h-6 text-teal-500 mr-2"),
            rx.el.span("Attendify", class_name="font-bold text-lg text-gray-800"),
            class_name="flex items-center",
        ),
        rx.el.button(
            rx.icon("log-out", class_name="w-5 h-5 text-gray-600"),
            on_click=AuthState.logout,
        ),
        class_name="md:hidden flex items-center justify-between p-4 bg-white border-b border-gray-200 sticky top-0 z-20",
    )