from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models1.schemas import Operation
import secrets
import pika

app = FastAPI()
router = APIRouter()

# Função para gerar uma chave de sessão única
def generate_session_key():
    return secrets.token_urlsafe(32)

#
# login
#

@router.post("/login")
def login_usuario(usuario: str, senha: str):
    app.state.mensagem = ""
    def callback(ch, metodos, props, body):
      print(f"Mensagem Recebida: {body}")
      conexao.close()
      app.state.mensagem = body
      return 
    
    parametros_conexao = pika.ConnectionParameters('localhost')
    conexao = pika.BlockingConnection(parametros_conexao)
    
    canal = conexao.channel()
    canal.queue_declare(queue='fila0')
    canal.queue_declare(queue='fila1')

    nome = Operation(id= 1, usuario= usuario, senha= senha)
    mensagem = nome.model_dump_json()
    canal.basic_publish(exchange="",routing_key = 'fila0', body=mensagem)
    print(f'Mensagem enviada: {mensagem}')

    canal.basic_consume(queue='fila1', auto_ack=True, on_message_callback=callback)
    print("Aguardando Resposta do Banco de Dados")
    canal.start_consuming()

    return app.state.mensagem

#
# logout
#

@router.post("/logout")
def logout():
    app.state.mensagem = ""
    def callback(ch, metodos, props, body):
      print(f"Mensagem Recebida: {body}")
      conexao.close()
      app.state.mensagem = body
      return 
    
    parametros_conexao = pika.ConnectionParameters('localhost')
    conexao = pika.BlockingConnection(parametros_conexao)
    canal = conexao.channel()
    canal.queue_declare(queue='fila0')
    canal.queue_declare(queue='fila1')

    nome = Operation(id= 2)
    mensagem = nome.model_dump_json()
    canal.basic_publish(exchange="",routing_key = 'fila0', body=mensagem)
    print(f'Mensagem enviada: {mensagem}')

    canal.basic_consume(queue='fila1', auto_ack=True, on_message_callback=callback)
    print("Aguardando Resposta do Banco de Dados")
    canal.start_consuming()

    return app.state.mensagem

#
# validar sessão
#

@router.get("/validate-session")
def validate_session(chave_sessao: str):
    app.state.mensagem = ""
    def callback(ch, metodos, props, body):
      print(f"Mensagem Recebida: {body}")
      conexao.close()
      app.state.mensagem = body
      return 
    
    parametros_conexao = pika.ConnectionParameters('localhost')
    conexao = pika.BlockingConnection(parametros_conexao)
    canal = conexao.channel()
    canal.queue_declare(queue='fila0')
    canal.queue_declare(queue='fila1')

    nome = Operation(id= 3)
    mensagem = nome.model_dump_json()
    canal.basic_publish(exchange="",routing_key = 'fila0', body=mensagem)
    print(f'Mensagem enviada: {mensagem}')
    
    canal.basic_consume(queue='fila1', auto_ack=True, on_message_callback=callback)
    print("Aguardando Resposta do Banco de Dados")
    canal.start_consuming()

    return app.state.mensagem

app.include_router(router)
