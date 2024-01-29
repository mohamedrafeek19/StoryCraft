import streamlit as st
import requests
import prompts  # Import prompts.py
import random
from prompts import generate_structured_sentence,format_twist_response

# Streamlit page configuration
st.set_page_config(page_title="StoryCraft - Interactive Storyteller",layout="wide")

# API configuration
API_KEY = st.secrets["API_KEY"]
TOKEN = st.secrets["TOKEN"]

# Initialize Streamlit session state
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None

# Initialize a session state variable for the selected question
if 'selected_question' not in st.session_state:
    st.session_state['selected_question'] = None

# Initialize random questions in session state if not already set
if 'random_questions' not in st.session_state:
    suggested_questions = ["Who created you?", "What is StoryCraft?", "How does StoryCraft work?", "What are the features of app?"]
    random.shuffle(suggested_questions)
    st.session_state['random_questions'] = suggested_questions[:2]

# Initialize 'story_created' in session state if not already set
if 'story_created' not in st.session_state:
    st.session_state['story_created'] = False
# Initialize session states for storing twist details
if 'twist_title' not in st.session_state:
    st.session_state['twist_title'] = ''
if 'twist_body' not in st.session_state:
    st.session_state['twist_body'] = ''
if 'twist_summaries' not in st.session_state:
    st.session_state['twist_summaries'] = []
# After initializing your session state variables:
if 'twist_titles_with_ids' not in st.session_state:
    st.session_state['twist_titles_with_ids'] = {}
# Initialize a counter for unique keys in session state if not present
if 'input_key_counter' not in st.session_state:
    st.session_state['input_key_counter'] = 0

# Define the style for headings, subheadings, and buttons
style = """
<style>
    body {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    h1 { /* Title */
    color: #c9b249; /* A gold*/
    font-size: 2em;
    margin-bottom: 0.5em;
    }
    h3 { /* Subheader */
    font-size: 1.5em;
    margin-bottom: 0.3em;
    transition: color 0.3s ease;
    }
    /* Streamlit native buttons */
    .stButton>button { 
        background-color: #F0F3F4; /* Light grey background for a subtle look */
        color: #333333; /* Dark text for contrast */
        border: 2px solid #BDC6CF; /* Slightly darker border for definition */
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s, transform 0.3s;
    }

    .stButton>button:hover {
        background-color: #DDE1E4; /* A shade darker on hover */
        transform: translateY(-2px); /* Slight lift effect */
    }

    /* Custom button class for alternative styling */
    .button { 
        background-color: #E8EEF1; /* Even lighter grey for an alternative button */
        color: #5C677D; /* Soft dark blue for text */
        padding: 0.5em 1em;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s, box-shadow 0.3s, transform 0.3s;
    }

    .button:hover {
        background-color: #CAD3D8; /* A subtle hover state */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* Soft shadow for depth */
        transform: translateY(-2px); /* Slight lift effect */
    }
</style>
"""

# Inject the style into the app
st.markdown(style, unsafe_allow_html=True)

def display_response(api_input, message):
    st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #e1f5fe; margin-bottom: 10px;'>👤 <strong>API Input:</strong><br>{api_input}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #f0f4c3; margin-bottom: 10px;'>📚 <strong>Generated Prompt:</strong><br>{message}</div>", unsafe_allow_html=True)

# Define the API functions
def get_current_user():
        response = requests.get(
            'https://story3.com/api/v2/users/me',
            headers={'accept': 'application/json', 'x-auth-token': TOKEN, 'Authorization': f'Bearer {TOKEN}'}
        )
        return response.json()

def create_user(agent_data):
    response = requests.post(
        'https://story3.com/api/v2/users',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        },
        json={"agent": agent_data}
    )
    if response.status_code != 201:
        return response.status_code, response.json()  # Return the error code and message
    return response.status_code, None

def get_authentication_token():
    response = requests.get(
        'https://story3.com/api/v2/users/me/api_key',
        headers={'accept': 'application/json', 'x-auth-token': TOKEN}
    )
    return response.json()

