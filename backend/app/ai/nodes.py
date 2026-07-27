"""
AI processing nodes for LangGraph workflow.
"""

import json
import time
from typing import TypedDict
from app.ai.groq_client import groq_client
from app.ai.prompts import (
    DOCUMENT_PARSER_PROMPT,
    FIELD_EXTRACTOR_PROMPT,
    RISK_CLASSIFIER_PROMPT,
    CATEGORY_CLASSIFIER_PROMPT,
    SUMMARY_GENERATOR_PROMPT,
    DUPLICATE_DETECTOR_PROMPT,
    ROOT_CAUSE_ANALYZER_PROMPT,
    CAPA_RECOMMENDER_PROMPT,
    COMPLETENESS_CHECKER_PROMPT,
)


class GraphState(TypedDict):
    """State for the LangGraph workflow."""
    complaint_id: str
    document_content: str
    extracted_text: str
    extracted_fields: dict
    risk_assessment: dict
    category: dict
    summary: dict
    duplicates: dict
    root_causes: dict
    capa_recommendations: dict
    completeness: dict
    ai_logs: list[dict]


async def document_parser_node(state: GraphState) -> GraphState:
    """Parse document and extract clean text."""
    start_time = time.time()
    
    try:
        prompt = DOCUMENT_PARSER_PROMPT.format(
            document_content=state["document_content"]
        )
        
        messages = [
            {"role": "system", "content": "You are a document parsing expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await groq_client.chat_completion(
            messages=messages,
            temperature=0.3,
            max_tokens=2000
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        state["ai_logs"].append({
            "node_name": "document_parser",
            "input_data": {"document_content_length": len(state["document_content"])},
            "output_data": {"extracted_text_length": len(response["content"])},
            "confidence_score": 1.0,
            "processing_time_ms": processing_time,
            "model_used": response["model"],
        })
        
        state["extracted_text"] = response["content"]
        
    except Exception as e:
        state["ai_logs"].append({
            "node_name": "document_parser",
            "error_message": str(e),
        })
        state["extracted_text"] = state["document_content"]
    
    return state


async def field_extractor_node(state: GraphState) -> GraphState:
    """Extract structured fields from complaint text."""
    start_time = time.time()
    
    try:
        prompt = FIELD_EXTRACTOR_PROMPT.format(
            complaint_text=state["extracted_text"]
        )
        
        messages = [
            {"role": "system", "content": "You are a pharmaceutical quality expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await groq_client.chat_completion(
            messages=messages,
            temperature=0.3,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        extracted_fields = json.loads(response["content"])
        
        state["ai_logs"].append({
            "node_name": "field_extractor",
            "input_data": {"text_length": len(state["extracted_text"])},
            "output_data": extracted_fields,
            "confidence_score": 0.85,
            "processing_time_ms": processing_time,
            "model_used": response["model"],
        })
        
        state["extracted_fields"] = extracted_fields
        
    except Exception as e:
        state["ai_logs"].append({
            "node_name": "field_extractor",
            "error_message": str(e),
        })
        state["extracted_fields"] = {}
    
    return state


async def risk_classifier_node(state: GraphState) -> GraphState:
    """Classify the risk level of the complaint."""
    start_time = time.time()
    
    try:
        prompt = RISK_CLASSIFIER_PROMPT.format(
            complaint_data=json.dumps(state["extracted_fields"], indent=2)
        )
        
        messages = [
            {"role": "system", "content": "You are a pharmaceutical risk assessment expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await groq_client.chat_completion(
            messages=messages,
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        risk_assessment = json.loads(response["content"])
        
        state["ai_logs"].append({
            "node_name": "risk_classifier",
            "input_data": state["extracted_fields"],
            "output_data": risk_assessment,
            "confidence_score": risk_assessment.get("confidence", 0.8),
            "processing_time_ms": processing_time,
            "model_used": response["model"],
        })
        
        state["risk_assessment"] = risk_assessment
        
    except Exception as e:
        state["ai_logs"].append({
            "node_name": "risk_classifier",
            "error_message": str(e),
        })
        state["risk_assessment"] = {"risk_level": "minor", "confidence": 0.5}
    
    return state


async def category_classifier_node(state: GraphState) -> GraphState:
    """Classify the complaint category."""
    start_time = time.time()
    
    try:
        prompt = CATEGORY_CLASSIFIER_PROMPT.format(
            complaint_data=json.dumps(state["extracted_fields"], indent=2)
        )
        
        messages = [
            {"role": "system", "content": "You are a pharmaceutical quality expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await groq_client.chat_completion(
            messages=messages,
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        category = json.loads(response["content"])
        
        state["ai_logs"].append({
            "node_name": "category_classifier",
            "input_data": state["extracted_fields"],
            "output_data": category,
            "confidence_score": category.get("confidence", 0.8),
            "processing_time_ms": processing_time,
            "model_used": response["model"],
        })
        
        state["category"] = category
        
    except Exception as e:
        state["ai_logs"].append({
            "node_name": "category_classifier",
            "error_message": str(e),
        })
        state["category"] = {"category": "quality", "confidence": 0.5}
    
    return state


async def summary_generator_node(state: GraphState) -> GraphState:
    """Generate a concise summary of the complaint."""
    start_time = time.time()
    
    try:
        prompt = SUMMARY_GENERATOR_PROMPT.format(
            complaint_data=json.dumps(state["extracted_fields"], indent=2)
        )
        
        messages = [
            {"role": "system", "content": "You are a pharmaceutical quality expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await groq_client.chat_completion(
            messages=messages,
            temperature=0.5,
            max_tokens=300,
            response_format={"type": "json_object"}
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        summary = json.loads(response["content"])
        
        state["ai_logs"].append({
            "node_name": "summary_generator",
            "input_data": state["extracted_fields"],
            "output_data": summary,
            "confidence_score": 0.9,
            "processing_time_ms": processing_time,
            "model_used": response["model"],
        })
        
        state["summary"] = summary
        
    except Exception as e:
        state["ai_logs"].append({
            "node_name": "summary_generator",
            "error_message": str(e),
        })
        state["summary"] = {"summary": state["extracted_fields"].get("description", "")}
    
    return state


async def duplicate_detector_node(state: GraphState) -> GraphState:
    """Detect duplicate complaints."""
    start_time = time.time()
    
    try:
        previous_complaints = []
        
        prompt = DUPLICATE_DETECTOR_PROMPT.format(
            current_complaint=json.dumps(state["extracted_fields"], indent=2),
            previous_complaints=json.dumps(previous_complaints, indent=2)
        )
        
        messages = [
            {"role": "system", "content": "You are a pharmaceutical quality expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await groq_client.chat_completion(
            messages=messages,
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        duplicates = json.loads(response["content"])
        
        state["ai_logs"].append({
            "node_name": "duplicate_detector",
            "input_data": {"current_complaint": state["extracted_fields"]},
            "output_data": duplicates,
            "confidence_score": duplicates.get("confidence", 0.8),
            "processing_time_ms": processing_time,
            "model_used": response["model"],
        })
        
        state["duplicates"] = duplicates
        
    except Exception as e:
        state["ai_logs"].append({
            "node_name": "duplicate_detector",
            "error_message": str(e),
        })
        state["duplicates"] = {"is_duplicate": False, "similar_complaints": [], "confidence": 0.5}
    
    return state


async def root_cause_analyzer_node(state: GraphState) -> GraphState:
    """Analyze potential root causes."""
    start_time = time.time()
    
    try:
        prompt = ROOT_CAUSE_ANALYZER_PROMPT.format(
            complaint_data=json.dumps(state["extracted_fields"], indent=2)
        )
        
        messages = [
            {"role": "system", "content": "You are a pharmaceutical quality expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await groq_client.chat_completion(
            messages=messages,
            temperature=0.5,
            max_tokens=800,
            response_format={"type": "json_object"}
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        root_causes = json.loads(response["content"])
        
        state["ai_logs"].append({
            "node_name": "root_cause_analyzer",
            "input_data": state["extracted_fields"],
            "output_data": root_causes,
            "confidence_score": 0.8,
            "processing_time_ms": processing_time,
            "model_used": response["model"],
        })
        
        state["root_causes"] = root_causes
        
    except Exception as e:
        state["ai_logs"].append({
            "node_name": "root_cause_analyzer",
            "error_message": str(e),
        })
        state["root_causes"] = {"root_causes": []}
    
    return state


async def capa_recommender_node(state: GraphState) -> GraphState:
    """Recommend corrective and preventive actions."""
    start_time = time.time()
    
    try:
        prompt = CAPA_RECOMMENDER_PROMPT.format(
            complaint_data=json.dumps(state["extracted_fields"], indent=2),
            root_causes=json.dumps(state["root_causes"], indent=2)
        )
        
        messages = [
            {"role": "system", "content": "You are a pharmaceutical quality expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await groq_client.chat_completion(
            messages=messages,
            temperature=0.5,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        capa = json.loads(response["content"])
        
        state["ai_logs"].append({
            "node_name": "capa_recommender",
            "input_data": {
                "complaint_data": state["extracted_fields"],
                "root_causes": state["root_causes"]
            },
            "output_data": capa,
            "confidence_score": 0.8,
            "processing_time_ms": processing_time,
            "model_used": response["model"],
        })
        
        state["capa_recommendations"] = capa
        
    except Exception as e:
        state["ai_logs"].append({
            "node_name": "capa_recommender",
            "error_message": str(e),
        })
        state["capa_recommendations"] = {"corrective_actions": [], "preventive_actions": []}
    
    return state


async def completeness_checker_node(state: GraphState) -> GraphState:
    """Check complaint form completeness."""
    start_time = time.time()
    
    try:
        prompt = COMPLETENESS_CHECKER_PROMPT.format(
            complaint_data=json.dumps(state["extracted_fields"], indent=2)
        )
        
        messages = [
            {"role": "system", "content": "You are a pharmaceutical quality expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = await groq_client.chat_completion(
            messages=messages,
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        completeness = json.loads(response["content"])
        
        state["ai_logs"].append({
            "node_name": "completeness_checker",
            "input_data": state["extracted_fields"],
            "output_data": completeness,
            "confidence_score": 0.9,
            "processing_time_ms": processing_time,
            "model_used": response["model"],
        })
        
        state["completeness"] = completeness
        
    except Exception as e:
        state["ai_logs"].append({
            "node_name": "completeness_checker",
            "error_message": str(e),
        })
        state["completeness"] = {"is_complete": True, "missing_fields": [], "suggestions": []}
    
    return state
