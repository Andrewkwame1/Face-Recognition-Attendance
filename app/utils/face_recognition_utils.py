import logging
import numpy as np
from typing import Optional

try:
    import face_recognition
    import cv2

    HAS_FACE_LIB = True
except ImportError as e:
    logging.warning(
        f"face_recognition or opencv-python-headless not installed. Face verification will be mocked. Error: {e}"
    )
    HAS_FACE_LIB = False
    face_recognition = None
    cv2 = None


def process_face_image(image_data: bytes) -> tuple[bool, Optional[object], str]:
    """
    Process an uploaded image byte stream.
    Returns: (success, encoding, message)
    """
    if not HAS_FACE_LIB:
        return (True, np.zeros(128), "Library missing, mock success")
    try:
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_img)
        if not face_locations:
            return (False, None, "No face detected in the image.")
        if len(face_locations) > 1:
            return (
                False,
                None,
                "Multiple faces detected. Please ensure only you are in the frame.",
            )
        encodings = face_recognition.face_encodings(rgb_img, face_locations)
        if not encodings:
            return (False, None, "Could not encode face.")
        return (True, encodings[0], "Face detected successfully.")
    except Exception as e:
        logging.exception(f"Error processing face: {e}")
        return (False, None, f"Error processing image: {str(e)}")


def compare_faces(
    known_encoding: object, check_encoding: object, tolerance: float = 0.6
) -> bool:
    """
    Compare two face encodings.
    """
    if not HAS_FACE_LIB:
        return True
    try:
        results = face_recognition.compare_faces(
            [known_encoding], check_encoding, tolerance=tolerance
        )
        return results[0]
    except Exception as e:
        logging.exception(f"Error comparing faces: {e}")
        return False