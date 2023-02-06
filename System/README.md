# The main structure of this project
functionalities are divided into Account, Recommendation, Discussion and Writing  
# How to install this system  
1. download source code from our latest Github repo  
2. create virtual environment in accord with freeze.yml, then activate it  
3. open a shell from current folder, type command : 'cd System'  
4. type following commands to build your database: 'py manage.py makemigrations' & 'py manage.py migrate' & 'py manage.py shell < default.py'. Then you are supposed to see db.sqlite3 in System/  
5. add foader 'data/', then load book data in txt file 'book_info_all.txt'(only provided to group members now)  
6. type command in shell: 'py manage.py shell < loaddata.py'  
7. at last, type command 'py manage.py runserver' to run the server  
## Account
### model: PlatformUser
### web page: Account.register
### web page: Account.login
### web page: Account.user_page

## Recommendation
offer recommendations to users based on their behaviors and other info  
recieving results from model ML  
### model: Book  
### model: BookTag  
### model: SearchRecord
### web page: Recommendation.search  
you can search for a book in database by its title  
your search records will be kept for recommendation optimization  
### web page: Recommendation.book
basic information of a book is provided here   
## Discussion
discussion zone & groups  
### discussion zone
showing groups of different topics or books  
### model: discGroup
members of the group can post comments about its topic or book  
### model: discRecord
key design for discussion zone  
allowing group members to post comments, reply to other comments(TODO) and give likes(TODO)  
### web page: Discussion.index  
displaying groups  
### web page: Discussion.detail  
showing discussions after entering a group  
### web page: Discussion.register
user can register a discgroup on this web page  
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