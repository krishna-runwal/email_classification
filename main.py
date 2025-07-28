from loguru import logger
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
import re



# Add file-based logging
logger.add("logger_config.log", level="INFO", format="{time} | {level} | {message}")

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Define request models
class ClassifyRequest(BaseModel):
    email_content: str


class RewriteRequest(BaseModel):
    email_content: str
    tone: str


# Load prompts from external files
def load_prompt_template(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


# Initialize LLM from LangChain with Groq
model_name = os.getenv("GROQ_MODEL")
if not model_name:
    raise ValueError("GROQ_MODEL environment variable not set.")


llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=model_name
)



# Load the prompt templates
classification_template = load_prompt_template("prompts/classify_prompt.txt")
rewrite_template = load_prompt_template("prompts/rewrite_prompt.txt")



# Removing the Think Tags , as we are using the deepseek that's why it is neccessary to remove them form the response.
def remove_think_tags(text: str) -> str:
    # Remove <think>...</think> and any content in between
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)



# Endpoint to classify email
@app.post("/classify_email")
def classify_email(request: ClassifyRequest):
    if not request.email_content.strip():
        logger.warning("Received empty email_content in /classify_email")
        raise HTTPException(status_code=400, detail="Email content is empty")

    try:
        logger.info(f"Classify Request Received: {request.email_content}")
        prompt = PromptTemplate.from_template(classification_template).format(
            email_content=request.email_content
        )
        result = llm.invoke(prompt)
        result = result.content.strip()
        result = remove_think_tags(result) 
        logger.success(f"Classification Result: {result}")
        return {"category": result} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to rewrite email
@app.post("/rewrite_email")
def rewrite_email(request: RewriteRequest):
    if not request.email_content.strip():
        logger.warning("Received empty email_content in /rewrite_email")
        raise HTTPException(status_code=400, detail="Email content is empty")

    try:
        logger.info(f"Rewrite Request Received: {request.email_content} | Tone: {request.tone}")
        prompt = PromptTemplate.from_template(rewrite_template).format(
            email_content=request.email_content,
            tone=request.tone
        )
        result = llm.invoke(prompt)
        result = result.content.strip()
        result = remove_think_tags(result)
        logger.success("Email rewritten successfully.")
        return {"rewritten_email": result}
    except Exception as e:
        logger.error(f"Rewrite Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

