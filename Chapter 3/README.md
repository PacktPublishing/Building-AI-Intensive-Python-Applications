# Building AI Intensive Python Applications

## Chapter 3 - Large Language Models

The Python script in this directory demonstrates the use of the `tiktoken` tokenizer library used with OpenAI language models.

First you need to install the `tiktoken` package:

```
pip install tiktoken
```

Then run the Python script from the command line:

```
python tokenizer.py
```

The script tokenizes the sentence "tiktoken is a popular tokenizer!" and returns both the token IDs and the actual tokens:

```
Token IDs [83, 1609, 5963, 374, 264, 5526, 47058, 0]
Tokens [b't', b'ik', b'token', b' is', b' a', b' popular', b' tokenizer', b'!']
```

You'll notice that some words are split into several tokens (such as "tiktoken"), while other words are their own token, such as " popular". Also note that `tiktoken` sometimes includes leading whitespace as part of the token.
