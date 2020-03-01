from Database.connDatabase import SQL

user= "postgres"
password = "061836" 
host = '192.168.1.16'
port = '5432'
database ="time3"

#test= SQL(user= "time3",password = "aFp5yEFVvGrfAu9c" , host = 'servidor-maratona,zeroglossa.com.br' , port = '5432' ,database ="time3")
test= SQL(user= user,password = password , host =host , port =  port  ,database =database)

query = "INSERT INTO public.convenio(conv_ans, conv_nome, con_data_update)VALUES ( '654654', 'Gosa Max', '2013-06-01')"

result = test.conn.execute(query)

#for i in result:
    # print(i)





