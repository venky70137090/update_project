# update_project
about createing tables:(sqlalchemy and cockroach_db)

create two tables named student , assignment.
student table contains the columns like id, name,reg_no.(id is primary key)
assignment table contains  the columns like id,topic,status,status_id.(id is primarykey , status_id is the foreign_key)
the relation between the two tables is one to many.
and if i delete the one id student table, then i need to delete the all related rows in the assignment table.
these about the creating the tables in using sqlalchemy not with sqllite or sql.

restapi:

restapi is to perfrom the http methods such as get,push,put,delete.
using these we want update the database or fetch the data from the database.

pytest:

using pytest ,we are checking weather these pytest operations performing as expected or not.


docker :
docker is used to containrise . my application  is  easy to share and use for others without version and enivorment conflict.

u can run these using
docker build -t charan(any name) .
docker run --name charan-container -p 6000:6000 charan


