# src/dataset_processing.py
import face_recognition
import os
from utils import save_pickle, get_file_list

def process_criminal_dataset(image_folder, output_file):
    encodings = []
    names = []

    image_files = get_file_list(image_folder, file_extensions=['.jpg', '.png'])
    
    for image_path in image_files:
        img = face_recognition.load_image_file(image_path)
        img_encodings = face_recognition.face_encodings(img)

        if img_encodings:
            encoding = img_encodings[0]
            name = os.path.splitext(os.path.basename(image_path))[0]
            encodings.append(encoding)
            names.append(name)

    # Save the encodings and names
    data = {"encodings": encodings, "names": names}
    save_pickle(data, output_file)

if __name__ == "__main__":
    process_criminal_dataset("data/criminal_images", "models/face_encodings.pickle")
