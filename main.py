from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

#Carregando o "cofre", no caso, é onde eu coloquei minha chave do banco de dados, que é a URL do Neon. O load_dotenv() vai ler o arquivo .env e colocar as variáveis de ambiente disponíveis para o Python usar.
load_dotenv()

#Aí aqui eu tô pegando a URL do banco de dados que tá guardada na variável de ambiente DATABASE_URL e colocando ela na variável URL_DO_BANCO, que é a que eu vou usar pra tentar conectar com o Neon.
URL_DO_BANCO = os.getenv("DATABASE_URL")

app = FastAPI()


#Isso basicamente eu tô dizendo pro Python que eu quero criar um modelo de dados chamado UsuarioNovo, que tem três campos: nome, email e senha. Todos esses campos são do tipo string. Esse modelo é útil pra quando eu quiser receber dados de um usuário novo, por exemplo, em uma rota de cadastro. Ele vai me ajudar a validar os dados que o usuário enviar e garantir que eles tenham o formato certo antes de eu tentar usar esses dados no meu sistema.
class UsuarioNovo(BaseModel):
    nome: str
    email: str
    senha: str


@app.post("/usuarios")
def criar_usuario(usuario: UsuarioNovo):
    try:
        #aqui eu tô abrindo uma conexão com o banco usando a URL que eu peguei do .env. Se a conexão abrir, eu fecho ela rapidinho só pra não gastar recurso, e aí eu retorno uma mensagem de sucesso. Se der algum erro, ele vai pular pra parte do except e me mostrar qual foi o erro.
        conexao = psycopg2.connect(URL_DO_BANCO)
        cursor = conexao.cursor() #Esse cursor é o "carteiro" que vai levar as informações do meu código pro banco de dados. Ele é responsável por executar os comandos SQL que eu quiser usar pra interagir com o banco.
        
        #Esse é o comando SQL que eu quero executar pra inserir um novo usuário na tabela "usuarios". O %s é um placeholder que vai ser substituído pelos valores reais do nome, email e senha do usuário. O RETURNING id é uma parte importante porque ele me diz pra retornar o ID do usuário que acabou de ser inserido, assim eu posso usar esse ID pra outras coisas depois, tipo mostrar pro usuário ou usar em outras partes do meu sistema.
        comando_sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s) RETURNING id;"
        valores = (usuario.nome, usuario.email, usuario.senha)

        cursor.execute(comando_sql, valores) #Aqui eu tô dizendo pro cursor executar o comando SQL que eu escrevi, e passar os valores do nome, email e senha do usuário pra substituir os %s no comando.
        novo_id = cursor.fetchone()[0] #Esse fetchone server pra pegar o resultado do comando SQL que eu acabei de executar. Como eu usei RETURNING id, ele vai me retornar o ID do novo usuário que foi inserido, e eu pego esse ID e guardo na variável novo_id.

        conexao.commit() #Esse cara vai bater o martelo e confirmar que as mudanças que eu fiz no banco de dados (inserir o novo usuário) são permanentes. Sem esse commit, as mudanças não seriam salvas de verdade no banco.

        cursor.close() #Tô fechando o cursor porque eu já terminei de usar ele pra executar o comando SQL, e é uma boa prática fechar o cursor quando a gente não precisa mais dele.
        conexao.close() #E aqui eu fecho a conexão com o banco de dados, porque eu já terminei tudo que precisava fazer.

        #Um adendo, o cursor é como se fosse um "carteiro" que leva as informações do meu código pro banco de dados. Ele é responsável por executar os comandos SQL que eu quiser usar pra interagir com o banco. Então, quando eu quero fazer alguma coisa no banco, tipo inserir um novo usuário, eu uso o cursor pra enviar esse comando pro banco e ele cuida de tudo pra mim.

        return {"status": "sucesso", "mensagem": f"Usuário {usuario.nome} criado com ID {novo_id}"} #Aqui eu tô retornando uma resposta pra quem chamou essa rota, dizendo que o usuário foi criado com sucesso e mostrando o nome do usuário e o ID que ele recebeu no banco de dados.

    except Exception as erro:
        return {"status": "erro", "mensagem": f"Deu ruim ao criar o usuário: {erro}"} #Se der algum erro durante esse processo todo, ele vai pular pra cá e me mostrar uma mensagem de erro com o que aconteceu.
    



#Estrutura da tabela "obras" no banco de dados
class ObraNova(BaseModel):
    usuario_id: int
    titulo: str
    categoria: str
    status: str
    nota: int

#Isso serve basicamente para criar uma nova obra no banco de dados. 
@app.post("/obras")
def criar_obra(obra: ObraNova):
    try:
        conexao = psycopg2.connect(URL_DO_BANCO)
        cursor = conexao.cursor()
        
        comando = "INSERT INTO obras (usuario_id, titulo, categoria, status, nota) VALUES (%s, %s, %s, %s, %s) RETURNING id;"
        valores = (obra.usuario_id, obra.titulo, obra.categoria, obra.status, obra.nota)
        
        cursor.execute(comando, valores)
        nova_id = cursor.fetchone()[0]
        conexao.commit()
        
        cursor.close()
        conexao.close()
        
        return {"status": "sucesso", "mensagem": f"Obra '{obra.titulo}' salva com ID {nova_id}"}
    except Exception as erro:
        return {"status": "erro", "mensagem": f"Erro ao salvar a obra: {erro}"}