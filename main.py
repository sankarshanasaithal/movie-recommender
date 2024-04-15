import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the recommender model and movie dataset
similarity = pickle.load(open('similarity.pkl', 'rb')) 
dataset = pickle.load(open('movie_list.pkl', 'rb'))

# Recommend 5 similar movies to the entered movie
def recommend(movie):
    # Find the index of the movie in the dataset
    index = next((i for i, d in enumerate(dataset) if d['Name'].lower() == movie), None)
    if index is None:
        return [], []  # when movie is not found
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        name = dataset[i[0]]['Name']
        image = dataset[i[0]]['Image']
        recommended_movie_posters.append(image)
        recommended_movie_names.append(name)
    return recommended_movie_names, recommended_movie_posters

# Renders the name and image (link) of the similar movies to the front end
@app.route('/', methods=['GET', 'POST'])
def index():
    movie_name = ""
    search_performed = False
    names, posters = [], []
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        search_performed = True
        if movie_name=="" or movie_name.replace(" ","")=="":
            search_performed = False
        for data in dataset:
            if data['Name'].lower() == movie_name.strip().lower():
                names, posters = recommend(movie_name.strip().lower())
                break
    return render_template('index.html', name=movie_name.title(), movie_names=names, image_links=posters, search_performed=search_performed)

# Renders the movie suggestions to the frontend as the user types
@app.route('/suggest', methods=['POST'])
def suggest():
    if request.method == 'POST':
        input_text = request.form.get('input_text', '').lower()
        suggestions = []
        count = 0
        for data in dataset:
            if count >= 5: 
                break
            if data['Name'].lower().startswith(input_text):
                suggestions.append(data['Name'])
                count += 1
        suggestions.sort()
        if len(suggestions)!=0:
            return '\n'.join(suggestions)
        else:
            return ''
    else:
        return 'Method Not Allowed', 405 

if __name__ == '__main__':
    app.run(debug=True)