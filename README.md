# GitHub-lister
# GitHub-lister
A server that returns to the client list of specified user's repositories or total stargazers count

Firstly you have to ensure you have installed Python3 and Flask framework. If you don't have Flask, type into your shell:
>pip install Flask

Then you have to move into directory where you have put the file. Than you may run it through the shell:
>python server.py

Now, to use the running program you may use curl program. 

To list user repositories, type in shell:
>curl http://localhost:5000/list?user=USERNAME

To get sum of stars of an user, type in shell:
>curl http://localhost:5000/star?user=allegro

In the future, the project can be expanded with:
* POST operation support
* a toggle which will determine if the server should list repositories in lexicographic order
* listing repositories of organisations, not only users
* a website that will would user-friendly present data gotten from the server
