from langchain.output_parsers import ResponseSchema
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


class ChangeRephraser(object):
    LLAMA = False
    DEBUG = False

    def __init__(self):
        if self.LLAMA:
            self.chat = Ollama(model="llama3.2")
        else:
            self.chat = ChatOpenAI(temperature=0, model_name='gpt-4', streaming=True)
        self.prompt = [
            ("system", """\
             Act as a service given the changes done to a software project in github, it will return a description of 
             these changes in Markdown format to be used as a Pull Request description.
             The description should have a title of up to 6 words summarizing the changes, followed by up to 2 
             sections one tilted "Logic changes" and one titled "Test changes" the logic changes section will contain a 
             subsection for each file that is not a test file titled with the file name each of these sub sections will 
             contain a bullet list summarizing the important changes in this file and their reason do not include more than 3 bullets.
             The Test changes section will be included only if there are test files and its contents will follow the same format as the Logic Section.
             The description should be in Markdown format. do include any thing in the response other than markdown.
             """),
            ("user", "{input}")
        ]
        self.prompt_template = ChatPromptTemplate.from_messages(self.prompt)
        self.chain = self.prompt_template | self.chat | StrOutputParser()

    def convert(self, text):
        if self.DEBUG:
            print(self.prompt_template1)
        out = self.chain.invoke(text)
        if self.DEBUG:
            for key, value in out:
                print(key + " ==> " + str(value))
        return out
