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
    
    