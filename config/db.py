from config.setup import app
from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = "uprevol.cs3vggqcgesi.ap-south-1.rds.amazonaws.com"
app.config['MYSQL_USER'] = "admin"
app.config['MYSQL_PASSWORD'] = "Uprevol1234"
app.config['MYSQL_DB'] = "uprevol"

mysql = MySQL(app)
