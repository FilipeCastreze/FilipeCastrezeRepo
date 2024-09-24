import getpass
from openai import OpenAI
import tiktoken
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

client = OpenAI()

# Get the openai secret key:
secret_key = getpass.getpass(
    "Please enter your openai key: "
)  # https://platform.openai.com/account/api-keys

client.api_key = secret_key

article_headings = [
    "I. Introduction A. Definition of the 2008 Financial Crisis B. Overview of the Causes and Effects of the Crisis C. Importance of Understanding the Crisis",
    "II. Historical Background A. Brief History of the US Financial System B. The Creation of the Housing Bubble C. The Growth of the Subprime Mortgage Market",
    "III. Key Players in the Crisis A. Government Entities B. Financial Institutions C. Homeowners and Borrowers",
    "IV. Causes of the Crisis A. The Housing Bubble and Subprime Mortgages B. The Role of Investment Banks and Rating Agencies C. The Failure of Regulatory Agencies D. Deregulation of the Financial Industry",
    "V. The Domino Effect A. The Spread of the Crisis to the Global Financial System B. The Impact on the Real Economy C. The Economic Recession",
    "VI. Government Responses A. The Troubled Asset Relief Program (TARP) B. The American Recovery and Reinvestment Act C. The Dodd-Frank Wall Street Reform and Consumer Protection Act",
    "VII. Effects on Financial Institutions A. Bank Failures and Bailouts B. Stock Market Decline C. Credit Freeze",
    "VIII. Effects on Homeowners and Borrowers A. Foreclosures and Bankruptcies B. The Loss of Home Equity C. The Impact on Credit Scores",
    "IX. Effects on the Global Economy A. The Global Financial Crisis B. The Impact on Developing Countries C. The Role of International Organizations",
    "X. Criticisms and Controversies A. Bailouts for Financial Institutions B. Government Intervention in the Economy C. The Role of Wall Street in the Crisis",
    "XI. Lessons Learned A. The Need for Stronger Regulation B. The Importance of Transparency C. The Need for Better Risk Management",
    "XII. Reforms and Changes A. The Dodd-Frank Wall Street Reform and Consumer Protection Act B. Changes in Regulatory Agencies C. Changes in the Financial Industry",
    "XIII. Current Economic Situation A. Recovery from the Crisis B. Impact on the Job Market C. The Future of the US Economy",
    "XIV. Comparison to Previous Financial Crises A. The Great Depression B. The Savings and Loan Crisis C. The Dot-Com Bubble",
    "XV. Economic and Social Impacts A. The Widening Wealth Gap B. The Rise of Populist Movements C. The Long-Term Effects on the Economy",
    "XVI. The Role of Technology A. The Use of Technology in the Financial Industry B. The Impact of Technology on the Crisis C. The Future of the Financial Industry",
    "XVII. Conclusion A. Recap of the Causes and Effects of the Crisis B. The Importance of Learning from the Crisis C. Final Thoughts",
    "XVIII. References A. List of Sources B. Additional Reading C. Further Research",
    "XIX. Glossary A. Key Terms B. Definitions",
    "XX. Appendix A. Timeline of the Crisis B. Financial Statements of Key Players C. Statistical Data on the Crisis",
]

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def chatgpt_completion_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

def parse_for_chat_history(response: client = False, user_prompt=None):
    if user_prompt:
        return {'role': 'user', 'content': user_prompt}
    return {'role': 'assistant', 'content': response.choices[0].message.content}

def num_tokens_from_messages(messages, model="gpt-4o-2024-08-06"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print(
            "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

messages = [
  {"role": "system", "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."},
  {"role": "system", "name":"example_user", "content": "New synergies will help drive top-line growth."},
  {"role": "system", "name": "example_assistant", "content": "Things working well together will increase revenue."},
  {"role": "system", "name":"example_user", "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
  {"role": "system", "name": "example_assistant", "content": "Let's talk later when we're less busy about how to do better."},
  {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
]

model = "gpt-3.5-turbo-0301"

print(f"{num_tokens_from_messages(messages, model)} prompt tokens counted.")
# Should show ~126 total_tokens

system_prompt = "You are a helpful assistant for a financial news website. You are writing a series of articles about the 2008 financial crisis. You have been given a list of headings for each article. You need to write a short paragraph for each heading. You can use the headings as a starting point for your writing.\n\n"
system_prompt += "All of the subheadings:\n"

# Add all of the subheadings to the system prompt to give the model context:
for heading in article_headings:
    system_prompt += f"{heading}\n"

# Create the chat history object:
chat_history =  []

# Add in the system message:
chat_history.append({'role': 'system', 'content': system_prompt})

# This will ensure that if the token count goes over the limit, the last message will be removed,
# to ensure that the token count is reduced as the chat history grows:
MAX_TOKEN_SIZE = 2048

# Loop over all of the headings and generate a chunk for each one
for heading in article_headings:
    # Add on a user prompt to the chat history object:
    chat_history.append(
        {"role": "user", "content": f"Write a short paragraph about {heading}"}
    )

    # Tell ChatGPT to generate a response:
    response = chatgpt_completion_with_backoff(
        model="gpt-3.5-turbo", messages=chat_history
    )

    # Get the response from the ChatGPT object:
    chat_history.append(parse_for_chat_history(response))

    # Whilst the Chat history object is more than 2048 tokens, remove the oldest non-system message:
    while num_tokens_from_messages(chat_history, model) > 2048:
        # Find the index of the first non-system message
        non_system_msg_index = next(
            (i for i, msg in enumerate(chat_history) if msg["role"] != "system"), None
        )

        # If there is a non-system message, remove it
        if non_system_msg_index is not None:
            chat_history.pop(non_system_msg_index)

    # Print the response:
    print(response)