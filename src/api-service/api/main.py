from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.schema import HumanMessage
from langchain.prompts.example_selector import LengthBasedExampleSelector
from api import examples
from google.cloud import aiplatform
from pydantic import BaseModel
import json
import os
import random

GCP_PROJECT = os.getenv('GCP_PROJECT')
ENDPOINT_ID = os.getenv('ENDPOINT_ID')
REGION = os.getenv('REGION')

ENDPOINT_NAME = (f"projects/{GCP_PROJECT}/locations/{REGION}/endpoints/{ENDPOINT_ID}")

with open('api/processed-leetcode.json', 'r') as file:
    question_bank = json.load(file)

easy_items = []
medium_items = []
hard_items = []
all_items = []

for index, question in enumerate(question_bank):
    question_with_index = (index, question)  # Tuple of index and question
    all_items.append(question_with_index)
    if question['difficulty'] == 'Easy':
        easy_items.append(question_with_index)
    elif question['difficulty'] == 'Medium':
        medium_items.append(question_with_index)
    else:
        hard_items.append(question_with_index)

question_index = None

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryModel(BaseModel):
    prompt: str

@app.get("/health-check")
async def healthcheck():
    return {"Hello": "World"}

@app.get("/get-interview-question")
async def getInterviewQuestion(difficulty: str = Query(None, enum=["Easy", "Medium", "Hard"])):
    if difficulty == "Easy":
        question_list = easy_items
    elif difficulty == "Medium":
        question_list = medium_items
    elif difficulty == "Hard":
        question_list = hard_items
    else:
        question_list = all_items

    global question_index
    question_index, item = random.choice(question_list)

    return {
        'statusCode': 200,
        'body': item['question']
    }

@app.get("/get-question-solution")
async def getQuestionSolution():
    return {
        'statusCode': 200,
        'body': question_bank[question_index]['python_sol']
    }

@app.get("/get-question-explanation")
async def getQuestionExplanation():
    return {
        'statusCode': 200,
        'body': question_bank[question_index]['explanation']
    }

@app.post("/query-tech")
async def queryTech(query: QueryModel):
    prompt = query.prompt

    endpoint = aiplatform.Endpoint(ENDPOINT_NAME)

    instances = [
        {
            "prompt": prompt,
            "max_tokens": 200,
            # "temperature": 0,
            # "top_p": 1.0,
            # "top_k": 10,
        },
    ]

    resp = endpoint.predict(instances=instances)
    
    return {
        'statusCode': 200,
        'body': resp.predictions[0]
    }

@app.post("/query-chat")
async def queryChat(query: QueryModel):
    prompt = query.prompt

    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

    formatted_template = '''{example_query} {example_response}'''
    prompt_tmplt = PromptTemplate(
        input_variables=["example_query", "example_response"],
        template=formatted_template,
    )

    prompt_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=prompt_tmplt
    )

    print()
    print('prompt_selector', prompt_selector)
    print()

    dynamic_prompt = FewShotPromptTemplate(
        example_selector=prompt_selector,
        example_prompt=prompt_tmplt,
        prefix="""As a software engineering interview chatbot, I am here to present you with coding challenges, algorithmic puzzles, and system design questions. I will provide solutions and explanations to these problems. 

        REQUIREMENTS:
        - The response will include a clear solution to the presented problem.
        - Solutions for coding problems will be in Python
        - Explanations for algorithmic puzzles will include both the approach and the reasoning behind it and their computational efficieny.
        - System design answers will outline key components and their interactions.
        """,
        suffix="\nPlease enter your software engineering interview question below:\n\n{input}\n",
        input_variables=["input"],
        example_separator="\n\n",
    )

    final_prompt = dynamic_prompt.format(input=f'{prompt}')

    print()
    print('final_prompt')
    print()
    print(final_prompt)
    print()

    resp = llm([HumanMessage(content=final_prompt)])

    print(resp)
    
    return {
        'statusCode': 200,
        'body': resp.content
    }
