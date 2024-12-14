import pandas as pd
import numpy as np
import json
from huggingface_hub import InferenceClient
from openai import OpenAI

# Initialize the Hugging Face Inference API and OpenAI API
hf_client = InferenceClient(token="")
openai_client = OpenAI(api_key="")

# Load the CSV file with precomputed embeddings and modifiers
df = pd.read_csv('with_embeddings.csv')

# Convert the 'summary_embedding' column from string back to numpy array
df['summary_embedding'] = df['summary_embedding'].apply(lambda x: np.array(json.loads(x), dtype=np.float32))

# Function to summarize the user query using OpenAI GPT
def summarize_query(query):
    prompt = (f"The user has input the query: '{query}'. "
              "Please generate 5 short phrases, seperated by commas, to represent the query: ")

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    rephrased_query = response.choices[0].message.content.strip()
    return rephrased_query

# Function to get the query embedding using Hugging Face API
def get_query_embedding(query_summary, model="sentence-transformers/multi-qa-mpnet-base-dot-v1"):
    response = hf_client.feature_extraction(query_summary, model=model)
    return np.array(response, dtype=np.float32)

# Function to find top matches for the summarized query based on cosine similarity and modifier
def find_top_matches(query, df, top_n=10):
    # Summarize the query using OpenAI GPT
    summarized_query = summarize_query(query)
    print(f"Summarized Query: {summarized_query}")
    
    # Get the embedding of the summarized query
    query_embedding = get_query_embedding(summarized_query)
    
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

    # Return the top matches with boosted similarities
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

if __name__ == "__main__":
    query_sentence = input("Enter your query: ")

    top_matches = find_top_matches(query_sentence, df, top_n=10)

    print("\nTop 10 Matches:\n")
    for i, match in enumerate(top_matches):
        print(f"Rank {i + 1}:")
        print(f"Summary: {match['summary']}")
        print(f"Name: {match['first_name']} {match['last_name']}")
        print(f"Similarity Score: {match['similarity']:.4f}\n")