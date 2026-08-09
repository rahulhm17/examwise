from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load model (only first time slow)
model = SentenceTransformer('all-MiniLM-L6-v2')


def find_similar_questions(questions, threshold=0.7):
    if not questions or len(questions) < 2:
        return []

    # Convert questions to embeddings
    embeddings = model.encode(questions)

    # Compute similarity matrix
    sim_matrix = cosine_similarity(embeddings)

    visited = set()
    groups = []

    for i in range(len(questions)):
        if i in visited:
            continue

        group = [questions[i]]
        visited.add(i)

        for j in range(i + 1, len(questions)):
            if sim_matrix[i][j] > threshold:
                group.append(questions[j])
                visited.add(j)

        if len(group) > 1:
            groups.append(group)

    return groups