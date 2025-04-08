import os
import time

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from graph import invoke_user_question


def display_sources_in_container(sources, content_container):
    with content_container.expander("Quellen"):
        for i, (doc, similarity_score) in enumerate(sources):
            with st.popover(
                f"Datei: {i + 1}: {doc.metadata.get('source', 'Unknown File')} - Seite: {doc.metadata.get('page_label', 'Unknown Page')} - Score: {similarity_score:.2f}"
            ):
                st.markdown(doc.page_content)
            pdf_file = doc.metadata.get("source", "").split("\\")[-1]
            print(f"PDF file check: {pdf_file}")
            if pdf_file in st.session_state.pdfs:
                if st.button(
                    f"View PDF: {pdf_file}",
                    key=f"pdf_btn_{message['content'][:10]}_{i}",
                ):
                    pdf_viewer(
                        st.session_state.pdfs[pdf_file],
                        width="90%",
                        height=800,
                        scroll_to_page=int(doc.metadata.get("page_label")),
                    )
                    print(doc.metadata.get("page"))


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Let's start chatting!"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "source" in message:
            sources_container = st.empty()
            display_sources_in_container(message["source"], sources_container)

if "pdfs" not in st.session_state:
    # Initialize PDF storage in session state
    pdf_folder = "./pdf"
    st.session_state.pdfs = {}

    # Check if the folder exists
    if os.path.exists(pdf_folder):
        # Load all PDFs from the folder
        for file in os.listdir(pdf_folder):
            if file.endswith(".pdf"):
                file_path = os.path.join(pdf_folder, file)
                with open(file_path, "rb") as f:
                    st.session_state.pdfs[file] = f.read()
                    print(f"Loaded PDF: {file}")
        if not st.session_state.pdfs:
            st.info("No PDF files found in the ./pdf folder.")
    else:
        st.warning(f"PDF folder '{pdf_folder}' does not exist.")

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
        with st.spinner("Thinking..."):
            # assistant_response = invoke_user_question(prompt)
            graph_response = invoke_user_question(prompt)

            response.markdown(graph_response["answer"])

            message = {
                "role": "assistant",
                "content": graph_response["answer"],
                "source": graph_response["context"],
            }

            sources_container = st.empty()
            display_sources_in_container(message["source"], sources_container)

        # Add assistant response to chat history
        st.session_state.messages.append(message)
