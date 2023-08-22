# Zettel LLM

**Zettel LLM** leverage LLMs and vector embeddings to automatically assign labels to notes within a zettelkasten system. For a more detailed guide, check out the [Simple Manual](SIMPLE_MANUAL.md).

## 🛠️ Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/przadka/zettel-llm
   ```

2. **Navigate to the Project Directory**
   ```bash
   cd zettel-llm
   ```

3. **Activate the Virtual Environment**
   *(Make sure you have `virtualenvwrapper` installed)*
   ```bash
   workon zettel-llm
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Prepare Your Documents**:
   - Place your documents in the `documents` directory.
   - Currently, the system assumes documents are in CSV format.

## 🚀 Usage

### 1. Initialize ChromaDB

Run the `initialize_chroma_db.py` script. This will ensure the presence of the 'zettelkasten' collection in the specified database and begin the querying process.

```bash
python initialize_chroma_db.py
```

### 2. Query the Database

Execute the `main.py` script to search for specific texts within the 'zettelkasten' collection.

```bash
python main.py
```

## 🌍 Environment Variables

Before using the scripts, configure the necessary environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key, required for the embedding function.

You can either export this variable directly in your shell or use an `.env` file.

## 📜 License

This project is open-source and licensed under the MIT License.
