from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from flask_cors import CORS
from huggingface_hub import InferenceClient
import json

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "https://www.expertpages.com"}})

# Load the CSV file with precomputed embeddings and modifiers
df = pd.read_csv('the_data.csv')

# Convert the 'summary_embedding' column from string back to numpy array
df['summary_embedding'] = df['summary_embedding'].apply(lambda x: np.array(json.loads(x), dtype=np.float32))

# Initialize the Hugging Face Inference API
client = InferenceClient(token="")

# Function to get the query embedding using Hugging Face API
def get_query_embedding(query, model="sentence-transformers/all-mpnet-base-v2"):
    response = client.feature_extraction(query, model=model)
    return np.array(response, dtype=np.float32)

# Function to find top matches for the query
def find_top_matches(query, df, top_n=10):
    query_embedding = get_query_embedding(query)
    
    # Normalize query embedding
    query_embedding = query_embedding / np.linalg.norm(query_embedding)
    
    # Stack and normalize the precomputed embeddings
    summary_embeddings = np.vstack(df['summary_embedding'].values)
    summary_embeddings = summary_embeddings / np.linalg.norm(summary_embeddings, axis=1, keepdims=True)

    # Compute cosine similarity between query and precomputed embeddings
    similarities = np.dot(summary_embeddings, query_embedding)

    # Apply the modifier to boost the similarity score
    similarities *= df['modifier'].values

    # Sort and find the top_n matches
    top_indices = similarities.argsort()[-top_n:][::-1]

    # Return the top matches
    top_matches = [
        {
            "summary": df.iloc[i]['display_summary'],
            "full_filename": df.iloc[i]["full_filename"],
            "similarity": float(similarities[i]),
            "first_name": df.iloc[i]['first_name'],
            "last_name": df.iloc[i]['last_name']
        }
        for i in top_indices
    ]
    return top_matches

# Route for sending queries
@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query_sentence = data.get('query')

    if not query_sentence:
        return jsonify({"error": "Query is required"}), 400

    top_matches = find_top_matches(query_sentence, df, top_n=10)

    response = {
        "query": query_sentence,
        "matches": [
            {
                "rank": i + 1,
                "summary": match["summary"],
                "full_filename": match["full_filename"],
                "similarity_score": match["similarity"],
                "first_name": match["first_name"],
                "last_name": match["last_name"]
            }
            for i, match in enumerate(top_matches)
        ]
    }

    return jsonify(response)

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)