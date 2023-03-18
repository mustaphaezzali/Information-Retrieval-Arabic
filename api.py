from flask import Flask, request, jsonify
from utils import ArabicIndexer, ArabicTfidfVectorizer
from methods import preprocess
import pandas as pd

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

indexer = ArabicIndexer.load("indexer/indexer.pkl")

data = pd.read_csv("data.csv")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    top_n = request.args.get("top_n", 10)
    
    try:
        top_n = int(top_n)
    except ValueError:
        top_n = 10

    query = preprocess(query)
    
    results = indexer.search(query, top_n)
    
    # look for the file diroctory with doc_id in results
    files = [data[data["docno"] == doc_id]["files"].values[0] for doc_id, _ in results]
    
    result_docs = [{"doc_id": doc_id, "score": score, "file": file} for (doc_id, score), file in zip(results, files)]
    response = {"results": result_docs}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=False)