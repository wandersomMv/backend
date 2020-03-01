from Database.connDatabase import SQL


test= SQL(user= "time3",password = "aFp5yEFVvGrfAu9c" , host = 'servidor-maratona,zeroglossa.com.br' , port = '5432' ,database ="time3")

query = "SELECT * FROM produto  ORDER BY id ASC LiMIT 100" \

result = test.conn.execute(query)

for i in result:
    print(i)