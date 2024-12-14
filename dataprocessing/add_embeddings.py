import pandas as pd
import numpy as np
from huggingface_hub import InferenceClient
import time

# Load the CSV file with summaries
df = pd.read_csv('most_recent.csv')

# Initialize the Hugging Face Inference API with a stronger model
client = InferenceClient(token="")

# Function to get embeddings for a batch of summaries using a stronger Hugging Face model
def get_batch_embeddings(summaries, model="sentence-transformers/all-mpnet-base-v2"):
    # Send all summaries in the batch as a single API call
    response = client.feature_extraction(summaries.tolist(), model=model)
    embeddings = [np.array(embedding, dtype=np.float32) for embedding in response]
    return embeddings

# Define batch size to 50
batch_size = 50

# List to store embeddings for the entire DataFrame
all_embeddings = [None] * len(df)

# Process summaries in batches
for i in range(0, len(df), batch_size):
    batch = df['display_summary'][i:i + batch_size]
    print(f"Processing batch {i // batch_size + 1}...")
    
    # Get embeddings for the current batch
    batch_embeddings = get_batch_embeddings(batch)
    
    # Assign the batch embeddings to the appropriate rows in the all_embeddings list
    all_embeddings[i:i + batch_size] = batch_embeddings

    # Optional: Save progress after each batch
    df['summary_embedding'] = [emb.tolist() if emb is not None else [] for emb in all_embeddings]
    df.to_csv('with_embeddings5.csv', index=False)

    # Sleep for 10 seconds after each batch to avoid hitting the rate limit
    time.sleep(2)

# Final save after all batches are processed
df['summary_embedding'] = [emb.tolist() if emb is not None else [] for emb in all_embeddings]
df.to_csv('with_embeddings5.csv', index=False)

print("Embeddings computed and saved in 'with_embeddings5.csv'.")