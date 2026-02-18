# RFP Responder

import os
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# CONFIGURATION
# You need to set up your specific Index in Pinecone Console
INDEX_NAME = "enterprise-proposals-v1"

def get_retriever():
    """
    Connects to the Vector DB to fetch past winning proposals.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    # connecting to the existing index where data is stored
    vectorstore = Pinecone.from_existing_index(INDEX_NAME, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

# --- THE CORE LOGIC (Step 3 & 4) ---
def generate_proposal_section(question: str):
    """
    Pulls context and forces LLM to act as a Senior Proposal Writer.
    """
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.2)
    retriever = get_retriever()

    # The "Million Dollar" Prompt
    # We explicitly tell it to MIMIC the tone of the retrieved documents.
    template = """You are a Senior Proposal Writer for a top-tier consulting firm.
    
    Task: Write a specific section for a new RFP based ONLY on the context provided below.
    
    CRITICAL INSTRUCTIONS:
    1. Match the writing style, tone, and vocabulary of the Context exactly.
    2. Cite specific case studies from the Context if relevant.
    3. Do not use generic AI fluff (e.g., "In the rapidly evolving landscape").
    4. If the context does not support the answer, state that we need manual input.

    Context (Past Winning Proposals):
    {context}

    New RFP Requirement:
    {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    # The Retrieval Chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(question)

# --- THE CHALLENGE FOR YOU ---
if __name__ == "__main__":
    # TODO: INGESTION LAYER
    # I have left this open. You need to write the script that:
    # 1. Loads PDFs using PyPDFLoader
    # 2. Splits them using RecursiveCharacterTextSplitter (500 tokens)
    # 3. Upserts them to Pinecone
    
    print("Agent is ready. Implement the Ingestion Layer above to run.")
    # Example usage:
    # print(generate_proposal_section("Describe our safety protocols for high-voltage sites."))