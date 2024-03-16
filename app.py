import sys
import os
import wave
import json
from vosk import Model, KaldiRecognizer


# здесь необходимо указать папку с моделью
# Модель взята здесь https://alphacephei.com/vosk/models (Российская, маленькая 45Мб)
# Можно скачать и указать другую модель

modelFolderName = "vosk-model-small-ru-0.22"

# Имя файла с результатом
fileInputName = 'speech.wav'
fileOutputName = 'speech.txt'

# Проверяем наличие модели 
if not os.path.exists(modelFolderName):
    print ("Модель не найдена. Скачайте ее здесь https://alphacephei.com/vosk/models и распакуйте в папку с программой.")
    exit (1)

def main() -> None:

    wf = wave.open(fileInputName, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Неверный формат аудиофайла: ожидаемый тип: .wav!")
        exit(1)

    model = Model(modelFolderName)
    recognizer = KaldiRecognizer(model, wf.getframerate())

    with open(fileOutputName, 'w', encoding='utf-8') as file:

        while True:
            data = wf.readframes(4000)

            if (len(data) == 0):
                break

            if (recognizer.AcceptWaveform(data)):
                break

            # Для отладки
            #print(recognizer.PartialResult())

            pass

        resultText = json.loads(recognizer.Result())
        # print("Результат: ", rec_text)

        file.write(resultText.get("text"))
        file.close()
  
if (len(sys.argv) >= 2):
        fileInputName = sys.argv[1]
        print("Выбран входной файл: ", fileInputName)

if (len(sys.argv) == 3):
    fileOutputName = sys.argv[2]
    print("Выбран выходной файл: ", fileOutputName)

main()