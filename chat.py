import streamlit as st
import time
from graph import invoke_user_question

def display_sources_in_expander(sources, content_container):
    with content_container.expander("Quellen"):
        for i, (doc, similarity_score) in enumerate(sources):
            with st.popover(f"Datei: {i + 1}: {doc.metadata.get('source', 'Unknown File')} - Seite: {doc.metadata.get('page_label', 'Unknown Page')} - Score: {similarity_score:.2f}"):
                st.markdown(doc.page_content)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting!"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "source" in message:
            sources_container = st.empty()
            display_sources_in_expander(message["source"], sources_container)

# Accept user input
if prompt := st.chat_input("Ich hab da mal ne Frage..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.empty()
        response.markdown("Thinking...")
        #assistant_response = invoke_user_question(prompt)
        graph_response = invoke_user_question(prompt)
        
        response.markdown(graph_response["answer"])  
        
        message = {"role": "assistant", "content": graph_response["answer"], "source": graph_response["context"]}
        
        sources_container = st.empty()
        display_sources_in_expander(message["source"], sources_container)
                    
        # Add assistant response to chat history
        st.session_state.messages.append(message)
        
        
    
