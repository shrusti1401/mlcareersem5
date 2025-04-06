from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
import os

app = Flask(__name__, template_folder='templates')

# Updated model path
MODEL_PATH = r'C:\sihcareer\Career-Recommendation-System-using-ML\backend\modelnew.pkl'

# Load the updated model
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# Note: Your ML logic is assumed to be trained and saved from 'updated.ipynb'

# Feature list
feature_names = ['Drawing', 'Dancing', 'Singing', 'Sports', 'Video Game', 'Acting', 'Travelling',
                 'Gardening', 'Animals', 'Photography', 'Teaching', 'Exercise', 'Coding',
                 'Electricity Components', 'Mechanic Parts', 'Computer Parts', 'Researching',
                 'Architecture', 'Historic Collection', 'Botany', 'Zoology', 'Physics',
                 'Accounting', 'Economics', 'Sociology', 'Geography', 'Psycology', 'History',
                 'Science', 'Bussiness Education', 'Chemistry', 'Mathematics', 'Biology',
                 'Makeup', 'Designing', 'Content writing', 'Crafting', 'Literature', 'Reading',
                 'Cartooning', 'Debating', 'Asrtology', 'Hindi', 'French', 'English', 'Urdu',
                 'Other Language', 'Solving Puzzles', 'Gymnastics', 'Yoga', 'Engeeniering',
                 'Doctor', 'Pharmisist', 'Cycling', 'Knitting', 'Director', 'Journalism',
                 'Bussiness', 'Listening Music']

# Prediction labels
numeric_to_category = {
    0: 'Animation, Graphics and Multimedia',
    1: 'B.Arch- Bachelor of Architecture',
    2: 'B.Com- Bachelor of Commerce',
    3: 'B.Ed.',
    4: 'B.Sc- Applied Geology',
    5: 'B.Sc- Nursing',
    6: 'B.Sc. Chemistry',
    7: 'B.Sc. Mathematics',
    8: 'B.Sc.- Information Technology',
    9: 'B.Sc.- Physics',
    10: 'B.Tech.-Civil Engineering',
    11: 'B.Tech.-Computer Science and Engineering',
    12: 'B.Tech.-Electrical and Electronics Engineering',
    13: 'B.Tech.-Electronics and Communication Engineering',
    14: 'B.Tech.-Mechanical Engineering',
    15: 'BA in Economics',
    16: 'BA in English',
    17: 'BA in Hindi',
    18: 'BA in History',
    19: 'BBA- Bachelor of Business Administration',
    20: 'BBS- Bachelor of Business Studies',
    21: 'BCA- Bachelor of Computer Applications',
    22: 'BDS- Bachelor of Dental Surgery',
    23: 'BEM- Bachelor of Event Management',
    24: 'BFD- Bachelor of Fashion Designing',
    25: 'BJMC- Bachelor of Journalism and Mass Communication',
    26: 'BPharma- Bachelor of Pharmacy',
    27: 'BTTM- Bachelor of Travel and Tourism Management',
    28: 'BVA- Bachelor of Visual Arts',
    29: 'CA- Chartered Accountancy',
    30: 'CS- Company Secretary',
    31: 'Civil Services',
    32: 'Diploma in Dramatic Arts',
    33: 'Integrated Law Course- BA + LL.B',
    34: 'MBBS'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        input_data = {feature: float(data.get(feature, 0)) for feature in feature_names}
        df = pd.DataFrame([input_data])

        # Ensure model is valid
        if not hasattr(model, 'predict'):
            raise ValueError("Loaded object is not a valid model. Please check modelnew.pkl.")

        prediction = model.predict(df)[0]
        category = numeric_to_category.get(prediction, "Unknown")
        return jsonify({'status': 'success', 'prediction': int(prediction), 'category': category})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
