from flask import Flask, render_template
import pickle

df = pickle.load(open('popular_books.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',book_name = list(df['Book-Title'].values),author=list(df['Book-Author'].values),image=list(df['Image-URL-L'].values),year=list(df['Year-Of-Publication'].values),rating_count=list(df['Rating_Count'].values),avg_rating=list(df['Avg_Ratings'].values)
                           )

@app.template_filter('floor')
def floor(x:float):
    return int(x)




if __name__ == "__main__":
    app.run(debug=True)