import streamlit as st
import pandas as pd
import openai

# Set up OpenAI API key
openai.api_key = st.secrets["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"]

# Load dataset
@st.cache
def load_data():
    # Replace 'your_dataset.csv' with the actual file name in your repository
    return pd.read_csv("BooksDataSet_project.csv")

df = load_data()

# Normalize columns for consistency
df['Genre'] = df['Genre'].str.lower()
df['Author'] = df['Author'].str.lower()
df['Book'] = df['Book'].str.lower()

# Chatbot functionality
def get_books_by_author(author_name):
    author_books = df[df['Author'] == author_name.lower()]
    count = len(author_books)
    if count > 0:
        return f"{author_name.title()} has written {count} book(s) in the dataset."
    else:
        return f"No books found for the author '{author_name.title()}'."

def get_similar_books(book_title):
    # Check if the book exists
    if book_title.lower() not in df['Book'].values:
        return f"The book '{book_title.title()}' is not found in the dataset."
    book_info = df[df['Book'] == book_title.lower()].iloc[0]
    genre = book_info['Genre']
    similar_books = df[df['Genre'] == genre]['Book'].tolist()
    similar_books.remove(book_title.lower())
    if similar_books:
        return f"Books similar to '{book_title.title()}' in the '{genre}' genre: {', '.join(similar_books[:10])}."
    else:
        return f"No similar books found in the '{genre}' genre."

def get_average_rating(book_title):
    book_info = df[df['Book'] == book_title.lower()]
    if len(book_info) > 0:
        avg_rating = book_info['Avg_Rating'].values[0]
        return f"The average rating of '{book_title.title()}' is {avg_rating}."
    else:
        return f"'{book_title.title()}' is not found in the dataset."

# Streamlit app interface
st.title("Book Recommendation and Query Chatbot")
st.write("Ask me about books, authors, genres, and ratings!")

# User query selection
query_type = st.selectbox(
    "What do you want to know?",
    [
        "Number of Books by an Author",
        "Similar Books of the Same Genre",
        "Average Rating for a Book",
    ],
)

if query_type == "Number of Books by an Author":
    author_name = st.text_input("Enter Author Name:")
    if st.button("Submit"):
        result = get_books_by_author(author_name)
        st.write(result)

elif query_type == "Similar Books of the Same Genre":
    book_title = st.text_input("Enter Book Title:")
    if st.button("Submit"):
        result = get_similar_books(book_title)
        st.write(result)

elif query_type == "Average Rating for a Book":
    book_title = st.text_input("Enter Book Title:")
    if st.button("Submit"):
        result = get_average_rating(book_title)
        st.write(result)