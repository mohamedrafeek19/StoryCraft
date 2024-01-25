import openai

def generate_welcome_message(user_info, API_KEY):
    openai.api_key = API_KEY

    prompt = f"Compose a neat and welcoming message for a user of StoryCraft. The user's details are:\n- Pseudonym: {user_info['pseudonym']}\n- Email: {user_info['email']}\n- User Since: {user_info['user']}\n- Author Since: {user_info['author']}\n- Agent State: {user_info['agent_state']}"

    response = openai.Completion.create(
      engine="gpt-3.5-turbo-instruct",
      prompt=prompt,
      max_tokens=200
    )

    return response.choices[0].text.strip()

def generate_general_response(question, API_KEY):
    openai.api_key = API_KEY

    # Custom responses for specific questions
    custom_responses = {
        "Who created you?": "I am developed by Mohamed Rafeek, an AI developer, using Story3 v2 APIs.",
        "What is StoryCraft?": "StoryCraft is an interactive storytelling platform powered by AI, utilizing Story3 v2 APIs.",
        "How does StoryCraft work?": "StoryCraft leverages advanced AI to create engaging and dynamic stories, providing users with a unique interactive experience.",
        "What are the features of app?":"StoryCraft offers innovative features like AI-driven story generation, interactive storytelling experiences, and a platform for writers to share and collaborate."

    }

    response_text = custom_responses.get(question)
    if not response_text:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=question,
            max_tokens=150
        )
        response_text = response.choices[0].text.strip()

    return response_text

def format_earnings_info(earnings_info, pseudonym):
    amount = earnings_info['amount']
    currency = earnings_info['currency']
    registered = 'incomplete' if not earnings_info['registered'] else 'complete'

    sentence = f"Your current account's pseudonym '{pseudonym}' has earnings amounting to ${amount} {currency}. Please note that registration for the earnings program appears to be {registered}."

    return sentence

def format_story_creation_response(story_response,API_KEY):
    openai.api_key = API_KEY
    prompt = f"Create a sentence summarizing the story creation response: {story_response}"

    response = openai.Completion.create(
      engine="gpt-3.5-turbo-instruct",
      prompt=prompt,
      max_tokens=200
    )

    return response.choices[0].text.strip()

def format_analytics_info(analytics_data, API_KEY):
    openai.api_key = API_KEY
    revenue = analytics_data['revenue']
    views = analytics_data['views']
    stories_count = analytics_data['storiesCount']
    unique_readers = analytics_data['uniqueReaders']

    prompt = f"Create a summary sentence for analytics data: Revenue is {revenue}, Views are {views}, Total stories count is {stories_count}, and Unique readers count is {unique_readers}."

    response = openai.Completion.create(
      engine="gpt-3.5-turbo-instruct",
      prompt=prompt,
      max_tokens=200
    )

    return response.choices[0].text.strip()

def format_analytics_info_story(analytics_data, API_KEY):
    openai.api_key = API_KEY

    # Setting default values for each key
    title = analytics_data.get('title', 'N/A')
    revenue = analytics_data.get('revenue', 0)
    views = analytics_data.get('views', 0)
    viewers = analytics_data.get('viewers', 0)
    paid_twist_unlockers = analytics_data.get('paidTwistUnlockers', 0)
    free_twist_unlockers = analytics_data.get('freeTwistUnlockers', 0)
    free_conversion = analytics_data.get('freeConversion', 0)
    paid_conversion = analytics_data.get('paidConversion', 0)

    prompt = f"Summarize the following analytics data into a sentence: Title: {title}, Revenue: {revenue}, Views: {views}, Viewers: {viewers}, Users who opened my story using paid twists: {paid_twist_unlockers}, Users who opened my story using free twists: {free_twist_unlockers}, Free Conversion Rate: {free_conversion}, Paid Conversion Rate: {paid_conversion}."

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=200
    )

    return response.choices[0].text.strip()

def generate_structured_sentence(title, body, genre, tags, API_KEY):
    openai.api_key = API_KEY
    # Create a prompt for OpenAI GPT to generate a structured sentence
    prompt = f"Generate a structured sentence summarizing a story with the following details:\nTitle: {title}\nBody: {body}\nGenre: {genre}\nTags: {', '.join(tags)}"

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=300
    )

    return response.choices[0].text.strip()

def format_user_story_response(story, API_KEY):
    openai.api_key = API_KEY
    # Create a prompt for the given story
    prompt = f"Provide a brief explanation for the story titled '{story['title']}':\n{story['summary']}"

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

def format_twist_response(twist_response, API_KEY):
    openai.api_key = API_KEY
    # Extracting necessary details from the twist response
    title = twist_response.get('title', 'Untitled')
    body = twist_response.get('body', 'No description provided.')
    status = twist_response.get('status', 'Unknown')
    monetization = twist_response.get('monetization_option', 'Not specified')
    createdAt = twist_response.get('createdAt', 'Unknown date')

    # Creating a prompt for OpenAI GPT to generate a structured sentence
    prompt = f"Generate a structured sentence summarizing a twist in a story with the following details:\nTitle: {title}\nBody: {body}\nStatus: {status}\nMonetization Option: {monetization}\nCreated At: {createdAt}"

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=200
    )

    return response.choices[0].text.strip()

def generate_publish_success_message(story_title, twist_titles, API_KEY):
    openai.api_key = API_KEY
    twist_titles_formatted = ", ".join([f'"{title}"' for title in twist_titles])

    prompt = f"Generate a congratulatory message for publishing a story titled '{story_title}' with twists titled {twist_titles_formatted}."

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=200
    )

    return response.choices[0].text.strip()