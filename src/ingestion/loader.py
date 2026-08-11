# src/ingestion/loader.py
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

def load_and_chunk(data_dir: str = "data/questions", chunk_size: int = 512, chunk_overlap: int = 50):
    documents = SimpleDirectoryReader(data_dir).load_data()
    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nodes = splitter.get_nodes_from_documents(documents)
    return nodes

if __name__ == "__main__":
    nodes = load_and_chunk()
    print(f"Loaded {len(nodes)} chunks")
    print(nodes[0].text[:200])