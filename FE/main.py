# from openai import OpenAI
import streamlit as st

st.title("Multi Media Information Retrieval")
import requests

# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

url_base = 'http://localhost:9000'


st.markdown("""
    <style>
        .stRadio > div {
            flex-direction: row;
        }
        .stRadio label {
            paddingTop: 10px;
            marginTop: 10px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stRadio input:checked + label {
            background-color: #4CAF50;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Thêm radio button với hai tùy chọn "Option 1" và "Option 2"
option = st.radio("Choose an option", ["Vector Search","Full Text Search"])


# if option == 'Vector Search':

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    prefix = prompt.split(" ")[0]
    query = " ".join(prompt.split(" ")[1:])
    # print(query)
    url = url_base + prefix
    # print(url)

    if prefix == "/chatbot":
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            print(option)
            params = {'query': str(query),
                        'mode' : option}
            response = requests.get(url, params=params).json()
            print(response)
            anwser = response['answer']
            # link = response['link']
            # respone = requests.get('http://localhost:9000/search', json={'query': prompt})
            # print(response.json())
            # st.markdown(f"[{anwser}]({link})", unsafe_allow_html=True)

            message_placeholder.markdown(anwser)
        st.session_state.messages.append({"role": "assistant", "content": anwser})
    
    if prefix == "/search":
        # display search result
        # print('search')
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            params = {'query': str(query),
                        'mode' : option}
            response = requests.get(url, params=params).json()['result']
            print(response)
    

            st.markdown("""
            <style>
            a:link {
            background-color: transparent;
            text-decoration: none;
            }
            a:visited {
            color:violet;
            background-color: transparent;
            text-decoration: none;
            }
            a:hover {
            color: blue;
            background-color: transparent;
            text-decoration: underline;
            }
            a:active {
            color: blue;
            background-color: transparent;
            text-decoration: underline;
            }
            </style>
            """, unsafe_allow_html=True)

            N_cards_per_row = 1

            
            if response:
                for idx_row in range(len(response)):
                    i = idx_row%N_cards_per_row
                    if i==0:
                        st.write("---")
                        cols = st.columns(N_cards_per_row, gap="large")
                    # draw the card
                    with cols[idx_row%N_cards_per_row]:
                        st.caption(f"**VNXPRESS**")
                        title = response[idx_row]['_source']['title']
                        link = response[idx_row]['_source']['link']
                        description = response[idx_row]['_source']['description']
                        st.markdown(f"**<p><a style='font-size:20px;' href={link}>{title.strip()}</a></p>**", unsafe_allow_html=True)
                        
                        st.markdown(f"*{description.strip()}*")
    