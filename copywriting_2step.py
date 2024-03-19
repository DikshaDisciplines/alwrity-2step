import time
import os
import json
import openai
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import retry, stop_after_attempt, wait_random_exponential

def main():
    set_page_config()
    custom_css()
    hide_elements()
    sidebar()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
    )

def custom_css():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            [class="st-emotion-cache-7ym5gk ef3psqc12"] {
                display: inline-block;
                padding: 5px 20px;
                background-color: #4681f4;
                color: #FBFFFF;
                width: 300px;
                height: 35px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

def sidebar():
    st.sidebar.title("as")
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown("🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")

def title_and_description():
    st.title("✍️ Alwrity - AI Generator for Two-Step Selling Process Copywriting Formula")
    with st.expander("What is **Two-Step Selling Process Copywriting Formula** & **How to Use**? 📝❗"):
        st.markdown('''
            ### What's Two-Step Selling Process Copywriting Formula, and How to use this AI generator 🗣️
            ---
            #### Two-Step Selling Process Copywriting Formula

            The Two-Step Selling Process focuses on guiding the audience through an informative stage followed by a persuasive selling stage:

            1. **Inform**: Providing valuable information to the audience to create awareness and understanding.
            2. **Sell**: Persuading the audience to take action or make a purchase based on the information provided.

            This formula helps in educating the audience about the product or service while also compelling them to take the desired action.

            #### Two-Step Selling Process Copywriting Formula: Simple Example

            - **Inform**: "Discover the benefits of our revolutionary posture corrector and how it can alleviate back pain."
            - **Sell**: "Take control of your spinal health today with our posture corrector. Buy now and experience the difference!"

            ---
        ''')


def input_section():
    with st.expander("**PRO-TIP** - Easy Steps to Create Compelling Two-Step Selling Process Copy", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            brand_name = st.text_input('**Enter Brand/Company Name**', help="Enter the name of your brand or company.")
        with col2:
            description = st.text_input(f'**Describe What {brand_name} Does ?** (In 5-6 words)', help="Describe your product or service briefly.")

        inform = st.text_input(f'**Provide Valuable Information (Inform)**', help="Share information about your product or service to create awareness.")
        sell = st.text_input(f'**Persuade to Take Action (Sell)**', help="Compel the audience to take action or make a purchase.")

        if st.button('**Get Two-Step Selling Copy**'):
            if inform.strip() and sell.strip():
                with st.spinner("Generating Two-Step Selling Copy..."):
                    selling_copy = generate_selling_copy(brand_name, description, inform, sell)
                    if selling_copy:
                        st.subheader('**👩‍💼💡 Your Two-Step Selling Copy**')
                        st.markdown(selling_copy)
                    else:
                        st.error("💥 **Failed to generate selling copy. Please try again!**")
            else:
                st.error("All fields are required!")

    page_bottom()


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_selling_copy(brand_name, description, inform, sell):
    prompt = f"""As an expert copywriter, I need your help in creating a marketing campaign for {brand_name},
        which is a {description}. Your task is to use the Two-Step Selling Process formula to craft compelling copy.
        Here's the breakdown:
        - Inform: {inform}
        - Sell: {sell}
        Do not provide explanations, provide the final marketing copy.
    """
    return openai_chatgpt(prompt)


def page_bottom():
    """Display the bottom section of the web app."""
    data_oracle = import_json(r"lottie_files/brain_robot.json")
    st_lottie(data_oracle, width=600, key="oracle")

    st.markdown('''
    Copywrite using Two-Step Selling Process Copywriting Formula - powered by AI (OpenAI, Gemini Pro).

    Implemented by [Alwrity](https://alwrity.netlify.app).

    Learn more about [Google's Stance on AI generated content](https://alwrity.netlify.app/post/googles-guidelines-on-using-ai-generated-content-everything-you-need-to-know).
    ''')

    st.markdown("""
    ### Inform:
    Discover the benefits of our revolutionary posture corrector and how it can alleviate back pain.

    ### Sell:
    Take control of your spinal health today with our posture corrector. Buy now and experience the difference!
    """)



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", max_tokens=500, top_p=0.9, n=1):
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"An error occurred: {err}")


# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url



if __name__ == "__main__":
    main()

