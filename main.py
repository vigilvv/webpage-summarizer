import os
import requests
import subprocess
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-4o-mini"
# Headers - needed for some websites
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
SYSTEM_PROMPT = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."


if not API_KEY:
    print("No API key found.")

openai = OpenAI()


class Website:
    """
    Create Website object from the given "url" using the BeautifulSoup library.
    """
    url: str
    title: str
    text: str

    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(['script', 'style', 'img', 'input']):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)


def generate_user_prompt(website):
    """
    A function that outputs a User Prompt
    """
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt


def generate_messages(website):
    """
    A function that generates "messages" compatible with the OpenAI API
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": generate_user_prompt(website)}
    ]


def summarize(url):
    """
    Summarize a webpage
    """
    website = Website(url)
    response = openai.chat.completions.create(
        model=LLM_MODEL, messages=generate_messages(website))
    return response.choices[0].message.content


subprocess.run(
    ['glow', '-'], input=summarize("https://www.cnn.com").encode('utf-8'))
