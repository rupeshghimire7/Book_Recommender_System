from flask import Flask, render_template, request
import pickle
import re
import numpy as np

df = pickle.load(open('popular_books.pkl','rb'))

books = pickle.load(open('books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',book_name = list(df['Book-Title'].values),author=list(df['Book-Author'].values),image=list(df['Image-URL-L'].values),year=list(df['Year-Of-Publication'].values),rating_count=list(df['Rating_Count'].values),avg_rating=list(df['Avg_Ratings'].values)
                           )

def find_best_match(input_book_name):
    best_match = None
    best_match_score = 0

    input_words = set(re.findall(r'\b\w+\b', input_book_name.lower()))

    for book_name in pt.index:
        book_words = set(re.findall(r'\b\w+\b', book_name.lower()))

        # Calculate the similarity score by finding the intersection of words
        match_score = len(input_words.intersection(book_words))

        if match_score > best_match_score:
            best_match = book_name
            best_match_score = match_score

    return best_match


def recommend(book_name):
    book_data=[]
    assert type(book_name)==str
    if book_name in pt.index:
        index = np.where(pt.index==book_name)[0][0]
        similar_books = sorted(list(enumerate(similarity_score[index])),key=lambda x: x[1],reverse=True)[0:6]
        
        for i in similar_books:
            item=[]
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))   

            book_data.append(item) 
        return book_data
    else:
        print("Your provided Book Name didn't match. Searching for best match:")
        book = find_best_match(book_name)
        print("Searching for\t:", book)
        print("")
        if book != None:
            recommend(book)
        else:
            print("Try for another book")

@app.route('/recommender',methods=['post'])
def recommender():
    input_book_name = request.form.get('input_book_name')
    result_books = recommend(input_book_name) 
    print(result_books)
    return render_template('recommender.html',result_books=result_books)


@app.template_filter('floor')
def floor(x:float):
    return int(x)

@app.template_filter('exclude_first')
def floor(book_list):
    return book_list[:][1:]




if __name__ == "__main__":
    app.run(debug=True)