# Function to get the user's balance in orbs
def get_users_balance():
    response = requests.get(
        'https://story3.com/api/v2/billing/balance',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}'
        }
    )
    return response.json()

# Function to get the user's earnings
def get_users_earnings():
    response = requests.get(
        'https://story3.com/api/v2/billing/earnings',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}'
        }
    )
    return response.json()

# Function to get the user's transactions
def get_users_transactions():
    response = requests.get(
        'https://story3.com/api/v2/billing/transactions',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}'
        }
    )
    return response.json()

# UI Layout
st.title("StoryCraft - Interactive Storyteller")

def get_new_authentication_token():
    response = requests.post(
        'https://story3.com/api/v2/users/me/api_key',
        headers={'accept': 'application/json', 'x-auth-token': TOKEN}
    )
    return response  # Return the whole response object

def create_agent_request():
    response = requests.post(
        'https://story3.com/api/v2/users/me/agent-request',
        headers={'accept': '*/*', 'x-auth-token': TOKEN}
    )
    return response  # Return the whole response object

# Define a new function to display responses in the sidebar
def display_sidebar_response(question, message):
    st.sidebar.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #fadadd; margin-bottom: 10px;'>👤 <strong>Question:</strong><br>{question}</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #fffacd; margin-bottom: 10px;'>📚 <strong>Answer:</strong><br>{message}</div>", unsafe_allow_html=True)

def create_story(title, body, lang, status, monetization_option):
    response = requests.post(
        'https://story3.com/api/v2/stories',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        },
        json={
            "title": title, 
            "body": body, 
            "lang": lang, 
            "status": status, 
            "monetization_option": monetization_option
        }
    )
    return response.json()

def get_analytics():
    response = requests.get(
        'https://story3.com/api/v2/analytics',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}'
        }
    )
    return response.json()

def get_story_analytics(story_hash_id):
    response = requests.get(
        f'https://story3.com/api/v2/analytics/{story_hash_id}',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}'
        }
    )
    return response.json()

def update_story_details(hash_id, genre, tags, title, body):
    tags_list = [tag.strip() for tag in tags.split(',')]  # Split and clean tags
    tags_list = [tag for tag in tags_list if len(tag) <= 100]  # Validate tag length

    response = requests.patch(
        f'https://story3.com/api/v2/stories/{hash_id}',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        },
        json={
            "genre": genre,
            "tags": tags_list,
            "title": title,
            "body": body
        }
    )
    if response.status_code != 200:
        print(f"Error updating story: {response.json()}")
        return None
    return response.json()

# Function to get user's stories
def get_user_stories():
    response = requests.get(
        'https://story3.com/api/v2/stories/my',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}'
        }
    )
    if response.status_code == 200:
        stories = response.json()
        return stories[:5]  # Return only the top 5 stories
    else:
        print(f"Error fetching stories: {response.json()}")
        return []

def create_twist(hash_parent_id, title, body, parent_twist_id=None):
    # Validate title and body length
    if len(title) > 80:
        return {"error": "Title must be shorter than or equal to 80 characters"}
    if len(body) > 1200:
        return {"error": "Body must be shorter than or equal to 1200 characters"}
    data = {
        "hashParentId": hash_parent_id if not parent_twist_id else parent_twist_id,
        "title": title,
        "body": body,
        "isExtraTwist": bool(parent_twist_id)  # set to True if parent_twist_id is provided
    }
    response = requests.post(
        'https://story3.com/api/v2/twists',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        },
        json=data
    )
    return response.json()

def on_add_twist():
    st.session_state['show_add_twist'] = True

# In the handle_add_twist function
def handle_add_twist(twist_title, twist_body):
    # Parent twist's hashId will be used as hashParentId for the sub-twist
    parent_twist_id = None
    if len(st.session_state['twist_summaries']) >= 3:
        st.warning("To add further sub-twists, please go to https://story3.com/ and create sub-twists there, as Story3 does not allow creating more than 3 twists for one story in this app.")
        return  # Exit the function to prevent adding more twists
    
    existing_twists = [(summary['title'], summary['hashId']) for summary in st.session_state['twist_summaries']]
    twist_titles = [title for title, _ in existing_twists]
    selected_twist_title = st.selectbox("Select Parent Twist Title:", twist_titles)
    parent_twist_id = next((id for title, id in existing_twists if title == selected_twist_title), None)

    if twist_title and twist_body:
        twist_response = create_twist(
            st.session_state['story_hash_id'], 
            twist_title, 
            twist_body, 
            parent_twist_id  # pass the hashId of the selected twist as hashParentId
        )
        process_twist_response(twist_response,twist_title)

