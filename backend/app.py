from flask import Flask,flash, request, jsonify, render_template, redirect, url_for, session
import pickle
import pandas as pd

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = '12345'


USERNAME = "shrusti@gmail.com"
PASSWORD = "12345"

# Load ML model
MODEL_PATH = r'C:\sihcareer\Career-Recommendation-System-using-ML\backend\modelnew.pkl'
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

feature_names = [
    'Drawing', 'Dancing', 'Singing', 'Sports', 'Video Game', 'Acting', 'Travelling',
    'Gardening', 'Animals', 'Photography', 'Teaching', 'Exercise', 'Coding',
    'Electricity Components', 'Mechanic Parts', 'Computer Parts', 'Researching',
    'Architecture', 'Historic Collection', 'Botany', 'Zoology', 'Physics',
    'Accounting', 'Economics', 'Sociology', 'Geography', 'Psycology', 'History',
    'Science', 'Bussiness Education', 'Chemistry', 'Mathematics', 'Biology',
    'Makeup', 'Designing', 'Content writing', 'Crafting', 'Literature', 'Reading',
    'Cartooning', 'Debating', 'Asrtology', 'Hindi', 'French', 'English', 'Urdu',
    'Other Language', 'Solving Puzzles', 'Gymnastics', 'Yoga', 'Engeeniering',
    'Doctor', 'Pharmisist', 'Cycling', 'Knitting', 'Director', 'Journalism',
    'Bussiness', 'Listening Music'
]

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

