from Database.connDatabase import SQL,dados

user= "postgres"
password = "061836" 
host = '192.168.1.16'
port = '5432'
database ="time3"

test= SQL(user= "time3",password = "aFp5yEFVvGrfAu9c" , host = 'servidor-maratona,zeroglossa.com.br' , port = '5432' ,database ="time3")
# test= SQL(user= user,password = password , host =host , port =  port  ,database =database)

result = test.Select_dados_zero_glosa(dados(numero_guia='182524178'))

for i in result:
    print(i.__dict__)






