import reflex as rx
from app.states.class_state import ClassState
from app.states.attendance_state import AttendanceState
from app.states.auth_state import AuthState
from app.components.sidebar import sidebar, mobile_header


def session_detail_page() -> rx.Component:
    current_records = AttendanceState.current_session_records
    return rx.el.div(
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.cond(
                    ClassState.current_session,
                    rx.el.div(
                        rx.el.a(
                            rx.icon("arrow-left", class_name="w-5 h-5 mr-2"),
                            "Back to Class",
                            href=f"/classes/{ClassState.current_session['class_id']}",
                            class_name="flex items-center text-gray-500 hover:text-teal-600 mb-6 transition-colors text-sm font-medium",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h1(
                                        "Active Session",
                                        class_name="text-2xl font-bold text-gray-800 mb-2 font-['Lora']",
                                    ),
                                    rx.el.p(
                                        "Students can scan this QR code to mark attendance.",
                                        class_name="text-gray-500 mb-6",
                                    ),
                                    rx.el.div(
                                        rx.image(
                                            src=ClassState.current_session["qr_code"],
                                            class_name="w-64 h-64 mx-auto mb-6 border-4 border-white rounded-xl shadow-lg",
                                        ),
                                        class_name="bg-teal-50 p-8 rounded-2xl border border-teal-100 flex flex-col items-center mb-6",
                                    ),
                                    rx.el.div(
                                        rx.el.div(
                                            rx.el.p(
                                                "Session Link",
                                                class_name="text-xs font-bold text-gray-400 uppercase mb-1",
                                            ),
                                            rx.el.p(
                                                ClassState.current_session["link"],
                                                class_name="text-sm text-gray-600 font-mono truncate bg-gray-100 p-2 rounded select-all",
                                            ),
                                            class_name="mb-4",
                                        ),
                                        rx.el.div(
                                            rx.el.p(
                                                "Geofence Details",
                                                class_name="text-xs font-bold text-gray-400 uppercase mb-1",
                                            ),
                                            rx.el.div(
                                                rx.icon(
                                                    "map-pin",
                                                    class_name="w-4 h-4 mr-2 text-teal-500",
                                                ),
                                                rx.el.span(
                                                    f"Lat: {ClassState.current_session['latitude']}, Long: {ClassState.current_session['longitude']}",
                                                    class_name="text-sm text-gray-600 mr-4",
                                                ),
                                                rx.el.span(
                                                    f"Radius: {ClassState.current_session['radius']}m",
                                                    class_name="text-sm text-gray-600",
                                                ),
                                                class_name="flex items-center bg-gray-50 p-2 rounded border border-gray-100",
                                            ),
                                        ),
                                        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm",
                                    ),
                                    class_name="flex flex-col",
                                ),
                                class_name="md:col-span-1",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.div(
                                            rx.el.p(
                                                "Status",
                                                class_name="text-sm text-gray-500 font-medium",
                                            ),
                                            rx.el.p(
                                                rx.cond(
                                                    ClassState.current_session["status"]
                                                    == "active",
                                                    "Live Now",
                                                    "Ended",
                                                ),
                                                class_name="text-lg font-bold text-green-600",
                                            ),
                                        ),
                                        rx.el.button(
                                            "End Session",
                                            on_click=ClassState.end_session,
                                            class_name="bg-red-50 hover:bg-red-100 text-red-600 px-4 py-2 rounded-lg text-sm font-medium transition-colors",
                                            disabled=ClassState.current_session[
                                                "status"
                                            ]
                                            != "active",
                                        ),
                                        class_name="flex justify-between items-center p-6 bg-white rounded-2xl border border-gray-100 shadow-sm mb-6",
                                    ),
                                    rx.el.div(
                                        rx.el.h3(
                                            "Live Attendance",
                                            class_name="text-lg font-bold text-gray-800 mb-4",
                                        ),
                                        rx.el.div(
                                            rx.el.div(
                                                rx.el.p(
                                                    f"{ClassState.current_session['attendee_count']}",
                                                    class_name="text-4xl font-bold text-teal-600",
                                                ),
                                                rx.el.p(
                                                    "Students Present",
                                                    class_name="text-sm text-gray-500",
                                                ),
                                                class_name="text-center p-6 bg-teal-50 rounded-xl mb-6",
                                            ),
                                            rx.el.div(
                                                rx.cond(
                                                    current_records.length() > 0,
                                                    rx.el.div(
                                                        rx.foreach(
                                                            current_records,
                                                            lambda r: rx.el.div(
                                                                rx.el.div(
                                                                    rx.el.div(
                                                                        r[
                                                                            "student_name"
                                                                        ][0],
                                                                        class_name="w-8 h-8 rounded-full bg-teal-100 text-teal-600 flex items-center justify-center font-bold text-sm mr-3",
                                                                    ),
                                                                    rx.el.div(
                                                                        rx.el.p(
                                                                            r[
                                                                                "student_name"
                                                                            ],
                                                                            class_name="font-medium text-gray-800 text-sm",
                                                                        ),
                                                                        rx.el.p(
                                                                            f"Checked in at {r['timestamp']}",
                                                                            class_name="text-xs text-gray-500",
                                                                        ),
                                                                    ),
                                                                    class_name="flex items-center",
                                                                ),
                                                                rx.icon(
                                                                    "square_check",
                                                                    class_name="w-4 h-4 text-green-500",
                                                                ),
                                                                class_name="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg transition-colors",
                                                            ),
                                                        ),
                                                        class_name="space-y-1 max-h-[400px] overflow-y-auto pr-2",
                                                    ),
                                                    rx.el.p(
                                                        "No attendance recorded yet.",
                                                        class_name="text-center text-gray-400 text-sm italic py-4",
                                                    ),
                                                ),
                                                class_name="border-t border-gray-100 pt-6",
                                            ),
                                        ),
                                        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex-1",
                                    ),
                                    class_name="flex flex-col h-full",
                                ),
                                class_name="md:col-span-2",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-3 gap-8",
                        ),
                    ),
                    rx.el.div(
                        "Session not found or loading...",
                        class_name="text-center text-gray-500 mt-20",
                    ),
                ),
                class_name="flex-1 p-6 md:p-10 md:ml-64 min-h-screen bg-gray-50/50",
            ),
            class_name="flex-1 flex flex-col min-h-screen",
        ),
        class_name="flex min-h-screen font-['Lora']",
    )