# ✅ Career-based resource links
career_resources = {
    'Animation, Graphics and Multimedia': [
        'https://www.skillshare.com/browse/animation',
        'https://www.udemy.com/topic/graphic-design/',
        'https://motiondesign.school/',
        'https://www.schoolofmotion.com/'
    ],
    'B.Arch- Bachelor of Architecture': [
        'https://www.archdaily.com/',
        'https://www.udemy.com/topic/architecture/',
        'https://www.coursera.org/courses?query=architecture',
        'https://www.architecturaldigest.com/'
    ],
    'B.Com- Bachelor of Commerce': [
        'https://www.edx.org/learn/accounting',
        'https://www.investopedia.com/',
        'https://corporatefinanceinstitute.com/',
        'https://www.coursera.org/browse/business/finance'
    ],
    'B.Ed.': [
        'https://www.edutopia.org/',
        'https://www.coursera.org/learn/foundations-of-teaching-learning',
        'https://teachthought.com/',
        'https://www.futurelearn.com/subjects/teaching-courses'
    ],
    'B.Sc- Applied Geology': [
        'https://www.geologyin.com/',
        'https://www.usgs.gov/',
        'https://www.coursera.org/learn/geology',
        'https://www.nature.com/subjects/geology'
    ],
    'B.Sc- Nursing': [
        'https://www.nursingtimes.net/',
        'https://www.khanacademy.org/science/health-and-medicine',
        'https://www.nurse.org/',
        'https://www.verywellhealth.com/nursing-basics-5188361'
    ],
    'B.Sc. Chemistry': [
        'https://www.chemguide.co.uk/',
        'https://pubs.acs.org/',
        'https://www.khanacademy.org/science/chemistry',
        'https://www.masterorganicchemistry.com/'
    ],
    'B.Sc. Mathematics': [
        'https://brilliant.org/',
        'https://www.khanacademy.org/math',
        'https://mathworld.wolfram.com/',
        'https://www.youtube.com/user/numberphile'
    ],
    'B.Sc.- Information Technology': [
        'https://www.geeksforgeeks.org/',
        'https://www.coursera.org/browse/information-technology',
        'https://www.edx.org/learn/information-technology',
        'https://www.freecodecamp.org/'
    ],
    'B.Sc.- Physics': [
        'https://www.physicsclassroom.com/',
        'https://www.khanacademy.org/science/physics',
        'https://phys.org/physics-news/',
        'https://www.feynmanlectures.caltech.edu/'
    ],
    'B.Tech.-Civil Engineering': [
        'https://theconstructor.org/',
        'https://www.engineeringcivil.com/',
        'https://www.coursera.org/courses?query=civil%20engineering',
        'https://nptel.ac.in/courses/105'
    ],
    'B.Tech.-Computer Science and Engineering': [
        'https://www.geeksforgeeks.org/',
        'https://www.freecodecamp.org/',
        'https://www.udemy.com/topic/computer-science/',
        'https://cs50.harvard.edu/x/'
    ],
    'B.Tech.-Electrical and Electronics Engineering': [
        'https://www.electronics-tutorials.ws/',
        'https://circuitdigest.com/',
        'https://www.allaboutcircuits.com/',
        'https://nptel.ac.in/courses/108'
    ],
    'B.Tech.-Electronics and Communication Engineering': [
        'https://www.electronicsforu.com/',
        'https://www.tutorialspoint.com/electronics_and_communication_engineering/',
        'https://www.electronics-notes.com/',
        'https://nptel.ac.in/courses/117'
    ],
    'B.Tech.-Mechanical Engineering': [
        'https://www.mechanicalc.com/',
        'https://www.engineeringclicks.com/',
        'https://nptel.ac.in/courses/112',
        'https://www.coursera.org/courses?query=mechanical%20engineering'
    ],
    'BA in Economics': [
        'https://www.economist.com/',
        'https://www.khanacademy.org/economics-finance-domain',
        'https://www.investopedia.com/economics-4689748',
        'https://www.coursera.org/courses?query=economics'
    ],
    'BA in English': [
        'https://www.litcharts.com/',
        'https://www.britannica.com/',
        'https://www.poetryfoundation.org/',
        'https://owl.purdue.edu/'
    ],
    'BA in Hindi': [
        'https://www.typingbaba.com/',
        'https://www.typingkeyboards.com/hindi/',
        'https://www.typingguru.in/',
        'https://hindipathshala.com/'
    ],
    'BA in History': [
        'https://www.history.com/',
        'https://www.khanacademy.org/humanities/world-history',
        'https://www.britannica.com/topic/history',
        'https://www.jstor.org/'
    ],
    'BBA- Bachelor of Business Administration': [
        'https://www.investopedia.com/',
        'https://www.edx.org/learn/business-administration',
        'https://www.coursera.org/browse/business',
        'https://hbr.org/'
    ],
    'BBS- Bachelor of Business Studies': [
        'https://corporatefinanceinstitute.com/',
        'https://www.udemy.com/topic/business-strategy/',
        'https://www.coursera.org/browse/business',
        'https://www.open.edu/openlearn/money-business'
    ],
    'BCA- Bachelor of Computer Applications': [
        'https://www.geeksforgeeks.org/bca-full-form/',
        'https://www.javatpoint.com/',
        'https://www.programiz.com/',
        'https://www.tutorialspoint.com/'
    ],
    'BDS- Bachelor of Dental Surgery': [
        'https://www.ada.org/',
        'https://www.dentalcare.com/',
        'https://www.osmosis.org/',
        'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6280614/'
    ],
    'BEM- Bachelor of Event Management': [
        'https://www.eventmarketer.com/',
        'https://www.eventbrite.com/blog/',
        'https://www.socialtables.com/blog/',
        'https://whova.com/blog/'
    ],
    'BFD- Bachelor of Fashion Designing': [
        'https://www.vogue.com/',
        'https://www.businessoffashion.com/',
        'https://www.udemy.com/topic/fashion-design/',
        'https://www.skillshare.com/browse/fashion-design'
    ],
    'BJMC- Bachelor of Journalism and Mass Communication': [
        'https://www.poynter.org/',
        'https://ijnet.org/en',
        'https://journalismcourses.org/',
        'https://www.coursera.org/learn/journalism'
    ],
    'BPharma- Bachelor of Pharmacy': [
        'https://www.pharmacytimes.com/',
        'https://www.pharmaguideline.com/',
        'https://www.pharmacist.com/',
        'https://www.coursera.org/learn/drug-commercialization'
    ],
    'BTTM- Bachelor of Travel and Tourism Management': [
        'https://skift.com/',
        'https://www.tourism-review.com/',
        'https://www.coursera.org/learn/travel-business',
        'https://www.ustravel.org/'
    ],
    'BVA- Bachelor of Visual Arts': [
        'https://www.skillshare.com/browse/visual-arts',
        'https://www.udemy.com/topic/visual-arts/',
        'https://www.theartofeducation.edu/',
        'https://mymodernmet.com/'
    ],
    'CA- Chartered Accountancy': [
        'https://www.icai.org/',
        'https://cleartax.in/',
        'https://www.edx.org/course/financial-accounting',
        'https://www.wallstreetmojo.com/'
    ],
    'CS- Company Secretary': [
        'https://www.icsi.edu/',
        'https://www.indiaeducation.net/careercenter/law/companysecretary/',
        'https://taxguru.in/',
        'https://www.toppr.com/guides/commerce/ca-cs-cma/cs-career-as-a-company-secretary/'
    ],
    'Civil Services': [
        'https://www.insightsonindia.com/',
        'https://iasbaba.com/',
        'https://www.clearias.com/',
        'https://upscpathshala.com/'
    ],
    'Diploma in Dramatic Arts': [
        'https://www.nsd.gov.in/',
        'https://www.backstage.com/',
        'https://www.udemy.com/topic/acting/',
        'https://www.skillshare.com/browse/acting'
    ],
    'Integrated Law Course- BA + LL.B': [
        'https://blog.ipleaders.in/',
        'https://www.legalbites.in/',
        'https://www.lawctopus.com/',
        'https://www.coursera.org/learn/international-law'
    ],
    'MBBS': [
        'https://www.amboss.com/',
        'https://www.medicowesome.com/',
        'https://www.khanacademy.org/science/health-and-medicine',
        'https://www.osmosis.org/'
    ]
}



