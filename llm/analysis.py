import json

from groq import Groq
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from llm.prompt import TOPIC_ANALYZER_PROMPT, SCRIPT_SCENE_PROMPT, VISUAL_STYLE_PROMPT, INSTA_CAPTION_PROMPT, \
    SCRIPT_SCENE_PROMPT_2
from utils.config import llm_baseurl, llm_key, llm_model


class LLMService:
    def __init__(self, model_temperature=0.7, json_output_required=True):
        self.url = llm_baseurl
        self.llm =  ChatOpenAI(
            model=llm_model,
            base_url=self.url,
            api_key=llm_key,
            temperature=model_temperature)
        if json_output_required:
            self.llm = self.llm.bind(response_format={"type": "json_object"})
        self.groq = Groq(api_key=llm_key)

    def analyze_topic(self, user_input,temperature):
        try:
            completion = self.groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": TOPIC_ANALYZER_PROMPT},
                    {"role": "user", "content": f"Generate themes for the topic {user_input}"}
                ],
                temperature=temperature,
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise e

    def generate_script(self, theme, purpose, tone, temperature):
        try:
            completion = self.groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SCRIPT_SCENE_PROMPT_2},
                    {"role": "user", "content": f"Generate script for the given theme: {theme}, purpose: {purpose} and tone: {tone}"}
                ],
                temperature=temperature,
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise e

    def generate_visual_style(self, script, theme):

        prompt = PromptTemplate.from_template(VISUAL_STYLE_PROMPT)
        chain = prompt | self.llm
        try:
            feedback = chain.invoke({"script": script, "theme": theme})
            print(f"llm analysis content:{feedback}\n")
            return feedback.content.strip()
        except Exception as e:
            raise e

    def generate_caption(self, theme, script, temperature):
        try:
            completion = self.groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": INSTA_CAPTION_PROMPT},
                    {"role": "user", "content": f"Generate caption for the given theme: {theme} and script: {script}"}
                ],
                temperature=temperature,
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise e