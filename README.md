
### LangChain OpenAI Knowbox

# 基于自有数据文件的chatgpt

## 使用技术

langchain+chatgpt+fastapi

## Usage

1.Install requirements

    ```
    pip3 install -r requirements.txt

    ```
2.copy `config-dev.py to` `config.py`

3.add openai key to `OPENAI_API_KEY`

DATA_PATH = './data'
./data 源数据文件

INDEX_JSON_PATH = './index.json'
向量存本地json文件，删除后自动重新加载data目录文件，到json文件

VECTOR_STORE_PATH = './vector_store_cache'
chroma本地向量数据库的文件路径，删除后自动重新加载data目录文件，到向量数据库

## 启动命令

uvicorn main:app --reload

## 向量数据库

### 本地向量文件

index.json

### Chorma

本地向量数据库

### Pinecone

Pinecone 是一个在线的向量数据库。所以，我可以第一步依旧是注册，然后拿到对应的 api key。<https://app.pinecone.io/>

免费版如果索引14天不使用会被自动清除。

然后创建我们的数据库：

Index Name：这个随意

Dimensions：OpenAI 的 text-embedding-ada-002 模型为 OUTPUT DIMENSIONS 为 1536，所以我们这里填 1536

Metric：可以默认为 cosine

## 相关接口

默认使用Chorma向量数据库

AgentToolStream
<http://127.0.0.1:8000/knowbox/chatStream?content=%E5%B0%8F%E7%9B%92%E6%98%AF%E4%BB%80%E4%B9%88&user_id=2298>

redisHistory ChromaSearchHistory
<http://127.0.0.1:8000/chatgpt/chatStream?content=%E5%86%8D%E4%B9%98%E4%BB%A53%E6%98%AF%E5%A4%9A%E5%B0%91&user_id=2233>

<http://127.0.0.1:8000/chatgpt/chat?content=%E6%88%91%E5%96%9C%E6%AC%A2%E7%9A%84%E8%BF%90%E5%8A%A8%E6%98%AF%E6%B8%B8%E6%B3%B3&user_id=12342>

## demo

h5/inxex.html

