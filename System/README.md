# The main structure of this project
functionalities are divided into System, Recommendation, Discussion and Writing
tips: Before run, ensure that you have already executed "python manage.py shell < default.py" in the command line
## System
welcome（TODO)  
register  
login  
user page  
## Account
### model: PlatformUser

### web page: Account.register
### web page: Account.login
### web page: Account.user_page

## Recommendation
offer recommendations to users based on their behaviors and other info  
recieving results from model ML  
### model: Book  
### model: Topic
## Discussion
discussion zone & groups  
### discussion zone
showing groups of different topics or books  
### model: discGroup
members of the group can post comments about its topic or book  
### model: discRecord
key design for discussion zone  
allowing group members to post comments, reply to other comments and give likes  
### web page: Discussion.index  
displaying groups  
### web page: Discussion.detail  
showing discussions after entering a group  
### web page: Discussion.register
register a discgroup
## Writing
post pencrafts and comment pencrafts   
### model: Pencraft
main body of a pencraft created by a platformUser  
containing title(topic), description and chapters  
### model: Chapter
containing subtitle and content of a chapter  
### web page: Writing.index
displaying pencrafts  
### web page: Writing.pencraft
showing title, author, chapters and other information about a pencraft  
### web page: Writing.chapter
showing content of a chapter  
### web page: Writing.author
homepage of an author(also platformuser)  
showing previous pencrafts from this author  
author can start a new pencraft in this page  
### web page: Writing.update
author can chooose one of his/her previous pencrafts and update a new chapter  