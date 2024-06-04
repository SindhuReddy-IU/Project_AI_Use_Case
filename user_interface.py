"""
The UserInterface class handles user interactions for the WeatherBot application.
"""

import streamlit as st
from chat_agent import ChatAgent
from entity_recognizer import EntityRecognizer

class UserInterface:
    """
    Manages the user interface for interacting with the WeatherBot.
    """

    def __init__(self):
        """
        Initializes the UserInterface with a ChatAgent and an EntityRecognizer.
        """
        self.__chat_agent = ChatAgent()
        self.__entity_recognizer = EntityRecognizer()

    def display(self):
        """
        Renders the chat interface and handles user input.
        """
        st.title("WeatherBot")
        st.write("Ask about the weather in any location!")

        # Display existing chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Handle user input
        if user_query := st.chat_input(placeholder="Ask me anything about the weather!"):
            st.chat_message("user").markdown(user_query)
            st.session_state.messages.append({"role": "user", "content": user_query})

            if self.__entity_recognizer.location_entity_detected(user_query):
                st.session_state.chat_history.clear()
            else:
                location = self.__entity_recognizer.find_location(st.session_state.chat_history.messages)
                if location:
                    st.session_state.chat_history.clear()
                    st.session_state.chat_history.add_user_message(location)

            st.session_state.chat_history.add_user_message(user_query)
            response = self.__chat_agent.respond(user_query)
            assistant = st.chat_message("assistant")
            assistant.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Initialize and display the user interface
ui = UserInterface()
ui.display()
