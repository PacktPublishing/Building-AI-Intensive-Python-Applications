# Install the latest version of these libraries
# pip3 install transformers tensorflow

# Import the pipeline function
from transformers import pipeline

# Initialize the sentiment analysis pipeline
analyse_sentiment = pipeline("sentiment-analysis")
analyse_sentiment("The weather is very nice today.")

# You can pass multiple inputs, like so:
analyse_sentiment(["The weather is very nice today.", "I don't like it when it rains in winter."])

# Generate text
generator = pipeline("text-generation")
generator("I love AI, it has")

# Specify a model name, unless you want the default
generator = pipeline("text-generation", model="distilgpt2")
generator("I love AI, it has", max_length=25, num_return_sequences=2)