from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class ChangeRephraser(object):
    LLAMA = False
    DEBUG = False

    def __init__(self):
        if self.LLAMA:
            self.chat = Ollama(model="llama3:8b")
        else:
            self.chat = ChatOpenAI(temperature=0, model_name='gpt-4', streaming=True)

        self.template = """\
                        You are a helpful assistant that rephrases the changes done to a software project in github, \
                        to be used as a Pull Request description.
                        Using following change , generate extract the following:
                        description: A description of the change included in the text, given that the text describe \
                        changes done to a software project in github, and the description you will proved will be used \
                        as a Pull Request description in github. The description should be a short summary of the changes and the reason for the changes.
                        The description should be formatted as markdown, each change should be in a new line with a number.
                        text: {text}
    
                        {format_instructions}
                        """
        self.description_schema = ResponseSchema(name='description',
                                                 description=' Pull request description')
        self.response_schemas = [self.description_schema]
        self.output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)
        self.format_instructions = self.output_parser.get_format_instructions()

    def convert(self, text):
        prompt_template = ChatPromptTemplate.from_template(self.template)
        if self.DEBUG:
            print(prompt_template)
        messages = prompt_template.format_messages(text=text,
                                                   format_instructions=self.format_instructions)
        response = self.chat(messages)
        json_dict = self.output_parser.parse(response.content)
        if self.DEBUG:
            for key, value in json_dict:
                print(key + " ==> " + str(value))
        return json_dict
