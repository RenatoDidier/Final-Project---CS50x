# CS50x - Final Project - Web App - 4SHARE

The final project is a web app where users can store in an organized and a structured way important things watched or read. I wanted to do this type of project, because I think the market lacks a site that organizes information that we think is important in this way. Living in this era where information is sometimes suffocating, it is essential that we have more and more technologies that help us with the storage and visualization of this information in an efficient way. It is essential that we always seek new information to improve as an individual, but let us not forget those that have already made us better.

Technologies used:
- Python (Flask)
- JavaScript (JQuery)
- Sqlite
- CSS (Bootstrap & DataTable)
- HTML

## How the web app works?

The site is extremely easy and intuitive to use. When the user has not yet created the account, the only interaction he will have from the site will be viewing the "ranking list" session. There he will see the tables that other users have chosen to make their table publicly available and at the mercy of a vote.

After creating the account on the platform, the user releases the tool to create his own table and to interact in the voting of the tables that are publicly available.
Creating a new table is extremely easy and intuitive. There are buttons available on the "mylist" page where the user can choose to create a new table, or, if he already has one, add new information to an existing table. If he is interested in making it available for public voting, he only needs to activate the "ranking mode".

I really missed a similar idea, especially when I started looking for the best way to learn to program. The internet is flooded with different paths in which we don't know what the outcome of each one will be. If there had been a user who had gone through this situation and had used this site to archive their entire journey, and in addition, after publishing their journey in table format, an entire community had voted to show validation on that particular path , it would be a great time saver in research and security in the choice made to follow this user's guidelines. Not only that. Also imagine other users who have a certain credibility in life posting tables about the best books, documentaries, movies etc. It's a great platform for that.  

## Files
- app.py<br>Here's most of the code. I used the Flask framework to be able to make the many different connections that the site has. From the creation of a new account, to the ranking system between the tables. The association of this part with the javascript files ensured a very dynamic user experience.
- helpers.py<br>Here you will only have one function in which you will check if the user is logged into an account or not. If he is not, he will be unable to use many features.
- (folder) templates<br>All html files
- createRow.js<br>This file is connected with a button. Whenever someone clicks this button, all the fields that are needed to fill a row of table information will be generated. This information is sent to "app.py" where it makes a direct connection to our database.
- createColumn.js<br>Esse arquivo está conectado com um botão. Sempre que alguém clica nesse botão, será gerado todos os campos que são necessários para preencher uma nova tabela para o usuário. Essa informação é enviada para o "app.py" no qual faz a conexão direta com o nosso banco de dados.
- dropDown.js<br>This is a function responsible for the correct functioning of the "dropdown" buttons on the site.
- sortTable.js<br>Essa é a função responsável que garante a ativação do framework DataTable, no qual fornece o recurso de sorteamento da tabela.

## Possible improvements

- It is possible to store images
- The user has more control in each information that he want to appear
- Users can generate columns as their need
- Connect the web app with e-mail
- If the user votes negative in a table, open a field for him to fill in the reason for the vote
- Create a session that has more interaction between users

## How to launch application

1. Install the last python version
2. Intall the last pimp version
3. With pimp, install flask, flask_session & cs50
4. Clone the code: `git clone https://github.com/RenatoDidier/project.git`
5. Once installed and clonned run two more commands: `export FLASK_APP=app.py` & `flask run`
6. You are ready to go!

