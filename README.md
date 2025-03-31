# Setup Instructions

## Prerequisites
1. Install [Docker](https://www.docker.com/).
2. Install [uv](https://docs.astral.sh/uv/) by following its installation guide.

## Steps to Set Up
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Sync the project using [uv](https://docs.astral.sh/uv/):
   ```bash
   uv sync
   ```

3. Download and run [Qdrant](https://qdrant.tech/) using [Docker](https://www.docker.com/):
   ```bash
   docker run -d -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```

4. Download and install [Ollama](https://ollama.ai/) and pull the required models:
     ```bash
     ollama pull jina/jina-embeddings-v2-base-de
     ```
     ```bash
     ollama pull llama3.2:3b
     ```
5. Populate the database with embeddings:
   ```bash
   python embedding.py
   ```

6. Start the application:
   ```bash
   streamlit run chat.py
   ```

## Notes
- Replace `<repository-url>` and `<repository-folder>` with the actual repository URL and folder name.
- Ensure Docker is running before starting Qdrant.
- If you encounter any issues, check the logs or refer to the documentation of the respective tools.

### Further Instructions
- Additional commands and usage details will be added here as the project evolves.