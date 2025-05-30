from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

import os
from dotenv import load_dotenv

load_dotenv()

class LLamaLLMChain:
    def __init__(self):
        self.API_KEY=os.getenv('GROQ')
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=self.API_KEY,
            model_name="llama-3.3-70b-versatile"
        )
    
    def extract_job_details(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {pg_data}

            ### INSTRUCTUION
            The scrapped text is from the job page of LinkedIn. Your task is to extract the following details from the job posting and return them in a JSON format with the keys:
            `job_title`, `role`, `description`, `skills`, `experience`, `tasks`.
            Only return the valid JSON format.

            ### VALID JSON (NO PREAMBLE)
            """
        )
        chain_extract = prompt_extract | self.llm # getting a prompt and passing it to the llm
        try:
            res = chain_extract.invoke(input={'pg_data': cleaned_text})
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException('Context too big. Unable to parse decsription')
        
        return res if isinstance(res, list) else [res]
    
    def write_email(self, jobs, tasks, links):
        prompt_email = PromptTemplate.from_template(
                """
                ### JOB DESCRIPTION:
                {job_desc}
                and TASKS:
                {job_tasks}
                ### INSTRUCTION:
                You are Annie Chakraborty, an MS Computer Science student at the University of Stuttgart. As a CS student you have gained several skills
                in the fields of full stack web development, python programming, API development, mobile apps development, and AI/ML model development.
                
                Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
                in fulfilling their needs.
                Also add the most relevant ones from the following links to showcase your portfolio: {links}
                Remember you are Annie, MS student in University of Stuttgart. 
                Do not provide a preamble.
                ### EMAIL (NO PREAMBLE):
                
                """
            )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_desc": str(jobs), 'job_tasks': tasks, "links": links})
        return res.content