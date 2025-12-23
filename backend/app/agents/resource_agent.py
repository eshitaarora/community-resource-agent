"""
LangChain AI Agent for resource navigation
Handles multi-turn conversations with tool integration
"""

from typing import List, Dict, Any, Optional
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.agents.llm_config import get_llm, SYSTEM_PROMPT
from app.agents.tools import AGENT_TOOLS
from app.db.models import ChatMessage
from app.db.database import SessionLocal
import logging
import json

logger = logging.getLogger(__name__)


class ResourceAgent:
    """
    AI Agent for helping users find community resources.
    Uses LangChain with tool-calling capabilities.
    """
    
    def __init__(self):
        """Initialize the agent with LLM and tools"""
        self.llm = get_llm()
        self.tools = AGENT_TOOLS
        self._setup_agent()
    
    def _setup_agent(self):
        """Setup the LangChain agent with prompt and tools"""
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create agent executor with memory
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=15,
            early_stopping_method="force"
        )
    
    def process_message(
        self,
        user_message: str,
        user_id: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return agent response.
        
        Args:
            user_message: The user's input message
            user_id: Unique identifier for the user
            chat_history: Previous messages in conversation
            user_context: Additional user context (location, needs, eligibility info)
        
        Returns:
            Agent response with message, tools used, and recommendations
        """
        try:
            # Build chat history for context
            messages: List[BaseMessage] = []
            if chat_history:
                for msg in chat_history:
                    if msg["role"] == "human":
                        messages.append(HumanMessage(content=msg["content"]))
                    else:
                        messages.append(AIMessage(content=msg["content"]))
            
            # Add user context to the initial message if provided
            input_message = user_message
            if user_context:
                context_str = self._format_user_context(user_context)
                input_message = f"{context_str}\n\nUser message: {user_message}"
            
            # Run the agent
            response = self.agent_executor.invoke({
                "input": input_message,
                "chat_history": messages,
                "agent_scratchpad": ""
            })
            
            # Extract the output
            agent_message = response.get("output", "")
            
            # Save to database
            self._save_message(
                user_id=user_id,
                user_message=user_message,
                agent_response=agent_message,
                tools_used=response.get("intermediate_steps", [])
            )
            
            return {
                "success": True,
                "message": agent_message,
                "tools_used": self._extract_tool_names(response.get("intermediate_steps", [])),
                "user_id": user_id
            }
        
        except Exception as e:
            logger.error(f"Error processing message for user {user_id}: {e}")
            error_message = "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
            self._save_message(user_id, user_message, error_message, [])
            
            return {
                "success": False,
                "message": error_message,
                "error": str(e),
                "user_id": user_id
            }
    
    def _format_user_context(self, context: Dict[str, Any]) -> str:
        """Format user context into a readable string for the agent"""
        context_parts = []
        
        if context.get("location"):
            context_parts.append(f"Location: {context['location']}")
        
        if context.get("needs"):
            needs_list = ", ".join(context["needs"])
            context_parts.append(f"Needs: {needs_list}")
        
        if context.get("eligibility_info"):
            eligibility = context["eligibility_info"]
            if eligibility.get("income_level"):
                context_parts.append(f"Income Level: {eligibility['income_level']}")
            if eligibility.get("age"):
                context_parts.append(f"Age: {eligibility['age']}")
        
        if context.get("accessibility_needs"):
            accessibility = ", ".join(context["accessibility_needs"])
            context_parts.append(f"Accessibility Needs: {accessibility}")
        
        if context_parts:
            return "User Context:\n" + "\n".join(context_parts)
        return ""
    
    def _extract_tool_names(self, intermediate_steps: List[tuple]) -> List[str]:
        """Extract tool names from intermediate steps"""
        tools_used = []
        try:
            for step in intermediate_steps:
                if step and len(step) > 0:
                    tool_name = step[0].tool if hasattr(step[0], 'tool') else str(step[0])
                    tools_used.append(tool_name)
        except Exception as e:
            logger.debug(f"Could not extract tool names: {e}")
        
        return list(set(tools_used))  # Remove duplicates
    
    def _save_message(
        self,
        user_id: str,
        user_message: str,
        agent_response: str,
        tools_used: List[tuple]
    ):
        """Save conversation to database for audit and learning"""
        db = SessionLocal()
        try:
            tool_names = self._extract_tool_names(tools_used)
            
            message = ChatMessage(
                user_id=user_id,
                message=user_message,
                response=agent_response,
                agent_tools_used=tool_names
            )
            db.add(message)
            db.commit()
        except Exception as e:
            logger.error(f"Error saving message to database: {e}")
            db.rollback()
        finally:
            db.close()
    
    def get_conversation_history(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversation history for a user.
        
        Args:
            user_id: User identifier
            limit: Number of recent messages to retrieve
        
        Returns:
            List of recent messages
        """
        db = SessionLocal()
        try:
            messages = (
                db.query(ChatMessage)
                .filter(ChatMessage.user_id == user_id)
                .order_by(ChatMessage.timestamp.desc())
                .limit(limit)
                .all()
            )
            
            return [
                {
                    "id": msg.id,
                    "user_message": msg.message,
                    "agent_response": msg.response,
                    "tools_used": msg.agent_tools_used or [],
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in reversed(messages)  # Reverse to get chronological order
            ]
        except Exception as e:
            logger.error(f"Error retrieving conversation history: {e}")
            return []
        finally:
            db.close()


# Global agent instance
_agent_instance = None


def get_agent() -> ResourceAgent:
    """Get or create the global agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = ResourceAgent()
    return _agent_instance
