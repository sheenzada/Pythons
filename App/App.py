from flask import Flask, render_template

app = Flask(__name__)

# Sample movie data
movies = [
    {
        "id": 1,
        "title": "Inception",
        "year": 2010,
        "description": "A thief who steals corporate secrets through dream-sharing technology.",
        "rating": 8.8
    },
    {
        "id": 2,
        "title": "Interstellar",
        "year": 2014,
        "description": "A team travels through a wormhole in space to ensure humanity's survival.",
        "rating": 8.6
    },
]

@app.route("/")
def home():
    return render_template("index.html", movies=movies)

@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    movie = next((m for m in movies if m["id"] == movie_id), None)
    return render_template("movie.html", movie=movie)

if __name__ == "__main__":
    app.run(debug=True)