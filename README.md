# RAG Application - PDF Question Answering System

A modular Retrieval-Augmented Generation (RAG) application for answering questions based on PDF documents. Built with LlamaIndex, HuggingFace Transformers, and Streamlit.

## Features

- **PDF Processing**: Upload and process PDF documents
- **Semantic Search**: Retrieve relevant context using vector embeddings
- **Question Answering**: Generate answers based on PDF content using LLM
- **Modular Architecture**: Clean, maintainable code structure
- **Configurable**: Easy to customize models and parameters

## Project Structure

```
Rag_app_llama-1/
├── src/
│   └── rag_app/
│       ├── __init__.py
│       ├── config.py              # Configuration management
│       ├── document_processor.py  # PDF loading and processing
│       ├── embeddings.py          # Embedding model management
│       ├── models.py              # LLM model loading and management
│       ├── query_engine.py        # Query engine and retriever setup
│       ├── prompts.py             # Prompt templates
│       └── rag_system.py          # Main RAG orchestrator
├── app.py                         # Streamlit application
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── examples/                      # Example notebooks
│   ├── llama.ipynb
│   └── rag_app2.ipynb
└── content1/                    # Sample PDFs
    └── 2308.12950v3.pdf
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Rag_app_llama-1
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

## Usage

### Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

### Using the Application

1. **Upload a PDF**: Use the sidebar to upload a PDF file
2. **Wait for Processing**: The system will process the PDF and create a vector index
3. **Ask Questions**: Enter your question in the main panel
4. **Get Answers**: Click "Get Answer" to generate a response based on the PDF content

## Configuration

The application can be configured through environment variables or by modifying the `Config` class in `src/rag_app/config.py`.

### Key Configuration Options

- **Embedding Model**: `EMBEDDING_MODEL_NAME` (default: `BAAI/bge-small-en-v1.5`)
- **LLM Model**: `LLM_MODEL_NAME` (default: `Qwen/Qwen2.5-1.5B-Instruct`)
- **Chunk Size**: `CHUNK_SIZE` (default: 256)
- **Chunk Overlap**: `CHUNK_OVERLAP` (default: 15)
- **Top-K Retrieval**: `SIMILARITY_TOP_K` (default: 2)
- **Similarity Cutoff**: `SIMILARITY_CUTOFF` (default: 0.5)

See `.env.example` for all available configuration options.

## Architecture

The application follows a modular architecture:

- **Config**: Centralized configuration management
- **DocumentProcessor**: Handles PDF loading and processing
- **EmbeddingManager**: Manages embedding model initialization
- **LLMModel**: Handles LLM loading and text generation
- **QueryEngineBuilder**: Creates query engines and retrievers
- **PromptTemplate**: Manages prompt templates
- **RAGSystem**: Orchestrates all components

## Dependencies

- **Streamlit**: Web application framework
- **LlamaIndex**: RAG framework for document indexing and retrieval
- **Transformers**: HuggingFace transformers for LLM models
- **PyTorch**: Deep learning framework

## Development

### Code Structure

The codebase is organized into logical modules:

- Each module has a single responsibility
- Components are loosely coupled and easily testable
- Configuration is centralized and environment-aware

### Extending the Application

To add new features:

1. **New Document Types**: Extend `DocumentProcessor` class
2. **Different Models**: Modify `Config` or use environment variables
3. **Custom Prompts**: Update `PromptTemplate` class
4. **Additional Retrieval Strategies**: Extend `QueryEngineBuilder`


## Acknowledgments

- Built with [LlamaIndex](https://www.llamaindex.ai/)
- Uses [HuggingFace Transformers](https://huggingface.co/transformers/)
- UI built with [Streamlit](https://streamlit.io/)
