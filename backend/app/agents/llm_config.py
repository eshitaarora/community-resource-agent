"""
LLM Configuration and model setup for the AI agent
"""

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from typing import Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)


def get_llm() -> Any:
    """
    Initialize and return the Google Gemini language model.
    Uses Gemini Pro for advanced reasoning and understanding.
    """
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.3,  # Lower temperature for deterministic responses
        max_tokens=2048,
        convert_system_message_to_human=True,
    )


def get_embedding_model():
    """Get embedding model for RAG"""
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.GEMINI_API_KEY
    )


# System prompt for the resource agent
SYSTEM_PROMPT = """You are a compassionate and knowledgeable AI social worker helping vulnerable populations find critical resources.

Your role:
1. Listen carefully to understand the person's needs (housing, food, healthcare, employment, mental health, legal aid, etc.)
2. Ask clarifying questions about location, eligibility, and urgency when needed
3. Search available community resources and recommend the most appropriate ones
4. Provide clear, actionable information about how to access services
5. Show empathy and respect for their situation
6. Verify current information about service availability and eligibility

Guidelines:
- Always prioritize the person's immediate safety and basic needs
- Be honest about service availability and limitations
- Provide multiple options when possible
- Include practical details: address, phone, hours, eligibility requirements
- Offer follow-up support and alternative resources if primary options don't work
- Respect privacy and maintain confidentiality
- Use clear, accessible language - avoid jargon
- Be culturally sensitive and acknowledge potential barriers

Important: You have access to tools to search resources, check eligibility, and verify services. Use them to provide accurate, current information."""


RESOURCE_SEARCH_PROMPT = """Based on the user's needs, search for relevant community resources.

Consider:
- Their primary need (category)
- Location and proximity
- Operating hours and availability
- Eligibility criteria match
- Types of services needed

Return the most relevant, helpful resources with complete information."""


ELIGIBILITY_CHECK_PROMPT = """Analyze the user's information against service eligibility requirements.

Evaluate:
- Income limits and verification
- Residency requirements
- Age restrictions
- Documentation needed
- Any barriers to access

Provide clear guidance on eligibility and what documents to bring."""
