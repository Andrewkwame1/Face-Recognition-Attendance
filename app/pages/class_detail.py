import reflex as rx
from app.states.class_state import ClassState
from app.states.auth_state import AuthState
from app.components.sidebar import sidebar, mobile_header
from app.pages.auth import login_page


def class_detail_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.cond(
                    ClassState.current_class,
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.a(
                                    rx.icon("arrow-left", class_name="w-5 h-5 mr-2"),
                                    "Back to Dashboard",
                                    href="/",
                                    class_name="flex items-center text-gray-500 hover:text-teal-600 mb-6 transition-colors text-sm font-medium",
                                ),
                                rx.el.div(
                                    rx.el.h1(
                                        ClassState.current_class["name"],
                                        class_name="text-3xl md:text-4xl font-bold text-gray-900 mb-2 font-['Lora']",
                                    ),
                                    rx.el.p(
                                        ClassState.current_class["description"],
                                        class_name="text-lg text-gray-600",
                                    ),
                                    class_name="mb-8",
                                ),
                                rx.el.div(
                                    rx.el.button(
                                        rx.icon(
                                            "circle_plus", class_name="w-5 h-5 mr-2"
                                        ),
                                        "Start New Session",
                                        on_click=ClassState.open_create_session_modal,
                                        class_name="flex items-center bg-teal-500 hover:bg-teal-600 text-white px-6 py-3 rounded-xl font-medium shadow-md hover:shadow-lg transition-all transform hover:-translate-y-0.5",
                                    ),
                                    class_name="flex justify-end mb-8",
                                ),
                            ),
                            class_name="max-w-6xl mx-auto",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "Class Sessions",
                                    class_name="text-xl font-bold text-gray-800 mb-4",
                                ),
                                rx.el.div(
                                    rx.foreach(
                                        ClassState.current_class_sessions,
                                        lambda s: rx.el.a(
                                            rx.el.div(
                                                rx.el.div(
                                                    rx.el.p(
                                                        s["date"],
                                                        class_name="font-bold text-gray-800",
                                                    ),
                                                    rx.el.p(
                                                        s["time"],
                                                        class_name="text-sm text-gray-500",
                                                    ),
                                                ),
                                                rx.el.div(
                                                    rx.el.span(
                                                        rx.cond(
                                                            s["status"] == "active",
                                                            "Active",
                                                            "Completed",
                                                        ),
                                                        class_name=rx.cond(
                                                            s["status"] == "active",
                                                            "bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide",
                                                            "bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide",
                                                        ),
                                                    ),
                                                    rx.el.span(
                                                        f"{s['attendee_count']} Attendees",
                                                        class_name="ml-4 text-sm text-gray-600",
                                                    ),
                                                    class_name="flex items-center",
                                                ),
                                                class_name="flex items-center justify-between p-4 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all cursor-pointer",
                                            ),
                                            href=f"/sessions/{s['id']}",
                                        ),
                                    ),
                                    class_name="space-y-3",
                                ),
                                class_name="md:col-span-2",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    "Student Roster",
                                    class_name="text-xl font-bold text-gray-800 mb-4",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.foreach(
                                            ClassState.student_roster,
                                            lambda student: rx.el.div(
                                                rx.el.div(
                                                    rx.el.div(
                                                        student["name"][0],
                                                        class_name="w-8 h-8 rounded-full bg-teal-100 text-teal-600 flex items-center justify-center font-bold text-sm mr-3",
                                                    ),
                                                    rx.el.span(
                                                        student["name"],
                                                        class_name="font-medium text-gray-700",
                                                    ),
                                                    class_name="flex items-center",
                                                ),
                                                rx.el.div(
                                                    rx.el.span(
                                                        f"{student['attendance_rate']}%",
                                                        class_name="font-bold text-gray-800 text-sm",
                                                    ),
                                                    rx.el.div(
                                                        class_name="h-1.5 rounded-full bg-teal-500 mt-1 w-16",
                                                        style={
                                                            "opacity": student[
                                                                "attendance_rate"
                                                            ]
                                                            / 100
                                                        },
                                                    ),
                                                    class_name="text-right",
                                                ),
                                                class_name="flex items-center justify-between p-3 border-b border-gray-50 last:border-0 hover:bg-gray-50 transition-colors",
                                            ),
                                        ),
                                        class_name="bg-white rounded-xl border border-gray-100 shadow-sm p-2",
                                    )
                                ),
                                class_name="md:col-span-1",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto",
                        ),
                    ),
                    rx.el.div(
                        "Class not found", class_name="text-center text-gray-500 mt-20"
                    ),
                ),
                class_name="flex-1 p-6 md:p-10 md:ml-64 min-h-screen bg-gray-50/50",
            ),
            class_name="flex-1 flex flex-col min-h-screen",
        ),
        rx.cond(
            ClassState.show_create_session_modal,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Create New Session",
                            class_name="text-xl font-bold text-gray-800 mb-4",
                        ),
                        rx.el.p(
                            "Start a new attendance session for this class. A unique QR code will be generated.",
                            class_name="text-gray-500 text-sm mb-6",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Location Coordinates (Lat, Long)",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    type="text",
                                    disabled=True,
                                    class_name="w-full p-3 rounded-lg border border-gray-200 bg-gray-100 text-gray-500",
                                    default_value=ClassState.new_session_lat,
                                    key=ClassState.new_session_lat,
                                ),
                                rx.el.input(
                                    type="text",
                                    disabled=True,
                                    class_name="w-full p-3 rounded-lg border border-gray-200 bg-gray-100 text-gray-500",
                                    default_value=ClassState.new_session_long,
                                    key=ClassState.new_session_long,
                                ),
                                class_name="grid grid-cols-2 gap-4 mb-4",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Geofence Radius (meters)",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="number",
                                default_value=ClassState.new_session_radius,
                                on_change=ClassState.set_new_session_radius,
                                class_name="w-full p-3 rounded-lg border border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none transition-all",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Cancel",
                                on_click=ClassState.close_create_session_modal,
                                class_name="px-4 py-2 rounded-lg text-gray-600 hover:bg-gray-100 font-medium mr-2 transition-colors",
                            ),
                            rx.el.button(
                                "Create & Generate QR",
                                on_click=ClassState.create_session,
                                class_name="px-4 py-2 rounded-lg bg-teal-500 hover:bg-teal-600 text-white font-medium shadow-sm hover:shadow-md transition-all",
                            ),
                            class_name="flex justify-end items-center",
                        ),
                        class_name="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-md m-4 relative z-50",
                    ),
                    class_name="fixed inset-0 flex items-center justify-center z-50",
                ),
                rx.el.div(
                    class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
                    on_click=ClassState.close_create_session_modal,
                ),
                class_name="fixed inset-0 z-50",
            ),
        ),
        class_name="flex min-h-screen font-['Lora']",
    )