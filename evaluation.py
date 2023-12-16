import os
import openai
import pandas as pd
import time

def main():
    """Main function to process queries."""

    df = pd.read_csv("queries.csv")
    df["LLM vs Human"] = ""

    for index, row in df.iterrows():
        print(f"Processing row {index}...")


        # read notion_1, notion_2,..,notion_8 from the dataframe into a set of strings

        notion_1 = row["notion_1"]
        notion_2 = row["notion_2"]
        notion_3 = row["notion_3"]
        notion_4 = row["notion_4"]
        notion_5 = row["notion_5"]
        notion_6 = row["notion_6"]
        notion_7 = row["notion_7"]
        notion_8 = row["notion_8"]

        # Filter out 'nan' and None values before creating the set
        human_assigned_keywords = set([notion for notion in [notion_1, notion_2, notion_3, notion_4, notion_5, notion_6, notion_7, notion_8] if notion is not None and str(notion).lower() != 'nan'])

        # remove nan from the set
        human_assigned_keywords.discard("")
        llm_assigned_keywords = set(row["Assigned Keywords"].split(", "))

        print(f"Human assigned keywords: {human_assigned_keywords}")
        print(f"LLM assigned keywords: {llm_assigned_keywords}")
        # check if the two sets are equal

        if human_assigned_keywords == llm_assigned_keywords:
            df.at[index, "LLM vs Human"] = "EQUAL"
        elif human_assigned_keywords.issubset(llm_assigned_keywords):
            df.at[index, "LLM vs Human"] = "LLM IS A SUPERSET"
        elif llm_assigned_keywords.issubset(human_assigned_keywords):
            df.at[index, "LLM vs Human"] = "HUMAN IS A SUPERSET"
        else:
            only_in_human = human_assigned_keywords.difference(llm_assigned_keywords)
            only_in_llm = llm_assigned_keywords.difference(human_assigned_keywords)
            df.at[index, "LLM vs Human"] = f"ONLY IN HUMAN: {only_in_human}, ONLY IN LLM: {only_in_llm}"

    # Save the dataframe with assigned labels back to a new CSV
    df.to_csv("queries.csv", index=False)



if __name__ == "__main__":
    main()