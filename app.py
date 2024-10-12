from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)


# TODO: Fetch dataset, initialize vectorizer and LSA here

# Fetch dataset
newsgroups = fetch_20newsgroups(subset='all')

# Initialize vectorizer
stop_words = 'english'
vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=5000)

# Fit and transform the documents
X = vectorizer.fit_transform(newsgroups.data)

# Initialize and fit LSA
lsa = TruncatedSVD(n_components=100, random_state=42)
X_lsa = lsa.fit_transform(X)


def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    # TODO: Implement search engine here
    # return documents, similarities, indices
    
    # Preprocess the query
    query_vector = vectorizer.transform([query])
    
    # Transform query to LSA space
    query_lsa = lsa.transform(query_vector)
    
    # Calculate cosine similarities
    similarities = cosine_similarity(query_lsa, X_lsa).flatten()
    
    # Get top 5 indices
    top_indices = similarities.argsort()[-5:][::-1]
    
    # Get corresponding documents and similarities
    documents = [newsgroups.data[i] for i in top_indices]
    top_similarities = similarities[top_indices]
    
    return documents, top_similarities.tolist(), top_indices.tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    documents, similarities, indices = search_engine(query)
    return jsonify({'documents': documents, 'similarities': similarities, 'indices': indices}) 

if __name__ == '__main__':
    app.run(debug=True)
