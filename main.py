"""
This is the main entry point for the WeatherBot application.
It initializes the Streamlit interface and handles user interactions.
"""

import streamlit as st
from chat_agent import ChatAgent
from entity_recognizer import EntityRecognizer

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory() 

# Initialize ChatAgent and EntityRecognizer
chat_agent = ChatAgent()
entity_recognizer = EntityRecognizer()

st.title("WeatherBot")
st.write("Ask about the weather in any location!")

# Display chat messages from the session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user queries
if user_query := st.chat_input(placeholder="Ask me anything about the weather!"):
    # Display the user's message
    st.chat_message("user").markdown(user_query)

    # Add user message to the session's messages
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Check for location entities
    if entity_recognizer.location_entity_detected(user_query):
        st.session_state.chat_history.clear()
    else:
        location = entity_recognizer.find_location(st.session_state.chat_history.messages)
        if location:
            st.session_state.chat_history.clear()
            st.session_state.chat_history.add_user_message(location)

    st.session_state.chat_history.add_user_message(user_query)

    # Generate and display the response
    response = chat_agent.respond(user_query)
    assistant = st.chat_message("assistant")
    assistant.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
