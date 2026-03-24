import os
import re
import ast
import time
import redis
from github import Github

GITHUB_TOKEN = os.getenv("TOKEN")

def split_words(name):
    """Divide nombres en camelCase y snake_case."""
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', name).replace('_', ' ')
    return [w.lower() for w in words.split() if w.isalpha()]

def extract_python_methods(content):
    """Analiza AST para extraer nombres de funciones en Python."""
    try:
        tree = ast.parse(content)
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    except:
        return []

def extract_java_methods(content):
    """Usa Regex para extraer nombres de metodos en Java."""
    pattern = r'(?:public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\('
    return re.findall(pattern, content)

def start_mining():
    print("Miner started")
    g = Github(GITHUB_TOKEN)
    r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    
    repos = g.search_repositories(query='language:python language:java', sort='stars', order='desc')

    for repo in repos:
        print(f"Mining repository: {repo.full_name}")
        try:
            contents = repo.get_contents("")
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                elif file_content.name.endswith(('.py', '.java')):
                    print(f"  Analyzing file: {file_content.name}")
                    raw_code = file_content.decoded_content.decode('utf-8', errors='ignore')
                    names = extract_python_methods(raw_code) if file_content.name.endswith('.py') else extract_java_methods(raw_code)
                    for name in names:
                        for word in split_words(name):
                            r.zincrby('word_count', 1, word)
        except Exception as e:
            pass
        
        time.sleep(10)

if __name__ == "__main__":
    start_mining()