from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from helpers.jinja_helpers import build_templates_and_router
import guidance
import pdb

templates, router, module_name = build_templates_and_router(__file__)


# guidance.llm = guidance.llms.Transformers("TheBloke/wizard-mega-13B-GPTQ", device=0)
guidance.llm = guidance.llms.Transformers("TheBloke/Kimiko-7B-fp16", device=0)


examples = [
    {'input': 'I wrote about shakespeare',
    'entities': [{'entity': 'I', 'time': 'present'}, {'entity': 'Shakespeare', 'time': '16th century'}],
    'reasoning': 'I can write about Shakespeare because he lived in the past with respect to me.',
    'answer': 'No'},
    {'input': 'Shakespeare wrote about me',
    'entities': [{'entity': 'Shakespeare', 'time': '16th century'}, {'entity': 'I', 'time': 'present'}],
    'reasoning': 'Shakespeare cannot have written about me, because he died before I was born',
    'answer': 'Yes'}
]

# define the guidance program
structure_program = guidance(
'''Given a sentence tell me whether it contains an anachronism (i.e. whether it could have happened or not based on the time periods associated with the entities).
----

{{~! display the few-shot examples ~}}
{{~#each examples}}
Sentence: {{this.input}}
Entities and dates:{{#each this.entities}}
{{this.entity}}: {{this.time}}{{/each}}
Reasoning: {{this.reasoning}}
Anachronism: {{this.answer}}
---
{{~/each}}

{{~! place the real question at the end }}
Sentence: {{input}}
Entities and dates:
{{gen "entities"}}
Reasoning:{{gen "reasoning"}}
Anachronism:{{#select "answer"}} Yes{{or}} No{{/select}}''')


class InputData(BaseModel):
    input_data: str = Field(..., min_length=1, description="Input data must be at least 1 character long")

@router.get("")
async def guidance(request: Request):
    return templates.TemplateResponse("guidance.html", {
        "request": request })

@router.post("")
async def guidance(json: InputData):
    user_input = json.input_data

    # messages = [{ "role": "user", "content": user_input }]
    # resp = gptj.chat_completion(messages)

    # execute the program
    out = structure_program(
        examples=examples,
        input='The T-rex bit my dog'
    )

    pdb.set_trace()

    return "done"

    # return resp['choices'][0]['message']['content']
