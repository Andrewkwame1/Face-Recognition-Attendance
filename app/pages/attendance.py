import reflex as rx
from app.states.attendance_state import AttendanceState
from app.states.auth_state import AuthState
from app.states.class_state import ClassState
from app.pages.auth import login_page


def attendance_page() -> rx.Component:
    current_session = AttendanceState.session_for_checkin
    geo_script = """
    var latInput = document.getElementById('lat_input');
    var lonInput = document.getElementById('lon_input');

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;

            if (latInput) {
                nativeInputValueSetter.call(latInput, position.coords.latitude);
                latInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
            if (lonInput) {
                nativeInputValueSetter.call(lonInput, position.coords.longitude);
                lonInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
            alert("Location captured!");
        }, function(error) {
            alert("Error capturing location: " + error.message);
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("scan-face", class_name="w-12 h-12 text-teal-500 mb-4 mx-auto"),
                rx.el.h1(
                    "Check-In",
                    class_name="text-3xl font-bold text-center text-gray-800 font-['Lora'] mb-2",
                ),
                rx.el.p(
                    "Please verify your identity and location.",
                    class_name="text-center text-gray-500 mb-8",
                ),
                rx.cond(
                    current_session,
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Session Info",
                                class_name="text-xs font-bold text-gray-400 uppercase tracking-wider",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "clock", class_name="w-4 h-4 text-teal-500 mr-2"
                                ),
                                rx.el.span(
                                    current_session["time"], class_name="font-medium"
                                ),
                                class_name="flex items-center mt-1",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Location Requirement",
                                class_name="text-xs font-bold text-gray-400 uppercase tracking-wider",
                            ),
                            rx.el.p(
                                f"Must be within {current_session['radius']}m of class location.",
                                class_name="text-sm text-gray-600 mt-1",
                            ),
                        ),
                        class_name="bg-gray-50 p-4 rounded-xl border border-gray-100 mb-6",
                    ),
                    rx.el.div("Loading session info...", class_name="text-center p-4"),
                ),
                rx.cond(
                    AttendanceState.check_in_message != "",
                    rx.el.div(
                        AttendanceState.check_in_message,
                        class_name=rx.cond(
                            AttendanceState.check_in_status == "success",
                            "bg-green-50 text-green-700 border-green-100",
                            rx.cond(
                                AttendanceState.check_in_status == "error",
                                "bg-red-50 text-red-700 border-red-100",
                                "bg-blue-50 text-blue-700 border-blue-100",
                            ),
                        )
                        + " p-4 rounded-xl border text-sm font-medium mb-6 text-center",
                    ),
                ),
                rx.cond(
                    AttendanceState.check_in_status == "success",
                    rx.el.div(
                        rx.icon(
                            "circle-check",
                            class_name="w-16 h-16 text-green-500 mx-auto mb-4",
                        ),
                        rx.el.a(
                            "Back to Dashboard",
                            href="/",
                            class_name="block w-full bg-gray-800 hover:bg-gray-900 text-white text-center font-medium py-3 rounded-lg transition-colors",
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Step 1: Capture Location",
                                class_name="block text-sm font-bold text-gray-700 mb-2",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("map-pin", class_name="w-5 h-5 mr-2"),
                                    "Get My Location",
                                    on_click=rx.call_script(geo_script),
                                    class_name="w-full flex items-center justify-center bg-white border-2 border-dashed border-gray-300 hover:border-teal-500 hover:text-teal-600 text-gray-500 font-medium py-3 rounded-xl transition-all mb-2",
                                ),
                                rx.cond(
                                    AttendanceState.current_lat != 0.0,
                                    rx.el.div(
                                        rx.icon(
                                            "check",
                                            class_name="w-4 h-4 text-green-500 mr-1",
                                        ),
                                        "Location acquired",
                                        class_name="text-xs text-green-600 flex items-center justify-center",
                                    ),
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.input(
                                id="lat_input",
                                class_name="hidden",
                                on_change=AttendanceState.update_current_lat,
                            ),
                            rx.el.input(
                                id="lon_input",
                                class_name="hidden",
                                on_change=AttendanceState.update_current_lon,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Step 2: Take Selfie",
                                class_name="block text-sm font-bold text-gray-700 mb-2",
                            ),
                            rx.upload.root(
                                rx.el.div(
                                    rx.icon(
                                        "camera",
                                        class_name="w-8 h-8 text-gray-400 mb-2",
                                    ),
                                    rx.el.span(
                                        "Tap to take photo",
                                        class_name="text-sm text-gray-500",
                                    ),
                                    class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-gray-300 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer",
                                ),
                                id="face_upload",
                                accept={"image/*": [".png", ".jpg", ".jpeg"]},
                                max_files=1,
                                class_name="mb-6 block",
                            ),
                        ),
                        rx.el.button(
                            rx.cond(
                                AttendanceState.check_in_status == "uploading",
                                rx.spinner(size="2"),
                                "Submit Check-In",
                            ),
                            on_click=AttendanceState.handle_check_in(
                                rx.upload_files(upload_id="face_upload")
                            ),
                            disabled=AttendanceState.check_in_status == "uploading",
                            class_name="w-full bg-teal-500 hover:bg-teal-600 disabled:bg-gray-300 text-white font-medium py-3 rounded-xl shadow-lg shadow-teal-100 transition-all transform hover:-translate-y-0.5",
                        ),
                    ),
                ),
                class_name="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100 relative",
            ),
            class_name="min-h-screen flex items-center justify-center bg-gray-50 p-4 font-['Lora']",
        )
    )