import cv2
import face_recognition
from config import VIDEO_OUTPUT_FOLDER
from utils import send_email_notification

def process_video(video_file, face_encodings, known_names):
    video_capture = cv2.VideoCapture(video_file)
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    codec = cv2.VideoWriter_fourcc(*'XVID')
    
    output_path = f'{VIDEO_OUTPUT_FOLDER}/output_video.avi'
    output_video = cv2.VideoWriter(output_path, codec, frame_rate, 
                                   (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), 
                                    int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    
    recording = False
    detected_criminal = None
    start_frame = None

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings_in_frame = face_recognition.face_encodings(rgb_frame, face_locations)
        
        criminal_detected = False
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings_in_frame):
            matches = face_recognition.compare_faces(face_encodings, face_encoding)
            if any(matches):
                match_index = matches.index(True)
                detected_criminal = known_names[match_index]
                criminal_detected = True
        
        if criminal_detected:
            if not recording:
                print(f"Started recording for {detected_criminal} at frame {int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))}")
                recording = True
                start_frame = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))
        
        if recording:
            output_video.write(frame)
            if not criminal_detected and start_frame is not None:
                print(f"Stopped recording for {detected_criminal}.")
                recording = False
                # Optionally, you could stop recording at this point or add more logic to handle end of recording

    video_capture.release()
    output_video.release()

    if detected_criminal:
        send_email_notification(detected_criminal, output_path)
