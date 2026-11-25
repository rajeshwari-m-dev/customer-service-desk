from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field

class Tone_Evaluation(BaseModel):
    score:int = Field(description="Enter the score between 1 and 5")
    reasoning : str = Field(description="Explanation of the score")

def get_tone_chain(llm):

    parser = PydanticOutputParser(pydantic_object=Tone_Evaluation)

    prompt = PromptTemplate(
        template= """
You are a QA evaluator for customer support calls.
    Evaluate the agent's tone and empathy in the following transcript.

    Consider:
    - Did the agent acknowledge the customer's issue?
    -Was the tone polite and professional?
    -Did the agent show empathy?

    Transcript:
    {transcript}

    {format_instructions} """,
        input_variables= ["transcript"],
        partial_variables= {
            "format_instructions" : parser.get_format_instructions()
        }

    )

    return prompt | llm | parser


class Knowledge_Evaluation(BaseModel):
    score:int = Field(description="Enter the score between 1 and 5")
    reasoning : str = Field(description="Explanation of the score")

def get_knowlegde_chain(llm):

    parser = PydanticOutputParser(pydantic_object=Knowledge_Evaluation)

    prompt = PromptTemplate(
        template= """
You are a QA evaluator for customer support calls.
    Evaluate the agent's knowlege and accuracy in the following transcript.

    Consider:
    - Did the agent provide correct and relevant information?
    -Was the explanation clear and easy to unserstand?
    -Did the agent avoid vague or misleading statement?


    Transcript:
    {transcript}

    {format_instructions} """,
        input_variables= ["transcript"],
        partial_variables= {
            "format_instructions" : parser.get_format_instructions()
        }

    )

    return prompt | llm | parser


class Resolution_Evaluation(BaseModel):
    score:int = Field(description="Enter the score between 1 and 5")
    reasoning : str = Field(description="Explanation of the score")

def get_resolution_chain(llm):

    parser = PydanticOutputParser(pydantic_object=Resolution_Evaluation)

    prompt = PromptTemplate(
        template= """
You are a QA evaluator for customer support calls.
    Evaluate the resolution quality of the agent.

    Consider:
    - Did the agent fully resolve the customer's issue?
    -Were next steps clearly communicated?
    -Did the agent confirm resolution before ending?

    Transcript:
    {transcript}

    {format_instructions}""",
        input_variables= ["transcript"],
        partial_variables= {
            "format_instructions" : parser.get_format_instructions()
        }

    )

    return prompt | llm | parser


