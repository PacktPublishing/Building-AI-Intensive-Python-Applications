# Setting up Python Environment

This README provides instructions on how to set up the Python environment required to run the `vector_search_ai_application.ipynb` or similarly `chunking_strategies.ipynb` or `advanced_rag_example.ipynb` notebook.

## Prerequisites

Before proceeding, make sure you have the following installed on your system:

- Python 3.x
- Jupyter Notebook

## Installation

1. Clone the repository to your local machine:

    ```
    git clone git@github.com:PacktPublishing/Building-AI-Intensive-Python-Applications.git
    ```

2. Navigate to the project directory:

    ```
    cd ./Building-AI-Intensive-Python-Applications/Chapter\ 8
    ```

3. Create a virtual environment:

    ```
    python3 -m venv env
    ```

4. Activate the virtual environment:

    - For Windows:

      ```
      .\env\Scripts\activate
      ```

    - For macOS/Linux:

      ```
      source env/bin/activate
      ```

5. Install the required dependencies:
    If you installed the dependencies from here you can ignore the pip install commands in the notebook

    ```
    pip install -r requirements.txt
    ```

## Running the Notebook

1. Launch Jupyter Notebook:

    ```
    jupyter notebook
    ```
2. Update `.env` file with your own OpenAI API key and MongoDB Atlas connection string.

3. In your browser, navigate to the notebook file `vector_search_ai_application.ipynb` or similarly `chunking_strategies.ipynb` or `advanced_rag_example.py`.

4. Open the notebook and run the cells sequentially to execute the AI application.

That's it! You have successfully set up the Python environment and can now run the `vector_search_ai_application.ipynb` notebook.
