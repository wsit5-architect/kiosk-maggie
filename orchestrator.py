Overview





import json
import logging
from google.antigravity import Agent, LocalAgentConfig, types
from robot.reachy_controller import reachy
from agents.get_process_agent import get_process_agent_tools
logger = logging.getLogger(__name__)
def send_ticket_email(issue_details: str, user_profile: str) -> str:
    """Sends a structured support email to servicedesk@georgefox.edu.
    
    Args:
        issue_details: Description of the problem.
        user_profile: The validated user profile from get_process_agent.
    """
    logger.info(f"[SMTP] Sending ticket for {user_profile} regarding: {issue_details}")
    return "Ticket sent successfully to servicedesk@georgefox.edu"
def search_internal_wiki(query: str) -> str:
    """Searches the internal knowledge base at data_wiki.georgefox.edu.
    
    Args:
        query: The technical or institutional data question.
    """
    logger.info(f"[WIKI] Searching data_wiki.georgefox.edu for: {query}")
    return "Wiki Search Results: The library hours are 8AM to 10PM."
def scrape_campus_info(query: str) -> str:
    """Scrapes campus info restricted to *.georgefox.edu domain.
    
    Args:
        query: Generic campus question.
    """
    logger.info(f"[SCRAPER] Scraping *.georgefox.edu for: {query}")
    return "Campus Info Results: The cafeteria is open."
async def capture_id_photo(user_profile: str) -> str:
    """Captures a new ID photo using Reachy's camera.
    
    Args:
        user_profile: The validated user profile.
    """
    logger.info(f"[CAMERA] Capturing ID photo for {user_profile}")
    photo_file = await reachy.capture_photo()
    return f"Photo captured successfully and bound to profile. File: {photo_file}"
orchestrator_tools = [
    send_ticket_email,
    search_internal_wiki,
    scrape_campus_info,
    capture_id_photo,
]
def get_agent_config():
    # Merge tools from the get_process_agent (subagent tasks) and main orchestrator
    all_tools = orchestrator_tools + get_process_agent_tools
    
    return LocalAgentConfig(
        tools=all_tools,
        system_instructions=(
            "You are 'Maggie', the IT Service Desk Kiosk for George Fox University. "
            "You control a Reachy Mini robot. "
            "Your main tasks are: "
            "1. Identify the user using the Active Directory/Local fallback tools. "
            "2. File IT tickets. "
            "3. Look up wiki info on data_wiki.georgefox.edu. "
            "4. Answer campus questions from *.georgefox.edu. "
            "5. Capture ID photos using the camera tool. "
            "Always be helpful and concise."
        )
    )
