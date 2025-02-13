import requests
import random
import time
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

# Configuration
BASE_URL = "https://llama32.gaia.domains"
MODEL = "Llama-3.2-3B-Instruct-Q5_K_M"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
"What motivates people to succeed?",
"Why do some people enjoy challenges?",
"Which habits lead to a productive life?",
"What to consider when choosing a career?",
"How to improve decision-making skills?",
"How to stay focused in a busy world?",
"Can happiness be measured scientifically?",
"How to develop emotional intelligence?",
"How to maintain work-life balance?",
"How to build self-confidence?",
"Can personality change over time?",
"What are the secrets to a healthy relationship?",
"How to make meaningful friendships?",
"Where do cultural differences come from?",
"Can meditation improve mental health?",
"How does stress affect the human body?",
"Can people truly multitask?",
"How do different cultures view time?",
"How does music affect the brain?",
"What are the benefits of traveling alone?",
"How do childhood experiences shape adulthood?",
"Why do humans dream?",
"What makes a great leader?",
"How does body language influence communication?",
"How do social norms change over time?",
"Can people unlearn bad habits?",
"What are the key components of happiness?",
"How does gratitude improve mental well-being?",
"Why do humans seek adventure?",
"How does laughter benefit health?",
"How do memories shape identity?",
"What is the psychology behind motivation?",
"Can a positive mindset improve success?",
"How does sleep impact mental health?",
"What are the signs of emotional intelligence?",
"Why do people procrastinate?",
"Can humans ever truly be objective?",
"How does storytelling impact society?",
"How does social media shape opinions?",
"What are the effects of digital detoxing?",
"How do different cultures express love?",
"Can animals feel emotions like humans?",
"Why do people fear public speaking?",
"How do traditions influence personal identity?",
"Can kindness change the world?",
"How do people develop their sense of humor?",
"Why do some people enjoy being alone?",
"How does curiosity drive human progress?",
"What are the benefits of learning multiple languages?",
"Can people be naturally talented, or is it all practice?",
"How do first impressions influence relationships?",
"Why do people lie?",
"How does body language affect first impressions?",
"Can money buy happiness?",
"Why do people enjoy watching horror movies?",
"How does nostalgia influence emotions?",
"Why do humans crave social connections?",
"What are the effects of kindness on the brain?",
"How does personal space differ across cultures?",
"Can changing your environment change your mindset?",
"What are the best ways to reduce stress?",
"How do habits form and how can they be changed?",
"What are the long-term effects of loneliness?",
"How does music impact learning and memory?",
"Why do people develop phobias?",
"How does color affect human psychology?",
"Can personality tests accurately define who we are?",
"Why do some people love extreme sports?",
"How does humor help with stress?",
"Can dreams predict the future?",
"How does the brain process emotions?",
"What are the benefits of journaling?",
"How do social expectations shape human behavior?",
"Why do people enjoy conspiracy theories?",
"How does fame affect mental health?",
"Can humans live without technology?",
"What are the psychological effects of clutter?",
"Why do people enjoy collecting things?",
"How do different cultures celebrate success?",
"Can gratitude improve physical health?",
"How does peer pressure influence decision-making?",
"Why do people love mysteries?",
"How does childhood trauma affect adult relationships?",
"Can personality be inherited?",
"What are the psychological effects of music genres?",
"Why do people talk to themselves?",
"How does travel impact personal growth?",
"Can living in nature improve mental health?",
"Why do people enjoy sad music?",
"How does sleep deprivation affect emotions?",
"Can happiness be taught?",
"What are the psychological benefits of volunteering?",
"Why do people make New Year's resolutions?",
"How does social isolation affect mental health?",
"What are the benefits of deep breathing?",
"Can reading fiction improve empathy?",
"Why do some people love scary stories?",
"How do childhood friendships shape adult relationships?",
"Why do people enjoy puzzles and riddles?",
"Can a person’s name influence their personality?",
"How does emotional intelligence impact leadership?",
"Why do people love nostalgia?",
"What are the benefits of mindfulness?",
"How does gratitude change the brain?",
"Why do people enjoy road trips?",
"Can traveling change a person’s worldview?",
"How does body language impact job interviews?",
"Why do people love pets?",
"Can personality influence success?",
"How does nature impact creativity?",
"Why do people enjoy festivals?",
"How does architecture influence human emotions?",
"What are the effects of kindness on relationships?",
"Why do people love taking photos?",
"How do colors influence mood?",
"Why do people enjoy watching sports?",
"How does optimism impact health?",
"What are the psychological effects of working from home?",
"Can a smile change someone's mood?",
"Why do people love nostalgia-based entertainment?",
"How do different cultures handle stress?",
"Why do people enjoy collecting vintage items?",
"How does gratitude impact relationships?",
"Can a person's voice influence their personality?",
"Why do people enjoy surprises?",
"How does physical exercise impact the brain?",
"Why do people make wishes on their birthdays?",
"How does traveling change perspectives?",
"Can a positive mindset affect aging?",
"Why do people enjoy cooking?",
"How does laughter create social bonds?",
"Why do people love adventure?",
"Can personality change due to experiences?",
"How does culture shape our emotions?",
"Why do people enjoy exploring abandoned places?",
"What are the psychological effects of handwritten letters?",
"How does self-reflection improve decision-making?",
"Why do people enjoy watching sunsets?",
"Can memories be altered over time?",
"How does storytelling impact learning?",
"Why do people enjoy fantasy worlds?",
"Can music heal emotional wounds?",
"How does the environment affect creativity?",
"Why do people enjoy journaling?",
"Can a change in routine improve happiness?",
"Why do people love small talk?",
"How does travel impact self-confidence?",
"Can friendships last a lifetime?",
"Why do people enjoy simple pleasures?",
"How does curiosity shape learning?",
"Can a single moment change a person’s life?",
"Why do people enjoy handwritten notes?",
"How does a sense of belonging affect happiness?",
"Why do people love mystery books?",
"How does gratitude impact sleep?",
"Why do people enjoy stargazing?",
"Can positivity be contagious?",
"How does laughter connect people?",
"Why do people enjoy trying new foods?",
"How does relaxation improve creativity?",
"Why do people feel attached to objects?",
"How does optimism affect problem-solving?",
"Why do people enjoy being near the ocean?",
"Can small changes lead to big results?",
"Why do people enjoy storytelling?",
"How does perspective influence happiness?",
"Can a good conversation change a person’s day?",
"Why do people enjoy handwritten letters?",
"How does nostalgia impact decision-making?",
"Why do people love traditions?",
"Can personal growth be measured?",
"Why do people enjoy surprises?",
"How does self-expression impact mental well-being?",
"Why do people feel connected to music?",
"How does gratitude influence daily life?",
"Can a change in mindset transform reality?",
"Why do people love spontaneous adventures?",
"How does kindness shape communities?",
"Can small acts of kindness change the world?",
"Why do people love discovering new things?",
]

