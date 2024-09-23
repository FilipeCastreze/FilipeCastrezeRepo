import openai
import getpass
import pandas as pd
import ipywidgets as widgets
import IPython.display as display


openai.api_key = getpass.getpass("Please enter your OpenAI Key:")

# Define two variants of the prompt
prompt_A = """Product description: A pair of shoes that can fit any foot size.
Seed words: adaptable, fit, omni-fit.
Product names:"""

prompt_B = """Product description: A home milkshake maker.
Seed words: fast, healthy, compact.
Product names: HomeShaker, Fit Shaker, QuickShake, Shake Maker

Product description: A watch that can tell accurate time in space.
Seed words: astronaut, space-hardened, eliptical orbit
Product names: AstroTime, SpaceGuard, Orbit-Accurate, EliptoTime.

Product description: A pair of shoes that can fit any foot size.
Seed words: adaptable, fit, omni-fit.
Product names:"""

def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content

# Iterate through the prompts and get responses
test_prompts = [prompt_A, prompt_B]
responses = []
num_tests = 5

for idx, prompt in enumerate(test_prompts):
    # prompt number as a letter
    var_name = chr(ord('A') + idx)

    for i in range(num_tests):
        # Get a response from the model
        response = get_response(prompt)

        data = {
            "variant": var_name,
            "prompt": prompt,
            "response": response
            }
        responses.append(data)

# Convert responses into a DataFrame
df = pd.DataFrame(responses)

# Save the DataFrame as a CSV file
df.to_csv("responses.csv", index=False)

print(df)

# Load the responses.csv file:
df = pd.read_csv("responses.csv")

# Shuffle the DataFrame
df = df.sample(frac=1).reset_index(drop=True)

# Assuming df is your DataFrame and 'response' is the column with the text you want to test
response_index = 0
df["feedback"] = pd.Series(dtype="str")  # add a new column to store feedback

response = widgets.HTML()
count_label = widgets.Label()

def update_response():
    new_response = df.iloc[response_index]["response"]
    new_response = (
        "<p>" + new_response + "</p>"
        if pd.notna(new_response)
        else "<p>No response</p>"
    )
    response.value = new_response
    count_label.value = f"Response: {response_index + 1} / {len(df)}"


def on_button_clicked(b):
    global response_index
    #  convert thumbs up / down to 1 / 0
    user_feedback = 1 if b.description == "👍" else 0

    # update the feedback column
    df.at[response_index, "feedback"] = user_feedback

    response_index += 1
    if response_index < len(df):
        update_response()
    else:
        # save the feedback to a CSV file
        df.to_csv("results.csv", index=False)

        print("A/B testing completed. Here's the results:")
        # Calculate score for each variant and count the number of rows per variant
        summary_df = (
            df.groupby("variant")
            .agg(count=("feedback", "count"), score=("feedback", "mean"))
            .reset_index()
        )
        print(summary_df)

update_response()

thumbs_down_button = widgets.Button(description="👎")
thumbs_down_button.on_click(on_button_clicked)

thumbs_up_button = widgets.Button(description="👍")
thumbs_up_button.on_click(on_button_clicked)


button_box = widgets.HBox(
    [
        thumbs_up_button,
        thumbs_down_button,
    ]
)

# After clicking it 10 times, then click it once more to display
display(response, button_box, count_label)