def process_twist_response(twist_response, twist_title):
    if twist_response.get('statusCode', 200) == 200:
        twist_id = twist_response.get('hashId')
        st.session_state['twist_titles_with_ids'][twist_title] = twist_id
        formatted_twist = format_twist_response(twist_response, API_KEY)
        st.success('Twist added successfully!')
        st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #fffacd; margin-bottom: 10px;'>📚 <strong>Twist Stories Summary:</strong><br>{formatted_twist}</div>", unsafe_allow_html=True)
    else:
        error_message = twist_response.get('message', 'Unknown error')
        if 'more than 3 twists' in error_message:
            st.warning("To add further sub-twists, please go to https://story3.com/ and create sub-twists there, as Story3 does not allow creating more than 3 twists for one story in this app.")
        else:
            st.error("Error adding twist: " + error_message)

def publish_twist(hash_id):
    response = requests.post(
        f'https://story3.com/api/v2/twists/{hash_id}/publish',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        }
    )
    return response.json()

def publish_story(hash_id):
    response = requests.post(
        f'https://story3.com/api/v2/stories/{hash_id}/publish',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json'
        }
    )
    return response.json()

def delete_story(hash_id):
    response = requests.delete(
        f'https://story3.com/api/v2/stories/{hash_id}',
        headers={
            'accept': 'application/json',
            'x-auth-token': TOKEN,
            'Authorization': f'Bearer {TOKEN}'
        }
    )
    return response.status_code == 200
   
# Update sidebar with new API options
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:  # This column has twice the space and will contain the image
        st.image("storycraft.png", width=200)
    st.header("User Actions")
    api_options = [
        'Select API',
        '/api/v2/users/me',
        '/api/v2/users/me/api_key',
        '/api/v2/users',
        '/api/v2/users/me/agent-request',
        '/api/v2/billing/balance',
        '/api/v2/billing/earnings',
        '/api/v2/billing/transactions',
        '/api/v2/stories',
        '/api/v2/analytics',
        '/api/v2/stories/my'
    ]
    selected_api = st.selectbox("Choose an API", api_options)

    # Conditionally hide the submit button based on the selected API
    if selected_api not in ['/api/v2/users/me/agent-request', '/api/v2/users','/api/v2/stories','/api/v2/stories/my']:
       submit_button = st.sidebar.button("Submit", key=f'submit_{selected_api.replace("/", "_")}')

# Handle different API calls
if selected_api == '/api/v2/users':
    agent_data = st.sidebar.text_input("Enter Agent Data", key='agent_data')
    create_user_button = st.sidebar.button("Create User", key='create_user')
    if create_user_button:
        response_code, response_message = create_user(agent_data)
        if response_code == 201:
            display_response("/api/v2/users", "User created successfully")
        else:
            custom_message = f"You need to create an account on story3.com and then use StoryCraft to get your information since story3 does not allow direct user creation in my app."
            display_response(selected_api,custom_message)

elif selected_api == '/api/v2/users/me':
    if submit_button:
        st.session_state['user_info'] = get_current_user()
        openai_key = st.secrets["API_KEY"]
        welcome_msg = prompts.generate_welcome_message(st.session_state['user_info'], openai_key)
        display_response(selected_api, welcome_msg)

