from .prompt import PromptGenerator

QWEN_DEFAULT_SYSTEM_TEMPLATE = """Answer the following questions as best you can. You have access to the following tools: `

<tool_list>"""

QWEN_DEFAULT_INSTRUCTION_TEMPLATE = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
"""

QWEN_DEFAULT_USER_TEMPLATE = """Question: <user_input>\n"""

QWEN_DEFAULT_EXEC_TEMPLATE = """Observation: <exec_result>"""


class QWenPromptGenerator(PromptGenerator):

    def __init__(self,
                 system_template=QWEN_DEFAULT_SYSTEM_TEMPLATE,
                 instruction_template=QWEN_DEFAULT_INSTRUCTION_TEMPLATE,
                 user_template=QWEN_DEFAULT_USER_TEMPLATE,
                 exec_template=QWEN_DEFAULT_EXEC_TEMPLATE,
                 assistant_template='',
                 sep='\n\n',
                 prompt_max_length=2800):
        super().__init__(system_template, instruction_template, user_template,
                         exec_template, assistant_template, sep,
                         prompt_max_length)
