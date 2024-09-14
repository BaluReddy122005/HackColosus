import face_recognition
import pickle
import os

def process_images(image_folder, encoding_file):
    face_encodings = []
    known_names = []

    # Iterate over each file in the directory
    for image_name in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_name)
        
        # Skip non-image files
        if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        
        try:
            # Load the image file
            image = face_recognition.load_image_file(image_path)
            
            # Find all face locations and encodings in the image
            face_locations = face_recognition.face_locations(image)
            face_encodings_in_image = face_recognition.face_encodings(image, face_locations)
            
            # Assuming each image contains only one face
            for face_encoding in face_encodings_in_image:
                face_encodings.append(face_encoding)
                known_names.append(os.path.splitext(image_name)[0])  # Use image name without extension as name

        except Exception as e:
            print(f"Could not process file {image_name}: {e}")

    # Save the encodings and names to a pickle file
    with open(encoding_file, 'wb') as f:
        pickle.dump((face_encodings, known_names), f)

    print(f"Face encodings saved to {encoding_file}")

if __name__ == "__main__":
    image_folder = "data/criminal_images"  # Folder containing the criminal images
    encoding_file = "models/face_encodings.pickle"  # Path to save the pickle file
    process_images(image_folder, encoding_file)
