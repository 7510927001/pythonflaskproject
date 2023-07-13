from flask import Flask, render_template, request
import os
import cv2

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'


def extract_frames(video_path):
    frames_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'frames')
    os.makedirs(frames_folder, exist_ok=True)

    
    cap = cv2.VideoCapture(video_path)

    frame_count = 0


    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

         
        frame_path = os.path.join(frames_folder, f'frame_{frame_count}.jpg')
        cv2.imwrite(frame_path, frame)

        frame_count += 1

    cap.release()


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
    
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        
        if file.filename == '':
            return 'No selected file'

    
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(video_path)

        
        extract_frames(video_path)

        
        frames_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'frames')
        frame_files = sorted(os.listdir(frames_folder))

        return render_template('index.html', frame_files=frame_files)

    return render_template('index.html')


if __name__ == '_main_':
    app.run(debug=True)