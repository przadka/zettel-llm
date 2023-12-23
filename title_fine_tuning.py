import pandas as pd
import json
import re



DEFAULT_SYSTEM_PROMPT = 'Zet is a helpful librarian who assigns titles to new quotes.'

def create_dataset(question, answer):
    return {
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
    }

if __name__ == "__main__":
    df = pd.read_csv('documents/train_data.csv')

    df["Question"] = ""
    df["Answer"] = ""

    for index, row in df.iterrows():
        author = row["author(s)"]
        source = row["title of the source"]
        quote = row["quotation"]
        title = row["title of the note"]

        question = f'''Here is a new note you need to assign title to:

===
Author: {author}
Source: "{source}"
Quote: "{quote}"
===

Remember, the assigned title should have the following form: first the author’s last name, then a colon, and then a sentence that captures the idea expressed in the quote. Only the first word of this phrase and proper nouns should be capitalized. The entire title should be no longer than 30 words.'''

        answer = title

        # add new column to store question and answer

        df.loc[index, 'Question'] = question
        df.loc[index, 'Answer'] = answer

    # sample 500 rows from the dataframe
        
    df = df.sample(n=500, random_state=1)

    # save the dataframe to a new csv file, 150 fine tuning examples

    #keep only columns: author(s), title of the source, quotation, title of the note, Question, Answer

    df = df[['author(s)', 'title of the source', 'quotation', 'title of the note', 'Question', 'Answer']]

    df.to_csv('documents/fine_tuning.csv', index=False)

