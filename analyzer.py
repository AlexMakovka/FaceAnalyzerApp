import cv2
from deepface import DeepFace

def analyze_face(frame):
    try:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        print("[DEBUG] Анализируем кадр...")

        result = DeepFace.analyze(
            rgb,
            actions=['gender', 'age', 'emotion'],
            detector_backend='opencv',
            enforce_detection=True
        )

        if isinstance(result, list):
            result = result[0]

        region = result.get("region", {})
        x, y, w, h = region.get("x", 0), region.get("y", 0), region.get("w", 0), region.get("h", 0)

        return {
            "gender": result.get("gender", "—"),
            "age": int(result.get("age", 0)),
            "emotion": result.get("dominant_emotion", "—"),
            "region": (x, y, w, h)
        }

    except Exception as e:
        print(f"[ERROR] DeepFace не смог проанализировать лицо: {e}")
        return None