elif selected_api == '/api/v2/users/me/api_key':
    if submit_button:
        if st.session_state['user_info']:
            pseudonym = st.session_state['user_info'].get('pseudonym', 'Unknown User')
            # Custom message formatting
            custom_message = f"Your pseudonym '{pseudonym}' can be used as a token for authentication with the header 'x-auth-token' in Story3 API Swagger documentation."
            display_response(selected_api, custom_message)
        else:
            token_info = get_authentication_token()
            pseudonym = token_info.get('pseudonym', 'Unknown User')
            # Custom message formatting
            custom_message = f"Your pseudonym '{pseudonym}' can be used as a token for authentication with the header 'x-auth-token' in Story3 API Swagger documentation."
            display_response(selected_api, custom_message)

elif selected_api == '/api/v2/users/me/agent-request':
    response = create_agent_request()
    if response.status_code == 201:
        display_response(selected_api, "Agent request created successfully")
    elif response.status_code == 409 and response.json().get('message') == 'users_agent_application_already_created':
        display_response(selected_api, "Agent application has already been created.")
    else:
        error_details = response.json()
        display_response(selected_api, f"Error in creating agent request: {error_details.get('message', 'Unknown error')}")

elif selected_api == '/api/v2/billing/balance':
    if submit_button:
       balance_info = get_users_balance()
       if 'statusCode' in balance_info and balance_info['statusCode'] == 500:
            display_response(selected_api, "Balance information is currently unavailable since story3 maintains it confidential.")
       else:
            display_response(selected_api, balance_info)

elif selected_api == '/api/v2/billing/earnings':
    # Check if user info is available in the session state
    if 'user_info' in st.session_state and st.session_state['user_info']:
        if submit_button:
            earnings_info = get_users_earnings()
            pseudonym = st.session_state['user_info'].get('pseudonym', 'Unknown User')
            formatted_earnings = prompts.format_earnings_info(earnings_info, pseudonym)
            display_response(selected_api, formatted_earnings)
    else:
        # Inform the user to run '/api/v2/users/me' API first
        st.error("Please run the '/api/v2/users/me' API to get user information before accessing earnings.")

elif selected_api == '/api/v2/billing/transactions':
    if submit_button:
        transactions_info = get_users_transactions()
        if 'statusCode' in transactions_info and transactions_info['statusCode'] == 500:
            display_response(selected_api, "Transaction details are currently unavailable since story3 maintains it confidential")
        else:
            display_response(selected_api, transactions_info)

# Show 'Get My Stories' button for '/api/v2/stories/my'
elif selected_api == '/api/v2/stories/my':
    if st.sidebar.button("Get My Stories"):
        user_stories = get_user_stories()
        if user_stories:
                for story in user_stories[:10]:
                    structured_summary = prompts.format_user_story_response(story, API_KEY)
                    st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #fffacd; margin-bottom: 10px;'>📚 <strong>User Stories Summary:</strong><br>{structured_summary}</div>", unsafe_allow_html=True)
        else:
            st.write("No stories found.")

