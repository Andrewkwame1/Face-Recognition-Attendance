import reflex as rx
import logging
import uuid
import datetime
from typing import TypedDict
from app.states.auth_state import AuthState
from app.utils.qr import generate_qr_code


class ClassItem(TypedDict):
    id: str
    name: str
    subject: str
    description: str
    teacher_id: str
    student_count: int


class SessionItem(TypedDict):
    id: str
    class_id: str
    date: str
    time: str
    status: str
    attendee_count: int
    latitude: float
    longitude: float
    radius: int
    qr_code: str
    link: str


class StudentAttendance(TypedDict):
    student_name: str
    status: str
    check_in_time: str


class StudentRosterItem(TypedDict):
    name: str
    attendance_rate: int


class ClassState(rx.State):
    classes: list[ClassItem] = [
        {
            "id": "c1",
            "name": "Defense Against the Dark Arts",
            "subject": "Magic",
            "description": "Practical defense techniques.",
            "teacher_id": "t1",
            "student_count": 25,
        },
        {
            "id": "c2",
            "name": "Potions",
            "subject": "Chemistry",
            "description": "Brewing glory.",
            "teacher_id": "t1",
            "student_count": 18,
        },
    ]
    sessions: list[SessionItem] = [
        {
            "id": "s1",
            "class_id": "c1",
            "date": "2023-10-25",
            "time": "10:00 AM",
            "status": "completed",
            "attendee_count": 24,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "radius": 100,
            "qr_code": generate_qr_code("http://localhost:3000/attend/s1"),
            "link": "http://localhost:3000/attend/s1",
        },
        {
            "id": "s2",
            "class_id": "c1",
            "date": "2023-10-27",
            "time": "10:00 AM",
            "status": "active",
            "attendee_count": 12,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "radius": 100,
            "qr_code": generate_qr_code("http://localhost:3000/attend/s2"),
            "link": "http://localhost:3000/attend/s2",
        },
        {
            "id": "s3",
            "class_id": "c2",
            "date": "2023-10-26",
            "time": "02:00 PM",
            "status": "completed",
            "attendee_count": 18,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "radius": 100,
            "qr_code": generate_qr_code("http://localhost:3000/attend/s3"),
            "link": "http://localhost:3000/attend/s3",
        },
    ]
    student_roster: list[StudentRosterItem] = [
        {"name": "Harry Potter", "attendance_rate": 95},
        {"name": "Hermione Granger", "attendance_rate": 100},
        {"name": "Ron Weasley", "attendance_rate": 88},
        {"name": "Draco Malfoy", "attendance_rate": 92},
        {"name": "Neville Longbottom", "attendance_rate": 85},
    ]
    current_class_id: str = ""
    current_session_id: str = ""
    show_create_session_modal: bool = False
    new_session_lat: float = 37.7749
    new_session_long: float = -122.4194
    new_session_radius: int = 100

    @rx.var
    async def teacher_classes(self) -> list[ClassItem]:
        return self.classes

    @rx.var
    def active_sessions_for_student(self) -> list[SessionItem]:
        return [s for s in self.sessions if s["status"] == "active"]

    @rx.var
    def student_history(self) -> list[SessionItem]:
        return [s for s in self.sessions if s["status"] == "completed"]

    @rx.var
    def current_class(self) -> ClassItem | None:
        return next((c for c in self.classes if c["id"] == self.current_class_id), None)

    @rx.var
    def current_class_sessions(self) -> list[SessionItem]:
        return [s for s in self.sessions if s["class_id"] == self.current_class_id]

    @rx.var
    def current_session(self) -> SessionItem | None:
        return next(
            (s for s in self.sessions if s["id"] == self.current_session_id), None
        )

    @rx.event
    def set_current_class(self, class_id: str):
        self.current_class_id = class_id

    @rx.event
    def set_current_session(self, session_id: str):
        self.current_session_id = session_id

    @rx.event
    def load_class_detail(self):
        class_id = self.router.page.params.get("class_id", "")
        logging.info(f"Loading class detail. Route param class_id: {class_id}")
        self.current_class_id = class_id

    @rx.event
    def load_session_detail(self):
        session_id = self.router.page.params.get("session_id", "")
        logging.info(f"Loading session detail. Route param session_id: {session_id}")
        self.current_session_id = session_id

    @rx.event
    async def create_class(self, form_data: dict):
        auth_state = await self.get_state(AuthState)
        new_class: ClassItem = {
            "id": str(uuid.uuid4()),
            "name": form_data.get("name", ""),
            "subject": form_data.get("subject", ""),
            "description": form_data.get("description", ""),
            "teacher_id": "t1",
            "student_count": 0,
        }
        self.classes.append(new_class)

    @rx.event
    def open_create_session_modal(self):
        self.show_create_session_modal = True

    @rx.event
    def close_create_session_modal(self):
        self.show_create_session_modal = False

    @rx.event
    def set_new_session_radius(self, value: str):
        try:
            self.new_session_radius = int(value)
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    def create_session(self):
        session_id = str(uuid.uuid4())
        link = f"http://localhost:3000/attend/{session_id}"
        qr_code = generate_qr_code(link)
        new_session: SessionItem = {
            "id": session_id,
            "class_id": self.current_class_id,
            "date": str(datetime.date.today()),
            "time": datetime.datetime.now().strftime("%I:%M %p"),
            "status": "active",
            "attendee_count": 0,
            "latitude": self.new_session_lat,
            "longitude": self.new_session_long,
            "radius": self.new_session_radius,
            "qr_code": qr_code,
            "link": link,
        }
        self.sessions.insert(0, new_session)
        self.show_create_session_modal = False
        return rx.redirect(f"/sessions/{session_id}")

    @rx.event
    def end_session(self):
        if self.current_session:
            self.current_session["status"] = "completed"
            for i, s in enumerate(self.sessions):
                if s["id"] == self.current_session_id:
                    self.sessions[i]["status"] = "completed"