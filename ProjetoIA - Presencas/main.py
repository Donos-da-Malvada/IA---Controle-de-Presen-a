import cv2
from cv2 import face
import cv2.data
import os
import numpy as np
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def write_to_sheet(sheet_id, values):
    credentials = Credentials.from_service_account_file(
        'APIKEY/trabalhoDeIAAPIKEY.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )

    service = build('sheets', 'v4', credentials=credentials)

    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id, range='Página1!A:A',
        valueInputOption='USER_ENTERED', body=body
    ).execute()

    print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))

def prepare_training_data(data_folder_paths):
    faces = []
    labels = []
    label_names = {}

    label = 0
    for folder_path in data_folder_paths:
        for file_name in os.listdir(folder_path):
            if file_name.startswith("."):
                continue

            image_path = os.path.join(folder_path, file_name)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Imagem não carregada corretamente: {image_path}")
                continue

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(face) != 1:
                continue

            (x, y, w, h) = face[0]
            faces.append(gray[y:y+w, x:x+h])
            labels.append(label)

        label_names[label] = folder_path.split('/')[-1]  # Obtém apenas o nome do diretório
        label += 1

    return faces, labels, label_names

def current_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Lista dos diretórios a serem analisados
directories = ["datasets/Dani", "datasets/Jao", "datasets/SAM", "datasets/Vini"]
faces, labels, label_names = prepare_training_data(directories)

# Criar e treinar o reconhecedor facial
face_recognizer = face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))

# Função para prever o rosto
def predict(test_img):
    img = test_img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        label, confidence = face_recognizer.predict(roi_gray)

        if confidence < 50:
            cv2.putText(img, label_names[label], (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            return img, True, label_names[label]

    return img, False, None

webcam = cv2.VideoCapture(0)

validated_directories = set()  # Conjunto para armazenar diretórios já validados

while True:
    ret, frame = webcam.read()
    if not ret:
        break

    processed_frame, is_face_found, directory = predict(frame)

    # Exibir o frame processado
    cv2.imshow("Reconhecimento Facial", processed_frame)

    if is_face_found and directory not in validated_directories:
        print(f"Rosto reconhecido do diretório: {directory}")

        # Enviar dados para a planilha
        time_stamp = current_time()
        data = [[directory, time_stamp]]
        write_to_sheet('1V3fBr3cHjpOuvMSCEDaapgZ8lpfKzIddYvj6aZ9TQVk', data)

        validated_directories.add(directory)  # Adicionar diretório à lista de validados

    # Esc para sair
    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()