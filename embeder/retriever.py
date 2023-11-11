from vector_db import add_vector, get_top_neighbors
from embedder import Embedder
import numpy as np


text = "EU has been subsidizing its own steel industry for decades"

def get_most_close_sources(text: str, top_k:int):

    model_name = 'thenlper/gte-base'
    embedder = Embedder(model_name=model_name)

    embedding=embedder.embedd([text])[0]
    embedding = np.array(embedding)

    neighbours = get_top_neighbors(embedding, top_k)
    # for a in neighbours:
    #     print(a.link)

    return neighbours

