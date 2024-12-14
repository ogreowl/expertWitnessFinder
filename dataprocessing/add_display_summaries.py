import pandas as pd
from openai import OpenAI

# Set your API key here
client = OpenAI(api_key="")

def truncate_text(text, max_chars=2000):
    """Truncate the text to ensure it stays within the character limit."""
    if isinstance(text, str):
        return text[:max_chars] + '...' if len(text) > max_chars else text
    return ''  # Return an empty string if text is None or not a string

def generate_summary(row):
    # Truncate the "about_me" field to reduce character count
    text = truncate_text(row['about_me'])
    
    # Extract first and last names from the row
    first_name = row['first_name']
    last_name = row['last_name']

    # Construct the prompt using the first and last names
    prompt = (f"Here is a description of {first_name} {last_name}: {text}\n"
              f"Please generate concise, detailed 2-sentence summary of what the expert witness {first_name} {last_name} does, "
              "including their full name in the summary:")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    summary = response.choices[0].message.content.strip()
    return summary

def process_csv_in_parts(csv_file, output_file, chunk_size=50):
    """Process the CSV file in chunks and generate summaries."""
    # Load the CSV file in chunks to avoid memory overload
    chunk_iter = pd.read_csv(csv_file, chunksize=chunk_size)

    # List to store processed chunks
    chunk_list = []

    for chunk in chunk_iter:
        # Generate summaries for the current chunk
        chunk['display_summary'] = chunk.apply(generate_summary, axis=1)

        # Append processed chunk to the list
        chunk_list.append(chunk)

    # Concatenate all chunks together into one DataFrame
    result_df = pd.concat(chunk_list, ignore_index=True)

    # Save the DataFrame with the new 'Summary' column to a new CSV
    result_df.to_csv(output_file, index=False)

    print(f"Summaries generated and saved in '{output_file}'.")

if __name__ == "__main__":
    # Process the CSV in chunks of 50 rows at a time
    process_csv_in_parts('experts_with_summary.csv', 'experts_with_display_summaries.csv', chunk_size=50)