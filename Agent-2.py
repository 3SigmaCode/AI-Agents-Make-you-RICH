#Support Triage

from typing import TypedDict, Literal
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# --- 1. DEFINE THE STATE ---
class TicketState(TypedDict):
    ticket_id: str
    user_query: str
    draft_response: str
    confidence_score: float

# --- 2. THE GRADER MODEL ---
class ConfidenceGrade(BaseModel):
    """Validator for the AI's draft."""
    score: float = Field(description="Confidence score between 0.0 and 1.0")
    reasoning: str = Field(description="Why is this score given?")

# --- 3. THE NODES ---
def drafter_node(state: TicketState):
    # Logic to draft a reply from FAQ
    # (Mocked for architecture demo)
    return {"draft_response": "Here is your refund link..."}

def grader_node(state: TicketState):
    """
    The Critical Loop: Checks if the draft is accurate.
    """
    model = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    structured_llm = model.with_structured_output(ConfidenceGrade)
    
    # In production, you would pass the actual Policy Docs here
    grade = structured_llm.invoke(f"Rate this answer: {state['draft_response']}")
    
    return {"confidence_score": grade.score}

# --- 4. THE DECISION DIAMOND (The Brain) ---
def route_ticket(state: TicketState) -> Literal["send_email", "escalate"]:
    """
    Determines if we automate or escalate.
    """
    # THIS IS WHAT YOU SELL TO CLIENTS:
    if state['confidence_score'] > 0.90:
        return "send_email"
    else:
        return "escalate"

# --- 5. THE MOCKED ACTIONS ---
def send_email_node(state: TicketState):
    print(f"✅ EMAIL SENT for Ticket {state['ticket_id']}")
    # TODO: Replace with Gmail/SendGrid API
    return

def escalate_node(state: TicketState):
    print(f"⚠️ ESCALATED Ticket {state['ticket_id']} to Human Slack Channel")
    # TODO: Replace with Slack/Zendesk API
    return

# --- 6. BUILD THE GRAPH ---
workflow = StateGraph(TicketState)
workflow.add_node("drafter", drafter_node)
workflow.add_node("grader", grader_node)
workflow.add_node("send_email", send_email_node)
workflow.add_node("escalate", escalate_node)

workflow.set_entry_point("drafter")
workflow.add_edge("drafter", "grader")
workflow.add_conditional_edges(
    "grader",
    route_ticket,
    {
        "send_email": "send_email",
        "escalate": "escalate"
    }
)

app = workflow.compile()