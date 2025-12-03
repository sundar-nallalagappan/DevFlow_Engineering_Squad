import os
import json

jira_api_token = os.getenv('JIRA_API_TOKEN')
#print('jira_api_token:', jira_api_token)
from src.utils.jira import JiraHandler

jira = JiraHandler(server_url="https://nsundar.atlassian.net", 
            email="nsundar.1990@gmail.com", 
            api_token=jira_api_token)

def search_tickets(project_key: str) -> dict:
    """
    Useful to find what work needs to be done. 
    Input should be the Project Key (e.g., 'CAP').
    Returns a list of Ticket IDs and Summaries.
    """ 
    """Looks up to JIRA board to find the open issues for the project

    Args:
        project_key: Input should be the Project Key (Ex: Sales-Dashboard)

    Returns:
        Dictionary with jira ticket details
        {'Ticket_Id': {'Priority': priority of ticket, 'Summary': summary of the issue, 'description': description of the issue}}
    """
    return jira.find_open_issues(project_key)


def read_ticket(ticket_id: str) -> dict:
    """
    Useful for reading the FULL description of a SPECIFIC ticket.
    
    Args:
        ticket_id: Ticket ID or ticket key to filter the exact Jira ticket

    Returns:
        Dictionary with Jira ticket details
        {"id": ticket_id, "summary": summary of the issue, "description": description of the issue, "status": status of the issue}
    """
    return jira.get_ticket_details(ticket_id)


def comment_on_ticket(ticket_id: str, message: str) -> dict:
    """
    Useful for posting a comment to a Jira ticket, to update the ticket with current status or to seek clarification.
    
    Args:
        ticket_id: Ticket ID or ticket key to filter the exact Jira ticket
        message  : comment/update to be posted in the ticket

    Returns:
        Dictionary with success/failure status 
    """
    return jira.post_comment(ticket_id, message)

def update_ticket_status(ticket_id: str, status: str) -> dict:
    """
    Useful for moving a ticket to a new workflow stage in JIRA Board.
    Does NOT add a comment. If an explanation is needed, use comment_on_ticket afterwards.
    
    Args:
        ticket_id: The Jira Ticket ID (e.g., 'CAP-101')
        status: The target status. Common values: 'TO DO', 'IN PROGRESS', 'IN REVIEW', 'DONE'.

    Returns:
        Dictionary with success or failure message.
    """
    return jira.update_ticket_status(ticket_id, status)

