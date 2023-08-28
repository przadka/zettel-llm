# Zettel LLM User Manual

## Introduction
The **Zettel LLM** system is designed to label notes within a zettelkasten system using LLMs and vector embeddings. This guide will walk you through the setup and usage process. 


## Prerequisites
- Ubuntu Linux operating system.
- A terminal application (usually pre-installed on Ubuntu).

## Data Files Structure

### notions.csv

- **Location**: `documents/notions.csv`
- **Purpose**: This file contains the notions that the system will embed and use.
- **Expected Columns**:
  - `Notions`: Contains the textual content of the notion.

### train_data.csv

- **Location**: `documents/train_data.csv`
- **Purpose**: Contains the quotes, associated metadata, and notions.
- **Expected Columns**:
  - `author(s)`: The author(s) of the quote.
  - `title of the source`: Title of the source from where the quote is taken.
  - `type of the source`: The type or category of the source (e.g., book, article, etc.).
  - `quotation`: The actual quote text.
  - `notion_1` to `notion_8`: Notions associated with the quote. The system supports up to 8 notions per quote.

Ensure all required columns are present. Missing data should be represented as empty strings.

## Step-by-step Setup and Usage

### Step 1: Preparation

1. Open the terminal by pressing `Ctrl` + `Alt` + `T`.
2. Ensure `git` is installed with the following command:
   ```bash
   sudo apt update && sudo apt install git
   ```

### Step 2: Clone the Repository

1. Clone the project repository:
   ```bash
   git clone https://github.com/przadka/zettel-llm
   ```
2. Change your directory to the project folder:
   ```bash
   cd zettel-llm
   ```

### Step 3: Virtual Environment Setup

1. Install `pip` and `virtualenvwrapper`:
   ```bash
   sudo apt install python3-pip
   pip3 install virtualenv virtualenvwrapper
   ```
2. Add the following lines to your `~/.bashrc` to configure the virtual environment:
   ```bash
   export WORKON_HOME=$HOME/.virtualenvs
   export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
   source /usr/local/bin/virtualenvwrapper.sh
   ```
3. Reload your bashrc file:
   ```bash
   source ~/.bashrc
   ```
4. Create a virtual environment for Zettel LLM:
   ```bash
   mkvirtualenv zettel-llm
   ```
5. Activate the virtual environment:
   ```bash
   workon zettel-llm
   ```

### Step 4: Install Dependencies

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Step 5: Environment Variables Configuration

1. Add your OpenAI API key to your bash environment:
   ```bash
   echo 'export OPENAI_API_KEY="YOUR_API_KEY"' >> ~/.bashrc
   ```
   Replace `YOUR_API_KEY` with the API key you received.
   
2. Activate the virtual environment again:
   ```bash
   workon zettel-llm
   ```

### Step 6: Prepare Your Documents

1. Place your CSV documents inside the `documents` directory of the project. This directory is where the system looks for the data.

### Step 7: Initialize the Database

1. To prepare the database, run:
   ```bash
   python initialize_chroma_db.py
   ```

### Step 8: Query the System

1. To use the system and retrieve notions based on a specific query, use the following command:
   ```bash
   python main.py "Your Query Text Here"
   ```
   Replace `"Your Query Text Here"` with the text you want to search.

### Adjusting the Number of Notions Returned:

In the `main.py` file, there's a constant named `QUERY_RESULTS`. By default, it might be set to 60. You can change this number to increase or decrease the number of results returned.

1. Open `main.py` in a text editor:
   ```bash
   nano main.py
   ```
2. Locate the line with `QUERY_RESULTS = 60` and change `60` to your desired number.
3. Save and exit by pressing `Ctrl` + `X`, then press `Y` and `Enter`.

### Re-initializing ChromaDB:

If you need to re-initialize the Chroma database, you can delete the existing one by executing the following command:

```bash
$ rm -rf chroma.db
```

Remember that initializing a new database incurs a small cost. Always ensure you're aware of any associated expenses before performing this action.

### Closing Thoughts

That's it! Now you can query your system with specific texts, and it will return relevant notions from the database. Remember to activate the virtual environment (`workon zettel-llm`) every time you want to use the system.
