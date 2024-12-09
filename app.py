import streamlit as st
import pandas as pd
import openai

# Load dataset
@st.cache
def load_data():
    return pd.read_csv("BooksDataSet_project.csv")

df = load_data()
df['Genre'] = df['Genre'].str.lower()
df['Author'] = df['Author'].str.lower()
df['Book'] = df['Book'].str.lower()

# OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to process user queries
def process_query(query):
    query = query.lower()
    
    # Check for author-related queries
    if "books by" in query or "author" in query:
        author_name = query.split("by")[-1].strip()
        author_books = df[df['Author'] == author_name]
        count = len(author_books)
        if count > 0:
            return f"{author_name.title()} has written {count} book(s): {', '.join(author_books['Book'].tolist())}."
        else:
            return f"No books found for the author '{author_name.title()}'."
    
    # Check for similar books
    elif "similar books" in query or "same genre" in query:
        book_title = query.split("books like")[-1].strip()
        if book_title in df['Book'].values:
            genre = df[df['Book'] == book_title].iloc[0]['Genre']
            similar_books = df[df['Genre'] == genre]['Book'].tolist()
            similar_books.remove(book_title)
            if similar_books:
                return f"Books similar to '{book_title.title()}': {', '.join(similar_books[:10])}."
            else:
                return f"No similar books found for '{book_title.title()}'."
        else:
            return f"The book '{book_title.title()}' is not found in the dataset."
    
    # Check for book ratings
    elif "rating of" in query:
        book_title = query.split("rating of")[-1].strip()
        book_info = df[df['Book'] == book_title]
        if not book_info.empty:
            avg_rating = book_info['Avg_Rating'].values[0]
            return f"The average rating of '{book_title.title()}' is {avg_rating}."
        else:
            return f"'{book_title.title()}' is not found in the dataset."
    
    # Default response for unrecognized queries
    else:
        return "I’m sorry, I couldn’t understand your query. Please try asking about books by an author, similar books, or ratings."

# Streamlit app interface
st.title("Book Recommendation and Query Chatbot")
st.write("Ask me about books, authors, genres, and ratings!")

# User input
user_query = st.text_input("Type your question here:")

# Process query on submit
if st.button("Submit"):
    if user_query:
        response = process_query(user_query)
        st.write(response)
    else:
        st.write("Please type a question!")
