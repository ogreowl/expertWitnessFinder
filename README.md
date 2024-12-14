<h2>BERT-based Semantic Search Engine for Expert Witnesses</h2>

<h3>Data Processing</h3>
We start off with a csv file of all the experts in the expertpages.com directory. The CSV has information about each experts, in their descriptions/page SEO / other variables. To consolidate all this information in an organized way, we used the GPT API to iteratively scan each Expert's information and create a summary of them. Then, we used a BERT model to create an embedding of each summary.

<h3>Back-end & Deployment</h3>
The back-end Python code takes in a user's query and creates an embedding of it with the same BERT model used for preprocessing. Then, it uses  cosine similarity to match the query with 10 experts, and outputs those experts and their page link through JSON. We use Dockerfile to build it the program as an image before pushing it to Google Cloud Run as a private API for the website to use.

<h3>Front-end</h3>
The front-end is a search bar that users can write their query into it which is then given to the API to find the best matches. It uses the JSON API input to display the top ten matches with a confidence score for each match, a short description of the expert, and a link to their profile.


You can try the system out yourself here: https://www.expertpages.com/ai-expert-finder (optimized for desktop). You can also read more detail about my process here: https://bobbybecker2001.com/expertpages-rag-system/
