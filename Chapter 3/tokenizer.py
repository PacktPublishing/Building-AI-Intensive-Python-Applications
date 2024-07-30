import tiktoken

encoder = tiktoken.get_encoding("cl100k_base")
token_ids = encoder.encode("tiktoken is a popular tokenizer!")
print("Token IDs", token_ids)

tokens = [encoder.decode_single_token_bytes(t) for t in token_ids]
print("Tokens", tokens)
