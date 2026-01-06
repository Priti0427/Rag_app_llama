from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine 
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.readers.file import PDFReader
from transformers import AutoModelForCausalLM, AutoTokenizer
import tempfile
import os

class RAGSystem:
    def __init__(self):
        self._initialize_settings()
        self._initialize_model()
        self.index = None

    def  _initialize_settings(self):
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        Settings.llm = None 
# if we have 5000 word document, if chunk size is 256, 5000/256 = 20 chunks
        Settings.chunk_size = 256
# content of last 15 words of first chunk == content of first 15 word of second chunk; to avoid loosing context we use chunk overlap
        Settings.chunk_overlap = 15   

    def _initialize_model(self):
        self.model_name = "Qwen/Qwen2.5-1.5B-Instruct" # 4gb model
        self.model = AutoModelForCausalLM.from_pretrained(
        self.model_name,
        trust_remote_code = False,
        revision = "main",
    #device_map = 'cuda:0' # when we try to load model on GPU. we have CPU, so comment this line.
    ) 

# load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast = True)

# load the PDF files
    def process_pdf(self,file_content):

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(file_content)
                tmp_path = tmp_file.name
        
        # Read PDF

            reader = PDFReader()
            documents = reader.load_data(tmp_path)

            self.index = VectorStoreIndex.from_documents(documents)

            # clean
            os.unlink(tmp_path)

            return True
        
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return False

    def get_query_engine(self,top_k = 2):

        if not self.index:
            raise ValueError("No index available. Please Process a PDF first")
        
        retriever = VectorIndexRetriever(
            index = self.index,
            similarity_top_k = top_k,
            )
        return RetrieverQueryEngine(
            retriever=retriever,
    # her, we are keeping similarity cut-off(dcuments which are 50% similar will be queried by the retriever queryengine and from those top2 will be retrived )
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.5)]
            )
    
    def _create_prompt(self, context, query):
        return f"""you are an AI assistant tasked with answering question based on the provided PDF content.
            Please analyze the following excerpt from the PDF and answer the question.
            PDF content:
            {context}

            Question : {query}

            Instructions:
            - Answer only based on the information provided in the PDF content above.
            - If the answer cannot be found in the provided content, say " I cannot find the answer to the question and provide a pdf documents"
            - BE concise and specific.
            - Include relevant quote or references from the PDF when applicable.

            Answer:
            """
    
    def generate_response(self, query_engine, query):

        try:
            response = query_engine.query(query)
            context = ""
            for node in response.source_nodes[:2]:
                context += f"{node.text}\n\n"

            if not context.strip():
                return "No relevant information from PDF document"

            # Creating a prompt and generating a response
            prompt = self._create_prompt(context, query)

            inputs = self.tokenizer(prompt, return_tensors = "pt", padding = True)
            outputs = self.model.generate(
                input_ids = inputs['input_ids'], 
                max_new_tokens = 512,
                num_return_sequences = 1,
                temperature = 0.3,
                top_p = 0.9,  # top probability
                do_sample = True,  # do sampling
                repetition_penalty = 1.2 # l1 and l2 regularisation

            )  
            response_text = self.tokenizer.decode(outputs[0], skip_special_tokens = True) 

            if "Answer" in response_text:
                response_text  = response_text.split("Answer: ")[-1].strip()

            return response_text if response_text else "Unable to generate a response from PDF documents"

        except Exception as e:
            print(f"Error generating a response:{str(e)}")
            return f" Error processing your question: {str(e)}" 
             