def chat_with_ai(api_key: str, question: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {"role": "user", "content": question}
    ]

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    for attempt in range(MAX_RETRIES):
        try:
            logging.info(f"Attempt {attempt+1} for question: {question[:50]}...")
            response = requests.post(
                f"{BASE_URL}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]

            logging.warning(f"API Error ({response.status_code}): {response.text}")
            time.sleep(RETRY_DELAY)

        except Exception as e:
            logging.error(f"Request failed: {str(e)}")
            time.sleep(RETRY_DELAY)

    raise Exception("Max retries exceeded")

def run_bot(api_key: str):
    while True:  # Outer loop to repeat the questions indefinitely
        random.shuffle(QUESTIONS)
        logging.info(f"Starting chatbot with {len(QUESTIONS)} questions in random order")

        for i, question in enumerate(QUESTIONS, 1):
            logging.info(f"\nProcessing question {i}/{len(QUESTIONS)}")
            logging.info(f"Question: {question}")

            start_time = time.time()
            try:
                response = chat_with_ai(api_key, question)
                elapsed = time.time() - start_time

                # Print the entire response
                print(f"Answer to '{question[:50]}...':\n{response}")

                logging.info(f"Received full response in {elapsed:.2f}s")
                logging.info(f"Response length: {len(response)} characters")

                # Ensure the script waits for the full response before proceeding
                time.sleep(QUESTION_DELAY)  # Wait before asking next question

            except Exception as e:
                logging.error(f"Failed to process question: {str(e)}")
                continue

def main():
    api_key = input("nhap key = ")
    run_bot(api_key)

if __name__ == "__main__":
    main()
