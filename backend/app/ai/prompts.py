"""
Prompt templates for AI processing nodes.
"""

DOCUMENT_PARSER_PROMPT = """
You are a document parsing expert. Extract clean text from the provided document content.

DOCUMENT CONTENT:
{document_content}

TASK:
1. Extract all readable text from the document
2. Remove any formatting artifacts, headers, footers
3. Preserve the structure and order of information
4. Return the cleaned text

OUTPUT:
Return only the cleaned text, nothing else.
"""

FIELD_EXTRACTOR_PROMPT = """
You are a pharmaceutical quality expert. Extract structured information from the complaint text.

COMPLAINT TEXT:
{complaint_text}

TASK:
Extract the following fields from the complaint:
1. product_name - Name of the pharmaceutical product
2. batch_lot_no - Batch or lot number mentioned
3. description - Full description of the complaint
4. reporter_name - Name of the person reporting
5. reporter_email - Email address of reporter
6. reporter_phone - Phone number of reporter
7. received_date - Date when the complaint was received (YYYY-MM-DD format)

OUTPUT FORMAT:
Return a JSON object with the extracted fields. Use null for fields that cannot be found.
"""

RISK_CLASSIFIER_PROMPT = """
You are a pharmaceutical risk assessment expert. Classify the risk level of this complaint.

COMPLAINT DATA:
{complaint_data}

TASK:
Classify the risk level based on:
- Potential patient harm
- Regulatory impact
- Product quality impact
- Business impact

RISK LEVELS:
- critical: Could cause serious patient harm or death, major regulatory violation
- major: Could cause moderate harm, significant quality issue, requires investigation
- minor: Low impact, cosmetic issue, no patient harm

OUTPUT FORMAT:
Return a JSON object:
{{
  "risk_level": "critical|major|minor",
  "confidence": 0.95,
  "justification": "Explanation for the risk classification"
}}
"""

CATEGORY_CLASSIFIER_PROMPT = """
You are a pharmaceutical quality expert. Classify the complaint category.

COMPLAINT DATA:
{complaint_data}

TASK:
Classify the complaint into one of these categories:
- quality: Product quality issues (potency, purity, dissolution)
- safety: Safety concerns (adverse events, contamination)
- packaging: Packaging defects (broken seals, damaged boxes)
- labeling: Labeling errors (wrong information, missing warnings)
- efficacy: Product not working as expected

OUTPUT FORMAT:
Return a JSON object:
{{
  "category": "quality|safety|packaging|labeling|efficacy",
  "confidence": 0.92,
  "justification": "Explanation for category classification"
}}
"""

SUMMARY_GENERATOR_PROMPT = """
You are a pharmaceutical quality expert. Generate a concise summary of the complaint.

COMPLAINT DATA:
{complaint_data}

TASK:
Generate a 2-3 sentence summary that includes:
- What the complaint is about
- Key details (product, batch number if available)
- Nature of the issue

OUTPUT FORMAT:
Return a JSON object:
{{
  "summary": "Concise summary text"
}}
"""

DUPLICATE_DETECTOR_PROMPT = """
You are a pharmaceutical quality expert. Detect if this complaint is similar to previous complaints.

CURRENT COMPLAINT:
{current_complaint}

PREVIOUS COMPLAINTS:
{previous_complaints}

TASK:
Compare the current complaint with previous complaints and identify potential duplicates.
Consider:
- Same product and batch number
- Similar issue description
- Same reporter
- Similar time frame

OUTPUT FORMAT:
Return a JSON object:
{{
  "is_duplicate": true|false,
  "similar_complaints": [
    {{
      "complaint_id": "uuid",
      "similarity_score": 0.85,
      "reason": "Similar issue with same batch"
    }}
  ],
  "confidence": 0.88
}}
"""

ROOT_CAUSE_ANALYZER_PROMPT = """
You are a pharmaceutical quality expert. Suggest potential root causes for this complaint.

COMPLAINT DATA:
{complaint_data}

TASK:
Analyze the complaint and suggest 2-3 potential root causes.
Consider common pharmaceutical manufacturing issues:
- Raw material quality
- Manufacturing process deviation
- Equipment malfunction
- Storage/handling issues
- Human error
- Supplier issues

OUTPUT FORMAT:
Return a JSON object:
{{
  "root_causes": [
    {{
      "cause": "Description of root cause",
      "likelihood": "high|medium|low",
      "evidence": "Supporting evidence from complaint"
    }}
  ]
}}
"""

CAPA_RECOMMENDER_PROMPT = """
You are a pharmaceutical quality expert. Recommend corrective and preventive actions.

COMPLAINT DATA:
{complaint_data}

ROOT CAUSES:
{root_causes}

TASK:
Recommend appropriate corrective and preventive actions based on the root causes.
Corrective actions: Immediate actions to address the current issue
Preventive actions: Long-term actions to prevent recurrence

OUTPUT FORMAT:
Return a JSON object:
{{
  "corrective_actions": [
    {{
      "action": "Description of corrective action",
      "priority": "high|medium|low",
      "timeline": "Immediate/Short-term"
    }}
  ],
  "preventive_actions": [
    {{
      "action": "Description of preventive action",
      "priority": "high|medium|low",
      "timeline": "Long-term"
    }}
  ]
}}
"""

COMPLETENESS_CHECKER_PROMPT = """
You are a pharmaceutical quality expert. Check if the complaint form is complete.

COMPLAINT DATA:
{complaint_data}

TASK:
Check if all required fields are present and valid.
Required fields:
- product_name
- description
- received_date
- reporter_name
- reporter_email

Optional but recommended:
- batch_lot_no
- reporter_phone
- category

OUTPUT FORMAT:
Return a JSON object:
{{
  "is_complete": true|false,
  "missing_fields": [
    {{
      "field": "field_name",
      "reason": "Why this field is needed"
    }}
  ],
  "suggestions": [
    "Suggestion to improve the complaint"
  ]
}}
"""