elif selected_api == '/api/v2/stories':
    # Row for header and delete button  
    header_col, delete_col = st.columns([3, 1])  # Adjust the ratio as needed
    with header_col:
        st.subheader("Create a Story")
    
    # Increment key counter for unique keys each time the story is deleted
    delete_triggered = False

    # Use the counter in session state to create unique keys
    unique_key = st.session_state['input_key_counter']
    story_title_key = f"story_title_{unique_key}"
    story_body_key = f"story_body_{unique_key}"

    story_title = st.text_input("Story Title", key=story_title_key)
    story_body = st.text_area("Story Body", key=story_body_key)
    story_lang = st.text_input("Language", "English", key=f"story_lang_{unique_key}")
    story_status = st.text_input("Status", "Draft", disabled=True, key=f"story_status_{unique_key}")
    monetization_option = st.text_input("Monetization Option", "Dynamic", disabled=True, key=f"monetization_option_{unique_key}")

    # Create Story Draft button
    if st.button("Create Story Draft", key='create_story'):
        if story_title and story_body:
            response = create_story(story_title, story_body, story_lang, story_status, monetization_option)
            if 'hashId' in response:
                st.session_state['story_response'] = response
                st.session_state['story_created'] = True
                st.session_state['story_hash_id'] = response['hashId']
                formatted_response = prompts.format_story_creation_response(response, API_KEY)
                st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #fffacd; margin-bottom: 10px;'>📚 <strong>Story Response:</strong><br>{formatted_response}</div>", unsafe_allow_html=True)

    with delete_col:
        if 'story_created' in st.session_state and st.session_state['story_created']:
            if st.button("Delete Story", key='delete_story'):
                if delete_story(st.session_state['story_hash_id']):
                    st.session_state['story_created'] = False
                    st.session_state['story_hash_id'] = None
                    st.session_state['input_key_counter'] += 1  # Increment the key counter
                    delete_triggered = True
    
    # If delete was triggered, rerun the app to clear the inputs
    if delete_triggered:
        st.experimental_rerun()
    
    # Create placeholders for twists
    twist_section_placeholder = st.empty()
    twist_button_placeholder = st.empty()

    if st.session_state.get('story_created', False):
        if not st.session_state.get('finish_twists_done', False): 
            with twist_section_placeholder.container(): # Check if twists are not finished
                st.subheader("Add Story Twists")

                # Directly create input fields for twist title and body
                twist_title_input = st.text_input("Twist Title", key='twist_title')
                twist_body_input = st.text_area("Twist Body", key='twist_body')

                # Create a single row for the buttons
                cols = st.columns([1, 1])  # Equal width for both buttons
                if cols[0].button("Add Story Twist", key='add_story_twist'):
                    handle_add_twist(twist_title_input, twist_body_input)
                    # Clear and recreate input fields
                    st.session_state['twist_title_session'] = None
                    st.session_state['twist_body_session'] = None

                if 'finish_twists_done' not in st.session_state:
                    st.session_state['finish_twists_done'] = False

                # Button to finish adding twists
                if cols[1].button("Finish Twists", key='finish_twists'):
                    st.session_state['finish_twists_done'] = True
                    twist_section_placeholder.empty()  # Clear the twists section
                    twist_button_placeholder.empty()  # Clear the buttons

                # Display all twist summaries
                for twist_summary in st.session_state['twist_summaries']:
                    st.markdown(twist_summary, unsafe_allow_html=True)

        # After finishing twists, show Update Story Details Section
        if st.session_state.get('finish_twists_done', False):
            # Use temporary variables to store input data
            genre_input = st.text_input("Add Genre", key='story_genre_session')
            tags_input = st.text_input("Add Tags (comma-separated)", key='story_tags_session')

            if st.button("Update Story Details"):
                # Update the session state with the input data
                st.session_state['story_genre'] = genre_input
                st.session_state['story_tags'] = tags_input
                title = st.session_state['story_response'].get('title', '')
                body = st.session_state['story_response'].get('body', '')
                genre = st.session_state['story_genre']
                tags = st.session_state['story_tags'].split(',')

                structured_sentence = generate_structured_sentence(title, body, genre, tags, API_KEY)
                st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #fffacd; margin-bottom: 10px;'>📚 <strong>Updated Story:</strong><br>{structured_sentence}</div>", unsafe_allow_html=True)

            # View Analytics Button
            if 'story_hash_id' in st.session_state:
                if st.button(f"View Analytics for {st.session_state['story_hash_id']}"):
                    analytics_response = get_story_analytics(st.session_state['story_hash_id'])
                    if analytics_response:
                            formatted_analytics = prompts.format_analytics_info_story(analytics_response, API_KEY)
                            st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #fffacd; margin-bottom: 10px;'>📚 <strong>Answer:</strong><br>{formatted_analytics}</div>", unsafe_allow_html=True)
                    else:
                        st.error("Error fetching analytics data.")
    
                # Publishing Section
                if st.session_state.get('finish_twists_done', False):
                    if st.button("Publish Story and Twists"):
                        story_title = st.session_state['story_response']['title']  # Fetch the story title
                        twist_titles = list(st.session_state['twist_titles_with_ids'].keys())

                         # Attempt to publish the story and twists
                        story_published = publish_story(st.session_state['story_hash_id'])
                        twists_published = all([publish_twist(twist_hash_id) for twist_hash_id in st.session_state['twist_titles_with_ids'].values()])

                        # Generate and display the success message
                        if story_published and twists_published:
                            publish_message = prompts.generate_publish_success_message(story_title, twist_titles, API_KEY)
                            st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #FFF0F5; margin-bottom: 10px;'>📚 <strong>Publication Success:</strong><br>{publish_message}</div>", unsafe_allow_html=True)
                        else:
                            st.error("Failed to publish story or one of the twists.")

