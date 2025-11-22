import reflex as rx
import math
import time
import uuid
import logging
from typing import TypedDict, Optional
from app.states.auth_state import AuthState
from app.states.class_state import ClassState, SessionItem
from app.utils.face_recognition_utils import process_face_image


class AttendanceRecord(TypedDict):
    id: str
    session_id: str
    student_id: str
    student_name: str
    timestamp: str
    latitude: float
    longitude: float
    status: str


class AttendanceState(rx.State):
    attendance_records: list[AttendanceRecord] = []
    current_lat: float = 0.0
    current_lon: float = 0.0
    check_in_status: str = "idle"
    check_in_message: str = ""
    check_in_session_id: str = ""
    uploaded_file_name: str = ""

    @rx.var
    async def session_for_checkin(self) -> Optional[SessionItem]:
        """Get the session details for the current check-in page."""
        class_state = await self.get_state(ClassState)
        for session in class_state.sessions:
            if session["id"] == self.check_in_session_id:
                return session
        return None

    @rx.event
    async def load_checkin_session(self, session_id: str):
        self.check_in_session_id = session_id
        self.check_in_status = "idle"
        self.check_in_message = ""
        self.current_lat = 0.0
        self.current_lon = 0.0

    @rx.event
    async def load_checkin_session_from_params(self):
        session_id = self.router.page.params.get("session_id", "")
        logging.info(
            f"Loading attendance check-in. Route param session_id: {session_id}"
        )
        await self.load_checkin_session(session_id)

    @rx.event
    def set_location(self, lat: str, lon: str):
        try:
            self.current_lat = float(lat)
            self.current_lon = float(lon)
            self.check_in_message = "Location captured successfully."
        except ValueError as e:
            logging.exception(f"Error parsing coordinates: {e}")
            self.check_in_message = "Invalid coordinates received."

    @rx.event
    def update_current_lat(self, val: str):
        try:
            self.current_lat = float(val)
        except ValueError as e:
            logging.exception(f"Error updating latitude: {e}")

    @rx.event
    def update_current_lon(self, val: str):
        try:
            self.current_lon = float(val)
        except ValueError as e:
            logging.exception(f"Error updating longitude: {e}")

    @rx.event
    async def handle_check_in(self, files: list[rx.UploadFile]):
        """Process the check-in attempt: Verify Location -> Verify Face -> Record Attendance"""
        self.check_in_status = "uploading"
        class_state = await self.get_state(ClassState)
        auth_state = await self.get_state(AuthState)
        current_user = auth_state.current_user
        if not current_user or current_user["role"] != "student":
            self.check_in_status = "error"
            self.check_in_message = "You must be logged in as a student to check in."
            return
        session = next(
            (s for s in class_state.sessions if s["id"] == self.check_in_session_id),
            None,
        )
        if not session:
            self.check_in_status = "error"
            self.check_in_message = "Session not found."
            return
        if session["status"] != "active":
            self.check_in_status = "error"
            self.check_in_message = "This session is not active."
            return
        if self.current_lat == 0.0 or self.current_lon == 0.0:
            self.check_in_status = "error"
            self.check_in_message = (
                "Location not captured. Please enable GPS and click 'Get Location'."
            )
            return
        R = 6371000
        phi1 = math.radians(session["latitude"])
        phi2 = math.radians(self.current_lat)
        dphi = math.radians(self.current_lat - session["latitude"])
        dlambda = math.radians(self.current_lon - session["longitude"])
        a = (
            math.sin(dphi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        if distance > session["radius"]:
            self.check_in_status = "error"
            self.check_in_message = f"You are {int(distance)}m away from the class. Please be within {session['radius']}m."
            return
        if not files:
            self.check_in_status = "error"
            self.check_in_message = "Please take a photo."
            return
        file = files[0]
        upload_data = await file.read()
        success, encoding, msg = process_face_image(upload_data)
        if not success:
            self.check_in_status = "error"
            self.check_in_message = msg
            return
        existing = next(
            (
                r
                for r in self.attendance_records
                if r["session_id"] == session["id"]
                and r["student_id"] == current_user["id"]
            ),
            None,
        )
        if existing:
            self.check_in_status = "error"
            self.check_in_message = "You have already checked in!"
            return
        new_record: AttendanceRecord = {
            "id": str(uuid.uuid4()),
            "session_id": session["id"],
            "student_id": current_user["id"],
            "student_name": current_user["name"],
            "timestamp": time.strftime("%I:%M %p"),
            "latitude": self.current_lat,
            "longitude": self.current_lon,
            "status": "present",
        }
        self.attendance_records.insert(0, new_record)
        for i, s in enumerate(class_state.sessions):
            if s["id"] == session["id"]:
                class_state.sessions[i]["attendee_count"] += 1
                break
        self.check_in_status = "success"
        self.check_in_message = "Attendance recorded successfully!"

    @rx.var
    async def current_session_records(self) -> list[AttendanceRecord]:
        """Return attendance records for the currently viewed session in ClassState"""
        class_state = await self.get_state(ClassState)
        return [
            r
            for r in self.attendance_records
            if r["session_id"] == class_state.current_session_id
        ]

    @rx.var
    def session_attendance_list(self) -> list[AttendanceRecord]:
        """Return attendance records for the currently viewed session in ClassState"""
        return []

    @rx.event
    def get_records_for_session(self, session_id: str) -> list[AttendanceRecord]:
        return [r for r in self.attendance_records if r["session_id"] == session_id]