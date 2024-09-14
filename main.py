from src.dataset_processing import process_criminal_dataset
from src.video_processing import process_video
from utils import load_pickle

def main():
    # Load face encodings
    face_encodings, known_names = load_pickle('models/face_encodings.pickle')
    print("Criminal encodings found. Loading from models/face_encodings.pickle...")
    print(f"Loaded {len(face_encodings)} criminal encodings.")

    # Process the video
    video_file = 'data/videos/video_footage.mp4'
    process_video(video_file, face_encodings, known_names)

if __name__ == "__main__":
    main()
