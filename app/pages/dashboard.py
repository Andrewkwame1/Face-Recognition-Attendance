import reflex as rx
from app.states.auth_state import AuthState
from app.states.class_state import ClassState
from app.components.sidebar import sidebar, mobile_header


def stat_card(title: str, value: str, icon: str, color_class: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-6 h-6 {color_class}"),
            class_name="p-3 rounded-full bg-white shadow-sm mr-4",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-800"),
        ),
        class_name="flex items-center p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow",
    )


def teacher_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_card("Total Classes", "4", "book", "text-blue-500"),
            stat_card("Total Students", "128", "users", "text-purple-500"),
            stat_card("Active Sessions", "2", "radio", "text-teal-500"),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Create New Class",
                    class_name="text-lg font-bold text-gray-800 mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.input(
                            placeholder="Class Name",
                            name="name",
                            class_name="w-full p-3 rounded-lg border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-teal-500 outline-none transition-all mb-3",
                        ),
                        rx.el.input(
                            placeholder="Subject",
                            name="subject",
                            class_name="w-full p-3 rounded-lg border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-teal-500 outline-none transition-all mb-3",
                        ),
                        rx.el.textarea(
                            placeholder="Description...",
                            name="description",
                            class_name="w-full p-3 rounded-lg border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-teal-500 outline-none transition-all mb-4 min-h-[100px]",
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="w-4 h-4 mr-2"),
                            "Create Class",
                            type="submit",
                            class_name="w-full flex items-center justify-center bg-teal-500 hover:bg-teal-600 text-white font-medium py-2 rounded-lg transition-colors",
                        ),
                    ),
                    on_submit=ClassState.create_class,
                ),
                class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 h-fit",
            ),
            rx.el.div(
                rx.el.h3(
                    "Your Classes", class_name="text-lg font-bold text-gray-800 mb-4"
                ),
                rx.el.div(
                    rx.foreach(
                        ClassState.teacher_classes,
                        lambda c: rx.el.a(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h4(
                                        c["name"],
                                        class_name="font-bold text-gray-800 text-lg",
                                    ),
                                    rx.el.span(
                                        c["subject"],
                                        class_name="text-xs font-semibold text-teal-600 bg-teal-50 px-2 py-1 rounded-full",
                                    ),
                                    class_name="flex justify-between items-start mb-2",
                                ),
                                rx.el.p(
                                    c["description"],
                                    class_name="text-sm text-gray-500 line-clamp-2 mb-4",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "users", class_name="w-4 h-4 text-gray-400 mr-2"
                                    ),
                                    rx.el.span(
                                        f"{c['student_count']} Students",
                                        class_name="text-sm text-gray-500",
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="p-6 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg hover:border-teal-100 transition-all cursor-pointer group",
                            ),
                            href=f"/classes/{c['id']}",
                        ),
                    ),
                    class_name="grid grid-cols-1 gap-4",
                ),
                class_name="md:col-span-2",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-8",
        ),
        class_name="w-full",
    )


def student_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_card("Attendance Rate", "92%", "percent", "text-teal-500"),
            stat_card("Classes Attended", "24", "check_check", "text-green-500"),
            stat_card("Missed Classes", "2", "circle_x", "text-red-500"),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Active Sessions", class_name="text-lg font-bold text-gray-800 mb-4"
                ),
                rx.cond(
                    ClassState.active_sessions_for_student.length() == 0,
                    rx.el.div(
                        rx.icon("coffee", class_name="w-12 h-12 text-gray-300 mb-2"),
                        rx.el.p(
                            "No active sessions right now.", class_name="text-gray-500"
                        ),
                        class_name="bg-white p-8 rounded-2xl border border-dashed border-gray-200 flex flex-col items-center justify-center text-center",
                    ),
                    rx.el.div(
                        rx.foreach(
                            ClassState.active_sessions_for_student,
                            lambda s: rx.el.div(
                                rx.el.div(
                                    rx.el.h4(
                                        "Defense Against Dark Arts",
                                        class_name="font-bold text-gray-800",
                                    ),
                                    rx.el.p(
                                        f"Started at {s['time']}",
                                        class_name="text-sm text-gray-500",
                                    ),
                                ),
                                rx.el.button(
                                    "Join Class",
                                    class_name="bg-teal-500 hover:bg-teal-600 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors shadow-sm",
                                ),
                                class_name="p-5 bg-white rounded-xl shadow-sm border border-gray-100 flex justify-between items-center hover:shadow-md transition-all",
                            ),
                        ),
                        class_name="space-y-4",
                    ),
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "Recent History", class_name="text-lg font-bold text-gray-800 mb-4"
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Class",
                                    class_name="text-left py-3 px-4 text-xs font-bold text-gray-500 uppercase bg-gray-50 rounded-tl-lg",
                                ),
                                rx.el.th(
                                    "Date",
                                    class_name="text-left py-3 px-4 text-xs font-bold text-gray-500 uppercase bg-gray-50",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="text-left py-3 px-4 text-xs font-bold text-gray-500 uppercase bg-gray-50 rounded-tr-lg",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                ClassState.student_history,
                                lambda s: rx.el.tr(
                                    rx.el.td(
                                        "Potions",
                                        class_name="py-3 px-4 text-sm text-gray-800 border-b border-gray-100",
                                    ),
                                    rx.el.td(
                                        s["date"],
                                        class_name="py-3 px-4 text-sm text-gray-600 border-b border-gray-100",
                                    ),
                                    rx.el.td(
                                        rx.el.span(
                                            "Present",
                                            class_name="inline-block px-2 py-1 text-xs font-bold text-green-700 bg-green-50 rounded-full",
                                        ),
                                        class_name="py-3 px-4 border-b border-gray-100",
                                    ),
                                ),
                            )
                        ),
                        class_name="w-full",
                    ),
                    class_name="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden",
                ),
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-8",
        ),
    )


def dashboard() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.el.div(
                    rx.el.h2(
                        f"Welcome back, {AuthState.user_name.split(' ')[0]}!",
                        class_name="text-3xl font-bold text-gray-800 mb-2 font-['Lora']",
                    ),
                    rx.el.p(
                        "Here's what's happening today.",
                        class_name="text-gray-500 mb-8",
                    ),
                    rx.cond(
                        AuthState.user_role == "teacher",
                        teacher_dashboard(),
                        student_dashboard(),
                    ),
                    class_name="max-w-6xl mx-auto",
                ),
                class_name="flex-1 p-6 md:p-10 md:ml-64 min-h-screen bg-gray-50/50",
            ),
            class_name="flex-1 flex flex-col min-h-screen",
        ),
        class_name="flex min-h-screen font-['Lora']",
    )