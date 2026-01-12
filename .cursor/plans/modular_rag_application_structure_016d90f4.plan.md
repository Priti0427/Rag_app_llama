---
name: Modular RAG Application Structure
overview: Restructure the RAG application into a modular package architecture with separate modules for configuration, document processing, embeddings, models, query engine, and the main application. Consolidate duplicate files and organize code by responsibility.
todos:
  - id: create_package_structure
    content: Create src/rag_app/ package directory with __init__.py
    status: completed
  - id: implement_config
    content: Create config.py with centralized configuration management
    status: completed
    dependencies:
      - create_package_structure
  - id: implement_document_processor
    content: Create document_processor.py for PDF loading and processing
    status: completed
    dependencies:
      - create_package_structure
  - id: implement_embeddings
    content: Create embeddings.py for embedding model management
    status: completed
    dependencies:
      - create_package_structure
      - implement_config
  - id: implement_models
    content: Create models.py for LLM model loading and generation
    status: completed
    dependencies:
      - create_package_structure
      - implement_config
  - id: implement_query_engine
    content: Create query_engine.py for query engine and retriever setup
    status: completed
    dependencies:
      - create_package_structure
      - implement_config
  - id: implement_prompts
    content: Create prompts.py for prompt template management
    status: completed
    dependencies:
      - create_package_structure
  - id: refactor_rag_system
    content: Refactor rag_system.py to use all new modules
    status: completed
    dependencies:
      - implement_document_processor
      - implement_embeddings
      - implement_models
      - implement_query_engine
      - implement_prompts
  - id: consolidate_app
    content: Consolidate app.py and app1.py into single clean app.py
    status: completed
    dependencies:
      - refactor_rag_system
  - id: create_requirements
    content: Create requirements.txt with all dependencies
    status: completed
  - id: create_env_example
    content: Create .env.example template file
    status: completed
  - id: organize_notebooks
    content: Move notebooks to examples/ directory
    status: completed
  - id: update_readme
    content: Update README.md with new structure and usage instructions
    status: completed
    dependencies:
      - consolidate_app
  - id: cleanup_old_files
    content: Remove duplicate files (app1.py, rag1.py)
    status: completed
    dependencies:
      - consolidate_app
---

# Modular RAG Application Structure

## Current State Analysis

- Duplicate files: `app.py`/`app1.py` and `rag.py`/`rag1.py`
- Monolithic `RAGSystem` class handling all responsibilities
- No configuration management
- Hard-coded model names and parameters
- Flat file structure

## Proposed Structure

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
├── app.py                         # Streamlit application (consolidated)
├── requirements.txt               # Dependencies
├── README.md                      # Updated documentation
├── .env.example                   # Environment variables template
├── examples/                      # Notebooks moved here
│   ├── llama.ipynb
│   └── rag_app2.ipynb
└── content1/                      # Existing content directory
    └── 2308.12950v3.pdf
```

## Implementation Details

### 1. Configuration Module (`src/rag_app/config.py`)

- Centralize all configuration settings
- Support environment variables and config files
- Default values for:
  - Embedding model: `BAAI/bge-small-en-v1.5`
  - LLM model: `Qwen/Qwen2.5-1.5B-Instruct`
  - Chunk size: 256
  - Chunk overlap: 15
  - Top-k retrieval: 2
  - Similarity cutoff: 0.5
  - Generation parameters (temperature, top_p, etc.)

### 2. Document Processor (`src/rag_app/document_processor.py`)

- `DocumentProcessor` class
- PDF loading functionality
- Temporary file management
- Document validation
- Extensible for future document types

### 3. Embeddings Module (`src/rag_app/embeddings.py`)

- `EmbeddingManager` class
- Initialize and manage HuggingFace embeddings
- Configure LlamaIndex Settings for embeddings

### 4. Models Module (`src/rag_app/models.py`)

- `LLMModel` class
- Model and tokenizer loading
- Generation parameters management
- Response decoding logic

### 5. Query Engine Module (`src/rag_app/query_engine.py`)

- `QueryEngineBuilder` class
- Create vector store index
- Configure retriever
- Setup query engine with postprocessors

### 6. Prompts Module (`src/rag_app/prompts.py`)

- `PromptTemplate` class
- Centralized prompt templates
- Easy to modify and extend

### 7. RAG System (`src/rag_app/rag_system.py`)

- `RAGSystem` class (refactored)
- Orchestrates all components
- Clean public API:
  - `process_pdf(file_content)`
  - `get_query_engine()`
  - `generate_response(query_engine, query)`

### 8. Application (`app.py`)

- Consolidate `app.py` and `app1.py` into one clean version
- Use the modular RAG system
- Clean UI code separation

### 9. Supporting Files

- `requirements.txt`: All dependencies
- `.env.example`: Template for environment variables
- Updated `README.md`: Usage instructions and architecture overview

## Migration Strategy

1. Create package structure
2. Implement each module with extracted functionality
3. Update RAGSystem to use new modules
4. Consolidate app files
5. Create requirements.txt
6. Move notebooks to examples/
7. Remove old duplicate files (app1.py, rag1.py)
8. Update README

## Benefits

- **Separation of Concerns**: Each module has a single responsibility
- **Maintainability**: Easy to modify individual components
- **Testability**: Each module can be tested independently
- **Extensibility**: Easy to add new document types, models, or retrieval strategies
- **Configuration**: Centralized and environment-aware
- **Clean Code**: No duplication, organized structure