from asyncio import sleep

import asyncio
import json
import os
import sys
import threading
import time
from fastapi import FastAPI, Request, Response

from fastapi.responses import StreamingResponse

from loguru import logger
from config import Config

from route.hello import Hello
from route.llm import Llm
from services.ChatBotMemory import ChatBotMemory
from services.ChatgptOriginal import ChatgptOriginal
from services.AgentFunctionChat import AgentFunctionChat
from services.llma import LLma
from services.ThreadedGenerator import ThreadedGenerator
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


logger.add('logs/app.log', rotation='500 MB', retention='1 days',
           level='INFO', encoding="utf-8", enqueue=True, compression="tar.gz")
logger.info('server init ')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route('/streamTest')
async def streamed_response():
    def generate():
        yield 'Hello asdf'+"\r\n"
        time.sleep(1)
        yield 'asdf'+"\r\n"
        time.sleep(1)
        yield '!'+"\r\n"
    return StreamingResponse(generate(), media_type='text/stream')


@app.api_route('/hello', methods=['GET', 'POST'])
async def hello(request: Request):
    logger.info('This is an info message')
    if request.method == 'POST':
        return Hello.post()
    else:
        return Hello.get()
    
@app.api_route('/chatgpt/chat', methods=['GET', 'POST'])
async def chatgptChat(request: Request):
    
    if request.method == 'POST':
        return ChatgptOriginal.chat(content,1)
    else:
        content = request.query_params["content"]
        user_id = request.query_params["user_id"]
        return ChatBotMemory().chat(content,user_id)


@app.api_route('/chatgpt/chatStream', methods=['GET', 'POST'])
async def chatgptChatStream(request: Request):
    if request.method == 'POST':
        return streamingresponse(ChatgptOriginal.streamChat(content,1), media_type='text/stream')
    else:
        content = request.query_params["content"]
        user_id = request.query_params["user_id"]
        #return streamingresponse(Chatgpt.streamChat(content,1), media_type='text/stream')
        return StreamingResponse(ChatBotMemory.streamChat(content, user_id), media_type='text/stream')

@app.api_route('/llm/chat', methods=['GET', 'POST'])
async def llmChat(request: Request, q:str=None):
    print("method:",request.method)
    if request.method == 'POST':
        content_type = request.headers["Content-Type"]
        if content_type == "application/json":
            json_body = await request.body()
            print("json_body:", json_body)
            body = json.loads(json_body)
            # 如果参数校验失败，则返回 400 状态码和错误信息
            return Llm.chat(body["content"])
    else:
        content = request.query_params["content"]

        print(content)
        return Llm.chat(content)


@app.api_route('/llm/chatStream', methods=['GET', 'POST'])
async def chatStream(request: Request):
    if request.method == 'POST':
        content_type = request.headers["Content-Type"]
        if content_type == "application/json":
            json_body = await request.body()
            print("json_body:", json_body)
            body = json.loads(json_body)
            return StreamingResponse(Llm.chatStream(body["content"]), media_type="text/event-stream")
    else:
        content = request.query_params["content"]
        return StreamingResponse(Llm.chatStream(content), media_type="text/event-stream")


# 生成索引
@app.api_route('/llm/create-index', methods=['GET', 'POST'])
async def llmCreateIndex(request: Request):
    if request.method == 'POST':

        return Llm.createIndox()
    else:
        return Llm.createIndox()
    
@app.api_route('/knowbox/chat', methods=['GET', 'POST'])
async def knowChat(request: Request, q:str=None):
    print("method:",request.method)
    if request.method == 'POST':
        content_type = request.headers["Content-Type"]
        if content_type == "application/json":
            json_body = await request.body()
            print("json_body:", json_body)
            body = json.loads(json_body)
            # 如果参数校验失败，则返回 400 状态码和错误信息
            return AgentFunctionChat.askQuestionChroma(body["content"])
    else:
        content = request.query_params["content"]
        user_id = request.query_params["user_id"] if "user_id" in request.query_params else "11234"
        print(content)
        print(user_id)
        return AgentFunctionChat().askQuestionChroma(user_id,content)


    
@app.api_route('/knowbox/chatStream', methods=['GET', 'POST'])
async def knowChatStream(request: Request, q:str=None):
    print("method:",request.method)
    if request.method == 'POST':
        content_type = request.headers["Content-Type"]
        if content_type == "application/json":
            json_body = await request.body()
            print("json_body:", json_body)
            body = json.loads(json_body)
            # 如果参数校验失败，则返回 400 状态码和错误信息
            return AgentFunctionChat.askQuestionChroma(body["content"])
    else:
        content = request.query_params["content"]
        user_id = request.query_params["user_id"] if "user_id" in request.query_params else "11234"

        print(content)
        return StreamingResponse(AgentFunctionChat().askQuestionChromaStream(user_id,content), media_type="text/event-stream")




if __name__ == '__main__':
    logger.info('app RUN')
