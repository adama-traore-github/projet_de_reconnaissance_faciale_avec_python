
import os
import face_recognition
from PIL import Image, ImageDraw, ImageFont
import cv2

# Global variable for save path
SAVE_PATH = ""

# Chemin vers le répertoire contenant les images connues
DIRECTORY_PATH = "C:/Users/HP/Desktop/AROLD/projet/aaa"

# Liste des fichiers dans le répertoire
IMAGE_FILES = os.listdir(DIRECTORY_PATH)

# Encodages faciaux des images connues
KNOWN_FACE_ENCODINGS = []
KNOWN_FACE_NAMES = []

# Charger les images connues et obtenir leurs encodages
for file_name in IMAGE_FILES:
    image = face_recognition.load_image_file(os.path.join(DIRECTORY_PATH, file_name))
    face_encoding = face_recognition.face_encodings(image)[0]
    KNOWN_FACE_ENCODINGS.append(face_encoding)
    person_name = os.path.splitext(os.path.basename(file_name))[0]
    KNOWN_FACE_NAMES.append(person_name)

# Function to display a welcome message and prompt the user to choose whether to save results
def welcome_and_choose_save():
    print("Bienvenue!")
    print("Voulez-vous sauvegarder les résultats de la reconnaissance faciale?")
    print("1. Oui")
    print("2. Non")
    choice = input("Entrez votre choix (1 ou 2) : ")
    
    if choice == '1':
        global SAVE_PATH
        SAVE_PATH = input("Entrez le chemin de sauvegarde des résultats : ")

# Function to perform facial recognition with an image
def reconnaissance_faciale_image(image_path):
    # Charger l'image inconnue
    image_unknown = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image_unknown)
    pil_image = Image.fromarray(image_unknown)
    draw = ImageDraw.Draw(pil_image)
    face_locations = face_recognition.face_locations(image_unknown)

    # Si aucun visage n'est détecté, afficher un message
    if not face_locations:
        print("Aucun visage n'a été détecté dans l'image.")
        return

    # Comparer les encodages avec les visages connus
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(KNOWN_FACE_ENCODINGS, face_encoding)
        name = "Inconnu"

        if True in matches:
            first_match_index = matches.index(True)
            name = KNOWN_FACE_NAMES[first_match_index]

        draw.rectangle(((left, top), (right, bottom)), outline="blue")
        draw.text((left, top - 20), name, fill="red", font=ImageFont.truetype("arial.ttf", 20))

        pil_image.show()

    # Sauvegarder l'image avec les résultats si un chemin de sauvegarde a été spécifié
    if SAVE_PATH:
        image_filename = os.path.basename(image_path)
        result_image_path = os.path.join(SAVE_PATH, "result_" + image_filename)
        pil_image.save(result_image_path)
        print(f"Résultats sauvegardés dans : {result_image_path}")


# Function to perform facial recognition with a videodef reconnaissance_faciale_video(video_path):
def reconnaissance_faciale_video(video_path):
    video_capture = cv2.VideoCapture(video_path)
    

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb_frame)
        encodings_faces = face_recognition.face_encodings(rgb_frame, faces)

        for (top, right, bottom, left), encodage_face in zip(faces, encodings_faces):
            nom_personne = "Inconnu"
            

            for nom, encodage in zip(KNOWN_FACE_NAMES, KNOWN_FACE_ENCODINGS):
                distance = face_recognition.face_distance([encodage], encodage_face)[0]

                if distance < 0.6:
                    nom_personne = nom
                    break

            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.putText(frame, nom_personne, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        cv2.imshow('Video', frame)

        # Sauvegarder la dernière frame de la vidéo avec les résultats si un chemin de sauvegarde a été spécifié
        if SAVE_PATH:
            frame_filename = "result_video_frame.jpg"
            result_frame_path = os.path.join(SAVE_PATH, frame_filename)
            cv2.imwrite(result_frame_path, frame)
            print(f"Dernière frame de la vidéo avec les résultats sauvegardée dans : {result_frame_path}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Afficher un message si aucun visage n'a été détecté
    if not faces:
        print("Aucun visage n'a été détecté dans la vidéo.")

    video_capture.release()
    cv2.destroyAllWindows()
    # Afficher un message si aucun visage n'a été détecté
   
def reconnaissance_faciale_temps_reel():
    video_capture = cv2.VideoCapture(0)
    

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb_frame)
        encodings_faces = face_recognition.face_encodings(rgb_frame, faces)

        for (top, right, bottom, left), encodage_face in zip(faces, encodings_faces):
            nom_personne = "Inconnu"
            

            for nom, encodage in zip(KNOWN_FACE_NAMES, KNOWN_FACE_ENCODINGS):
                distance = face_recognition.face_distance([encodage], encodage_face)[0]

                if distance < 0.6:
                    nom_personne = nom
                    break

            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.putText(frame, nom_personne, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        cv2.imshow('Video', frame)

        # Sauvegarder la dernière frame de la vidéo avec les résultats si un chemin de sauvegarde a été spécifié
        if SAVE_PATH:
            frame_filename = "result_realtime_frame.jpg"
            result_frame_path = os.path.join(SAVE_PATH, frame_filename)
            cv2.imwrite(result_frame_path, frame)
            print(f"Dernière frame de la vidéo avec les résultats sauvegardée dans : {result_frame_path}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Afficher un message si aucun visage n'a été détecté
    if not faces:
        print("Aucun visage n'a été détecté en temps réel.")

    video_capture.release()
    cv2.destroyAllWindows()

# Main function
def main():
    welcome_and_choose_save()
    
    # Display recognition options after choosing whether to save results
    print("Choisissez une option :")
    print("1. Reconnaissance faciale avec une image")
    print("2. Reconnaissance faciale avec une vidéo")
    print("3. Reconnaissance faciale en temps réel")
    choix = input("Entrez votre choix (1, 2 ou 3) : ")

    if choix == '1':
        image_path = input("Entrez le chemin de l'image : ")
        reconnaissance_faciale_image(image_path)
    elif choix == '2':
        video_path = input("Entrez le chemin de la vidéo : ")
        reconnaissance_faciale_video(video_path)
    elif choix == '3':
        reconnaissance_faciale_temps_reel()
    else:
        print("Choix invalide. Veuillez choisir 1, 2 ou 3.")

# Run the main function
if __name__ == "__main__":
    main()
