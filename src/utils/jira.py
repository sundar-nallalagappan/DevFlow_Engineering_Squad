from jira import JIRA
import json
import os


class JiraHandler:
    def __init__(self, server_url, email, api_token):
        self.jira = JIRA(server=server_url,
                         basic_auth=(email, api_token))
        
    def find_open_issues(self, project_key='Sales Dashboard'):
        """Finds all unresolved tickets in a specific project."""
        print('find_open_issues')
        # JQL: Project is X AND Status is not Done
        
        myself = self.jira.myself()
        print(f"✅ Jira Connection SUCCESS! Logged in as: {myself['displayName']}")
        
        jql_query = f'project = "{project_key}" AND statusCategory != Done ORDER BY priority DESC'
        print('jql_query:', jql_query)
        try:
            # maxResults=5 
            issues = self.jira.search_issues(jql_query, maxResults=5)
            
            result_list = {}
            for issue in issues:
                priority_name = issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else "None"
                # Format: "Ticket: SALES-101 | Priority: Highest | Summary: ..."
                # This format makes it very easy for the LLM to parse.
                result_list[issue.key] = {'Priority': priority_name, 'Summary': issue.fields.summary, 'description':issue.fields.description}
                
            print('result_list:', result_list)
            if not result_list:
                return json.dumps({'jira':"No open tickets found"})
            
            return json.dumps(result_list)
            
        except Exception as e:
            return json.dumps({'status': f"Error posting comment: {str(e)}"})
        
    def get_ticket_details(self, ticket_id):
        """
        Get Jira ticket details for the provided ticket ID
        """    
        print('get_ticket_details')
        try:
            issue = self.jira.issue(ticket_id)
            return json.dumps({
                "id": ticket_id,
                "summary": issue.fields.summary,
                "description": issue.fields.description,
                "status": issue.fields.status.name
            })
        except Exception as e:
            print("Error raised")
            return json.dumps({'status': f"Error posting comment: {str(e)}"})

    def post_comment(self, ticket_id, message):
        """Function to post comments in the JIRA ticket for the provided ticket ID"""
        print('post_comment')
        print('ticket_id:', ticket_id)
        print('message:', message)
        try:
            self.jira.add_comment(ticket_id, message)
            return json.dumps({'status': f"Successfully commented on {ticket_id}"})
        except Exception as e:
            return json.dumps({'status': f"Error posting comment: {str(e)}"})
        
    def update_ticket_status(self, ticket_id, status_name):
        """
        Useful for moving a ticket to a new workflow stage.
        
        Args:
            ticket_id: Ticket ID or ticket key to filter the exact Jira ticket
            status name: 'TO DO', 'IN PROGRESS', 'IN REVIEW', 'DONE'

        Returns:
            Dictionary with success/failure status 
        """
        try:
            issue = self.jira.issue(ticket_id)
            
            # 1. Get all possible transitions for this ticket
            transitions = self.jira.transitions(issue)
            
            # 2. Find the ID associated with the status name
            transition_id = None
            for t in transitions:
                if t['name'].lower() == status_name.lower():
                    transition_id = t['id']
                    break
            
            if transition_id:
                # 3. Perform the transition (Status change ONLY)
                self.jira.transition_issue(issue, transition_id)
                
                return json.dumps({
                    "status": "success", 
                    "message": f"Ticket {ticket_id} successfully moved to '{status_name}'."
                })
            else:
                allowed = [t['name'] for t in transitions]
                return {
                    "status": "error", 
                    "message": f"Cannot move to '{status_name}'. Allowed statuses: {allowed}"
                }
                
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
        
        