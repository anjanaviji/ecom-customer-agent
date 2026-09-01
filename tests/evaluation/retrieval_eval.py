import math

from customer_agent.rag.reranker import Reranker
from customer_agent.rag.retriever import get_retriever
from rag_dataset import dataset


# ============================================================
# Dependencies
# ============================================================

vectorstore = get_retriever().vectorstore
reranker = Reranker()


# ============================================================
# NDCG
# ============================================================

def dcg_at_k(
    retrieved_chunks: list[str],
    relevant_chunks: dict[str, int],
    k: int,
) -> float:
    """
    Calculate DCG@K using graded relevance.

    Relevance scores:
        3 -> directly answers the question
        2 -> useful/supporting information
        1 -> somewhat relevant
        0 -> irrelevant
    """

    dcg = 0.0

    for rank, chunk_id in enumerate(
        retrieved_chunks[:k],
        start=1,
    ):
        relevance = relevant_chunks.get(
            chunk_id,
            0,
        )

        dcg += relevance / math.log2(rank + 1)

    return dcg


def ndcg_at_k(
    retrieved_chunks: list[str],
    relevant_chunks: dict[str, int],
    k: int,
) -> float | None:
    """
    Calculate NDCG@K using graded relevance.

    Returns None for unanswerable queries.
    """

    if not relevant_chunks:
        return None

    # --------------------------------------------------------
    # Actual DCG
    # --------------------------------------------------------

    actual_dcg = dcg_at_k(
        retrieved_chunks,
        relevant_chunks,
        k,
    )

    # --------------------------------------------------------
    # Ideal DCG
    #
    # Sort relevant chunks by relevance:
    #
    # 3 -> 3 -> 3 -> 2 -> 1
    # --------------------------------------------------------

    ideal_retrieved = [
        chunk_id
        for chunk_id, relevance in sorted(
            relevant_chunks.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    ]

    ideal_dcg = dcg_at_k(
        ideal_retrieved,
        relevant_chunks,
        k,
    )

    if ideal_dcg == 0:
        return 0.0

    return actual_dcg / ideal_dcg


# ============================================================
# Retrieval Strategies
# ============================================================

def baseline_retrieval(query: str):

    """
    Baseline:

        Query
          ↓
        Vector Search
          ↓
        Top 5
    """

    return vectorstore.similarity_search(
        query,
        k=5,
    )


def reranked_retrieval(query: str):

    """
    Reranked:

        Query
          ↓
        Vector Search
          ↓
        Top 20 candidates
          ↓
        Cross Encoder
          ↓
        Top 5
    """

    # Stage 1: retrieve candidates
    candidates = vectorstore.similarity_search(
        query,
        k=20,
    )

    # Stage 2: rerank candidates
    reranked = reranker.rerank(
        query,
        candidates,
        top_k=5,
    )

    # Return documents only
    return [
        document
        for document, score in reranked
    ]


# ============================================================
# Metric Calculation
# ============================================================

def calculate_metrics(
    dataset,
    retrieve_fn,
    k: int = 5,
):
    """
    Evaluate a retrieval strategy using:

        Recall@1
        Recall@3
        Recall@5
        MRR@5
        NDCG@5

    Unanswerable questions are excluded.
    """

    recall_at_1 = 0
    recall_at_3 = 0
    recall_at_5 = 0

    reciprocal_ranks = []
    ndcg_scores = []

    answerable_count = 0

    for example in dataset:

        # ----------------------------------------------------
        # Skip unanswerable questions
        # ----------------------------------------------------

        if not example.relevant_chunks:
            continue

        answerable_count += 1

        # ----------------------------------------------------
        # Retrieve
        # ----------------------------------------------------

        documents = retrieve_fn(
            example.query
        )

        retrieved_chunks = [
            document.metadata["chunk_id"]
            for document in documents[:k]
        ]

        # Dictionary keys = relevant chunk IDs
        expected = set(
            example.relevant_chunks.keys()
        )

        # ----------------------------------------------------
        # Recall@1
        # ----------------------------------------------------

        if expected.intersection(
            retrieved_chunks[:1]
        ):
            recall_at_1 += 1

        # ----------------------------------------------------
        # Recall@3
        # ----------------------------------------------------

        if expected.intersection(
            retrieved_chunks[:3]
        ):
            recall_at_3 += 1

        # ----------------------------------------------------
        # Recall@5
        # ----------------------------------------------------

        if expected.intersection(
            retrieved_chunks[:5]
        ):
            recall_at_5 += 1

        # ----------------------------------------------------
        # MRR@5
        # ----------------------------------------------------

        reciprocal_rank = 0.0

        for rank, chunk_id in enumerate(
            retrieved_chunks,
            start=1,
        ):
            if chunk_id in expected:
                reciprocal_rank = 1 / rank
                break

        reciprocal_ranks.append(
            reciprocal_rank
        )

        # ----------------------------------------------------
        # NDCG@5
        # ----------------------------------------------------

        ndcg = ndcg_at_k(
            retrieved_chunks,
            example.relevant_chunks,
            k=5,
        )

        if ndcg is not None:
            ndcg_scores.append(ndcg)

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    return {
        "Recall@1": (
            recall_at_1 / answerable_count
        ),
        "Recall@3": (
            recall_at_3 / answerable_count
        ),
        "Recall@5": (
            recall_at_5 / answerable_count
        ),
        "MRR@5": (
            sum(reciprocal_ranks)
            / answerable_count
        ),
        "NDCG@5": (
            sum(ndcg_scores)
            / len(ndcg_scores)
        ),
    }


# ============================================================
# Baseline vs Reranked Comparison
# ============================================================

def compare_retrieval(
    dataset,
    k: int = 5,
):

    print("\n")
    print("=" * 60)
    print("BASELINE vs RERANKED")
    print("=" * 60)

    for example in dataset:

        if not example.relevant_chunks:
            continue

        expected = set(
            example.relevant_chunks.keys()
        )

        # ----------------------------------------------------
        # Baseline
        # ----------------------------------------------------

        baseline_docs = baseline_retrieval(
            example.query
        )

        baseline_chunks = [
            doc.metadata["chunk_id"]
            for doc in baseline_docs[:k]
        ]

        # ----------------------------------------------------
        # Reranked
        # ----------------------------------------------------

        reranked_docs = reranked_retrieval(
            example.query
        )

        reranked_chunks = [
            doc.metadata["chunk_id"]
            for doc in reranked_docs[:k]
        ]

        # ----------------------------------------------------
        # First relevant rank
        # ----------------------------------------------------

        def first_relevant_rank(chunks):

            for rank, chunk_id in enumerate(
                chunks,
                start=1,
            ):
                if chunk_id in expected:
                    return rank

            return None

        baseline_rank = first_relevant_rank(
            baseline_chunks
        )

        reranked_rank = first_relevant_rank(
            reranked_chunks
        )

        # ----------------------------------------------------
        # Output
        # ----------------------------------------------------

        print("\n--------------------------------")
        print("Query:", example.query)

        print("Expected:", expected)

        print(
            "Baseline:",
            baseline_chunks,
        )

        print(
            "Baseline first relevant rank:",
            baseline_rank,
        )

        print(
            "Reranked:",
            reranked_chunks,
        )

        print(
            "Reranked first relevant rank:",
            reranked_rank,
        )

        # ----------------------------------------------------
        # Classification
        # ----------------------------------------------------

        if (
            baseline_rank is not None
            and reranked_rank is not None
        ):

            if reranked_rank < baseline_rank:
                print(
                    "Result: RERANKER IMPROVED"
                )

            elif reranked_rank > baseline_rank:
                print(
                    "Result: RERANKER HURT"
                )

            else:
                print("Result: SAME")

        elif baseline_rank is not None:

            print(
                "Result: RERANKER LOST RELEVANT CHUNK"
            )

        elif reranked_rank is not None:

            print(
                "Result: RERANKER FOUND RELEVANT CHUNK"
            )

        else:

            print("Result: BOTH FAILED")


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Baseline
    # --------------------------------------------------------

    baseline_metrics = calculate_metrics(
        dataset,
        baseline_retrieval,
        k=5,
    )

    # --------------------------------------------------------
    # Reranked
    # --------------------------------------------------------

    reranked_metrics = calculate_metrics(
        dataset,
        reranked_retrieval,
        k=5,
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print("\n==============================")
    print("RETRIEVAL EVALUATION")
    print("==============================")

    print("\nBaseline:")

    for metric, value in baseline_metrics.items():
        print(
            f"{metric}: {value:.3f}"
        )

    print("\nReranked:")

    for metric, value in reranked_metrics.items():
        print(
            f"{metric}: {value:.3f}"
        )

    # --------------------------------------------------------
    # Detailed comparison
    # --------------------------------------------------------

    compare_retrieval(dataset)