@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('email')
    password = request.form.get('password')
    if username == USERNAME and password == PASSWORD:
        session['user'] = username
        return redirect(url_for('dashboard'))
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'})

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html')

@app.route('/user-details', methods=['GET', 'POST'])
def user_details():
    if 'user' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')

        # Optionally save or process the data

        flash("Submitted successfully!", "success")
        return redirect(url_for('user_details'))

    return render_template('userdetails.html')

@app.route('/career-test')
def career_test():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        input_data = {feature: float(data.get(feature, 0)) for feature in feature_names}
        df = pd.DataFrame([input_data])

        prediction = model.predict(df)[0]
        category = numeric_to_category.get(prediction, "Unknown")
        session['career_result'] = category

        return jsonify({'status': 'success', 'prediction': int(prediction), 'category': category})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/personality-profile')
def personality_profile():
    if 'user' not in session:
        return redirect(url_for('home'))
    career_result = session.get('career_result', 'No result available')
    return render_template('personality_profile.html', result=career_result)

@app.route('/resources')
def resources():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    career = session.get('career_result', 'Unknown')
    links = career_resources.get(career, None)
    
    if not links:
        links = ['No resources available for this career. Please check back later.']

    return render_template('resources.html', career=career, resources=links)

@app.route('/feedback')
def feedback():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('feedback.html')

@app.route('/feedback', methods=['POST'])
def handle_feedback():
    if 'user' not in session:
        return redirect(url_for('home'))

    name = request.form.get('name')
    email = request.form.get('email')
    comment = request.form.get('comment')
    rating = request.form.get('rating')
    recommend = request.form.get('recommend')

    print("Feedback received:", name, email, rating, recommend, comment)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
