from dataclasses import dataclass

"""

3 → directly answers the question
2 → useful/supporting information
1 → somewhat relevant
0 → irrelevant
"""
@dataclass
class RAGRetrievalExample:
    query: str
    relevant_chunks: dict[str, int]  # Mapping of chunk_id to relevance score (0-3)


dataset = [

    # ============================================================
    # RETURN POLICY
    # ============================================================

    # Straightforward
    RAGRetrievalExample(
        query="What is the return policy for purchases?",
        relevant_chunks={"return_policy_0": 3},
    ),

    # Paraphrased
    RAGRetrievalExample(
        query="How long do I have to send a product back?",
        relevant_chunks={"return_policy_0": 3},
    ),
    # Paraphrased
    RAGRetrievalExample(
    query="When can I expect the refund?",
    relevant_chunks={
        "return_policy_3": 3,
        "refund_policy_0": 3,
        "return_policy_2": 3,
        "refund_policy_1": 3,
        "refund_policy_3": 2,
    },
),

    # Specific condition
    RAGRetrievalExample(
        query="Can I return an opened product?",
        relevant_chunks={"return_policy_0": 3, "return_policy_1": 2},
    ),

    # Edge case
    RAGRetrievalExample(
        query="Can I return an opened product if it is defective?",
        relevant_chunks={"return_policy_2": 3},
    ),


    # ============================================================
    # CANCELLATION
    # ============================================================

    # Normal cancellation
    RAGRetrievalExample(
        query="How can I cancel my order?",
        relevant_chunks={"cancellation_policy_0": 3},
    ),

    # After shipment
    RAGRetrievalExample(
        query="Can I cancel my order after it has shipped?",
        relevant_chunks={"cancellation_policy_1": 3},
    ),

    # Paraphrased 
    RAGRetrievalExample(
        query="Until when can I cancel an order?",
        relevant_chunks={"cancellation_policy_0": 3, "cancellation_policy_1": 2},
    ),

    # Specific condition
    RAGRetrievalExample(
        query="Is there a cancellation fee?",
        relevant_chunks={"cancellation_policy_1": 2},
    ),


    # ============================================================
    # SHIPPING
    # ============================================================

    # Standard
    RAGRetrievalExample(
        query="What is the shipping time for standard delivery?",
        relevant_chunks={"shipping_policy_0": 3},
    ),

    # Paraphrased
    RAGRetrievalExample(
        query="How long does regular delivery usually take?",
        relevant_chunks={"shipping_policy_0": 3},
    ),

    # Express
    RAGRetrievalExample(
        query="How quickly will my order arrive with express delivery?",
        relevant_chunks={"shipping_policy_0": 3},
    ),


    # Tracking
    RAGRetrievalExample(
        query="How can I track my order?",
        relevant_chunks={"shipping_policy_1": 3},
    ),
    RAGRetrievalExample(
            query="Why is the order delayed?",
            relevant_chunks={"shipping_policy_1": 3, "shipping_policy_2": 2},
        ),


    # ============================================================
    # NO-ANSWER / OUT-OF-KB
    # ============================================================

    RAGRetrievalExample(
        query="How do I redeem loyalty points?",
        relevant_chunks={},
    ),

    RAGRetrievalExample(
        query="What is the nearest physical store?",
        relevant_chunks={},
    ),
    RAGRetrievalExample(
        query="How long does international shipping take?",
        relevant_chunks={},
    ),
]