elif selected_api == '/api/v2/analytics':
    if submit_button:
        analytics_data = get_analytics()
        formatted_analytics = prompts.format_analytics_info(analytics_data, API_KEY)
        display_response(selected_api, formatted_analytics)

else:
    st.sidebar.write("Select an API to proceed.")

# Sidebar for general questions
with st.sidebar:
    st.markdown("<h2>Ask a General Question</h2>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, question in enumerate(st.session_state['random_questions']):
        if cols[i].button(question):
            st.session_state['selected_question'] = question

    custom_question = st.text_input("Ask your own question:")
    if st.button("Ask", key='ask_custom_question'):
        st.session_state['selected_question'] = custom_question

    if st.session_state['selected_question']:
        question = st.session_state['selected_question']
        response_text = prompts.generate_general_response(question, API_KEY)
        display_sidebar_response(question, response_text)
        st.session_state['selected_question'] = None  # Reset the selected question
        
with st.sidebar.expander("User Guide",expanded=False):
    user_guide_markdown = """
        ## User Guide

        ### My project, "StoryCraft - Interactive Storyteller," is a Streamlit-based web app designed for interactive storytelling, integrating with the Story3 API. Here's an overview and a user based guide of my project:

        #### Project Overview:
        - **Story Creation and Management:** Users can create, update, and delete stories. This includes adding twists to make stories more engaging.
        - **Story3 API Integration:** The app leverages Story3's API for several features, including user management, story analytics, and transaction details. This API is key to the app's functionality.
        - **Interactive Features:** Users can interact with the app through a sidebar, choosing different API functions and adding custom questions.
        - **User Interaction and Responses:** The app uses prompts to generate structured sentences and format responses, enhancing user interaction.

        #### User Guide:
        - **Starting with StoryCraft:** Launch the app to access its features laid out in a user-friendly interface.The sidebar contains a user guide and different API options.
        - **Creating and Managing Stories:** Select 'Create a Story' by clicking /api/v2/stories. Enter details like title, body, and language.Stories can be updated or deleted as needed.
        - **Adding Twists to Stories:** Enhance your story by adding twists. Provide a title and body for the twist and integrate it into your story.
        - **Using Story3 API Functions:** Access various functionalities like viewing user info, balance, earnings, and transactions through the sidebar.Interact with the app using Story3's API for a dynamic experience.
        - **Viewing Analytics and Publishing:** Analyze your story's performance and make informed decisions to improve engagement.Publish your story and its twists to share them with a wider audience.
        - **Asking Questions and Interacting:** Use the sidebar to ask general questions or interact with different API options.The app responds with generated prompts and structured information.

        Enjoy crafting your unique stories!
        """
    st.markdown(user_guide_markdown, unsafe_allow_html=True)

     # Adding a distinct note
    note_markdown = """
    <div style="border: 2px solid #009688; border-radius: 5px; padding: 10px; margin-top: 10px; background-color: #e0f2f1;">
        <strong>Note:</strong><br>
        - The app currently operates with a preset API key. Future updates might allow personal API key usage for enhanced user experiences.<br>
        - The app is designed with the intention of providing a seamless and interactive storytelling platform, leveraging the capabilities of Story3's API and AI-generated content.
    </div>
    """
    st.markdown(note_markdown, unsafe_allow_html=True)

    # Collecting User Feedback
    st.sidebar.title("Feedback")
    rating = st.sidebar.slider("Rate your experience", 1, 5, 3)
    if st.sidebar.button("Submit Rating"):
        st.sidebar.success(f"Thanks for rating us {rating} stars!")
        st.sidebar.markdown(
            "Do visit my [Github Repository](https://github.com/mohamedrafeek19/StoryCraft)"
        )
