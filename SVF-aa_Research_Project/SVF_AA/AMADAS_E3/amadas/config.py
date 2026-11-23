import os
from dotenv import load_dotenv
load_dotenv()

def get_llm():
    provider = os.getenv('LLM_PROVIDER', 'ollama').lower()
    if provider == 'ollama':
        from langchain_ollama import ChatOllama
        return ChatOllama(model=os.getenv('OLLAMA_MODEL', 'qwen2.5:7b'), temperature=0)
    if provider == 'openai':
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'), temperature=0)
    raise ValueError(f'Unsupported LLM_PROVIDER: {provider}')
