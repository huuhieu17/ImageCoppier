import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
user_folder = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_folder_path', methods=['POST'])
def save_folder_path():
    global user_folder
    data = request.json
    user_folder = data['folder']
    blob = data['blob']
    filepath = os.path.join(user_folder, 'edited_image.jpg')
    
    with open(filepath, 'wb') as f:
        f.write(blob)
    
    return jsonify({'filepath': filepath})

if __name__ == "__main__":
    app.run(debug=True)
