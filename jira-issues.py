import csv
from jira import JIRA

# Define Jira server URL and authentication
jira_server = 'https://jira-service-mgt.atlassian.net'
jira_username = ''
jira_password = ''

jira = JIRA(server=jira_server, basic_auth=(jira_username, jira_password))

projects = jira.projects()
print("*** List of all Jira projects ***")

issues = []  # Define issues as an empty list

try:
    issues = jira.search_issues('project=SCRUM')
    print("Jira connection is successful.")
except Exception as e:
    print(f"Error connecting to Jira: {str(e)}")

# Specify the fields to extract
fields_to_extract = ["project", "issuetype", "timespent", "created", "updated", "assignee", "status"]

# Open a CSV file for writing
with open('/usr/share/grafana/jira_issues.csv', mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields_to_extract)
    writer.writeheader()  # Write the header row

    for issue in issues:
        issue_detail = jira.issue(issue)
        issue_data = {field: getattr(issue_detail.fields, field, '') for field in fields_to_extract}
        writer.writerow(issue_data)

print("Data has been written to jira_issues.csv")
