import reflex as rx
from app.pages.auth import login_page, register_page
from app.pages.dashboard import dashboard
from app.pages.class_detail import class_detail_page
from app.pages.session_detail import session_detail_page
from app.pages.attendance import attendance_page
from app.states.auth_state import AuthState
from app.states.class_state import ClassState
from app.states.attendance_state import AttendanceState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(dashboard, route="/")
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(
    class_detail_page, route="/classes/[class_id]", on_load=ClassState.load_class_detail
)
app.add_page(
    session_detail_page,
    route="/sessions/[session_id]",
    on_load=ClassState.load_session_detail,
)
app.add_page(
    attendance_page,
    route="/attend/[session_id]",
    on_load=AttendanceState.load_checkin_session_from_params,
)