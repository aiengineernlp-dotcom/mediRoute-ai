# llm_output_parser.py
"""
LLM Output Parser using Regex.
Use case: Extract structured data from unstructured LLM outputs.
This mirrors LangChain's OutputParsers exactly.
Stack: Regex + Exceptions → foundation for LangChain OutputParsers.
"""
import re
import json
from typing import Optional


class LLMOutputParser:
    """
    Parses various LLM output formats into structured Python objects.
    Handles: JSON blocks, key-value pairs, lists, scores.
    """

    # Patterns compilés — performance sur gros volumes
    PATTERNS = {
        "json_block":   re.compile(
            r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```',
            re.DOTALL
        ),
        "json_inline":  re.compile(r'(\{[^{}]+\})', re.DOTALL),
        "score":        re.compile(
            r'(?:score|rating|confidence)[:\s]+([0-9.]+)',
            re.IGNORECASE
        ),
        "percentage":   re.compile(r'([0-9.]+)\s*%'),
        "key_value":    re.compile(
            r'^([A-Za-z_][A-Za-z0-9_\s]*?):\s*(.+)$',
            re.MULTILINE
        ),
        "bullet_list":  re.compile(
            r'^[-*•]\s*(.+)$',
            re.MULTILINE
        ),
        "numbered_list":re.compile(
            r'^\d+[.)]\s*(.+)$',
            re.MULTILINE
        ),
        "emails":       re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        ),
        "urls":         re.compile(
            r'https?://[^\s<>"{}|\\^`\[\]]+'
        ),
    }

    def extract_json(self, text: str) -> Optional[dict | list]:
        """Extract first valid JSON from LLM output."""
        # Essayer d'abord les blocs de code markdown
        match = self.PATTERNS["json_block"].search(text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # Essayer le JSON inline
        for match in self.PATTERNS["json_inline"].finditer(text):
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue

        raise ValueError("No valid JSON found in LLM output")

    def extract_score(self, text: str) -> Optional[float]:
        """Extract a numerical score from LLM output."""
        # Chercher score explicite
        match = self.PATTERNS["score"].search(text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass

        # Chercher pourcentage
        match = self.PATTERNS["percentage"].search(text)
        if match:
            try:
                return float(match.group(1)) / 100
            except ValueError:
                pass

        return None

    def extract_key_values(self, text: str) -> dict:
        """Extract key-value pairs from structured LLM output."""
        matches = self.PATTERNS["key_value"].findall(text)
        return {
            key.strip(): value.strip()
            for key, value in matches
        }

    def extract_list(self, text: str) -> list[str]:
        """Extract bullet or numbered list items."""
        bullet  = self.PATTERNS["bullet_list"].findall(text)
        numbered = self.PATTERNS["numbered_list"].findall(text)
        return [item.strip() for item in (bullet or numbered)]

    def extract_emails(self, text: str) -> list[str]:
        """Extract all email addresses."""
        return self.PATTERNS["emails"].findall(text)

    def extract_urls(self, text: str) -> list[str]:
        """Extract all URLs."""
        return self.PATTERNS["urls"].findall(text)

    def parse_classification_output(self, text: str) -> dict:
        """
        Parse LLM classification output.
        Expects: label + confidence + reasoning.
        """
        result = {}

        # Label
        label_match = re.search(
            r'(?:label|class|category)[:\s]+([A-Za-z_]+)',
            text, re.IGNORECASE
        )
        if label_match:
            result["label"] = label_match.group(1).upper()

        # Confidence
        score = self.extract_score(text)
        if score is not None:
            result["confidence"] = round(
                score if score <= 1 else score / 100, 4
            )

        # Reasoning
        reason_match = re.search(
            r'(?:reason|because|explanation)[:\s]+(.+?)(?:\n|$)',
            text, re.IGNORECASE
        )
        if reason_match:
            result["reasoning"] = reason_match.group(1).strip()

        return result


# Test avec des outputs LLM réels simulés
parser = LLMOutputParser()

outputs = {
    "json_in_markdown": """
Sure! Here's the analysis:
```json
{
    "sentiment": "positive",
    "score": 0.87,
    "keywords": ["excellent", "fast", "reliable"],
    "category": "product_review"
}
```

Let me know if you need more details.
""",

    "classification": """
Based on my analysis:
Label: SPAM
Confidence score: 0.94
Reason: Contains multiple promotional keywords and suspicious links.
""",

    "structured_kv": """
Model: gpt-4o
Temperature: 0.7
Max tokens: 2048
Provider: OpenAI
Status: production
""",

    "bullet_list": """
Here are the key steps:
- Load and preprocess the documents
- Generate embeddings using text-embedding-3-small
- Store embeddings in a vector database
- Retrieve top-k similar chunks for each query
- Augment the prompt with retrieved context
""",

    "with_contacts": """
Please contact the team:
- Tech lead: alice@startup.ai
- Data scientist: bob@company.com
Visit our docus at https://docs.langchain.com
""",
}

print("=" * 55)
print(f"{'LLM OUTPUT PARSER TESTS':^55}")
print("=" * 55)

# Test 1 : JSON
print("\n1. JSON EXTRACTION:")
try:
    data = parser.extract_json(outputs["json_in_markdown"])
    print(f"  ✅ Extracted: {data}")
except ValueError as e:
    print(f"  ❌ {e}")

# Test 2 : Classification
print("\n2. CLASSIFICATION PARSING:")
cls_result = parser.parse_classification_output(
    outputs["classification"]
)
print(f"  ✅ {cls_result}")

# Test 3 : Key-values
print("\n3. KEY-VALUE EXTRACTION:")
kv = parser.extract_key_values(outputs["structured_kv"])
for k, v in kv.items():
    print(f"  {k:<15}: {v}")

# Test 4 : Liste
print("\n4. LIST EXTRACTION:")
items = parser.extract_list(outputs["bullet_list"])
for item in items:
    print(f"  → {item}")

# Test 5 : Contacts
print("\n5. CONTACTS EXTRACTION:")
emails = parser.extract_emails(outputs["with_contacts"])
urls   = parser.extract_urls(outputs["with_contacts"])
print(f"  Emails: {emails}")
print(f"  URLs  : {urls}")