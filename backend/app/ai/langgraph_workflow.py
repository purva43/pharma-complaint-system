"""
LangGraph workflow for AI-powered complaint processing.
"""

from langgraph.graph import StateGraph, END
from app.ai.nodes import (
    GraphState,
    document_parser_node,
    field_extractor_node,
    risk_classifier_node,
    category_classifier_node,
    summary_generator_node,
    duplicate_detector_node,
    root_cause_analyzer_node,
    capa_recommender_node,
    completeness_checker_node,
)


def create_complaint_workflow():
    """
    Create the LangGraph workflow for complaint processing.
    
    Returns:
        Compiled LangGraph workflow
    """
    workflow = StateGraph(GraphState)
    
    workflow.add_node("document_parser", document_parser_node)
    workflow.add_node("field_extractor", field_extractor_node)
    workflow.add_node("risk_classifier", risk_classifier_node)
    workflow.add_node("category_classifier", category_classifier_node)
    workflow.add_node("summary_generator", summary_generator_node)
    workflow.add_node("duplicate_detector", duplicate_detector_node)
    workflow.add_node("root_cause_analyzer", root_cause_analyzer_node)
    workflow.add_node("capa_recommender", capa_recommender_node)
    workflow.add_node("completeness_checker", completeness_checker_node)
    
    workflow.set_entry_point("document_parser")
    
    workflow.add_edge("document_parser", "field_extractor")
    workflow.add_edge("field_extractor", "risk_classifier")
    workflow.add_edge("risk_classifier", "category_classifier")
    workflow.add_edge("category_classifier", "summary_generator")
    workflow.add_edge("summary_generator", "duplicate_detector")
    workflow.add_edge("duplicate_detector", "root_cause_analyzer")
    workflow.add_edge("root_cause_analyzer", "capa_recommender")
    workflow.add_edge("capa_recommender", "completeness_checker")
    workflow.add_edge("completeness_checker", END)
    
    compiled_workflow = workflow.compile()
    
    return compiled_workflow


async def process_complaint_with_ai(complaint_id: str, document_content: str):
    """
    Process a complaint through the AI workflow.
    
    Args:
        complaint_id: UUID of the complaint
        document_content: Raw document content
        
    Returns:
        dict: Complete AI processing results
    """
    workflow = create_complaint_workflow()
    
    initial_state = {
        "complaint_id": complaint_id,
        "document_content": document_content,
        "extracted_text": "",
        "extracted_fields": {},
        "risk_assessment": {},
        "category": {},
        "summary": {},
        "duplicates": {},
        "root_causes": {},
        "capa_recommendations": {},
        "completeness": {},
        "ai_logs": [],
    }
    
    final_state = await workflow.ainvoke(initial_state)
    
    return final_state


__all__ = [
    "create_complaint_workflow",
    "process_complaint_with_ai",
]
