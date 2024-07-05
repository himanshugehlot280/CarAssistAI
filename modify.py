# Imports
import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
import streamlit as st 
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI 
from langchain.chains import SequentialChain 
from langchain.agents import ChainToolkit 
from dotenv import load_dotenv

def main():
    # Streamlit page configuration
    st.set_page_config(page_title='Serpapi Agent', layout='wide')

    # CSS styling
    css = """
    <style>
    body {
        font-family: Arial, sans-serif;
    }
    .bot-message {
        background-color: #f1f1f1;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px; 
        color: red;
    }
    .user-message {
        background-color: #d1f1d1;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        text-align: right; 
        color: red;
    }
    </style>
    """
    st.write(css, unsafe_allow_html=True)

    # HTML templates
    bot_template = """
    <div class="bot-message">
        <p>{{MSG}}</p>
    </div>
    """
    user_template = """
    <div class="user-message">
        <p>{{MSG}}</p>
    </div>
    """ 


    # Initialize Session States
    if 'generated' not in st.session_state: 
        st.session_state['generated'] = []

    if 'past' not in st.session_state: 
        st.session_state['past'] = []

    # Set up the Streamlit app layout
    st.title("Intelligent Google Search ChatBot")
    st.subheader("Powered by LangChain + OpenAI + Serpapi + Streamlit")   

    template = """ 

    As A Virtual Assistant You have ask Car Make, Car Model, Car Year in series

    You are a Virtual Assistant to SUGGEST CAR DIAGNOSIS.
    BASED ON THE CAR MAKE, CAR MODEL, CAR YEAR and CAR ISSUE, PROVIDE A DESCRIPTION OF WHAT IS WRONG AND HOW TO FIX IT AND WHAT IS THE DIAGNOSIS? CAREFULLY ASSESS THE CONTEXT BEFORE ANSWERING.

    Format:
    Give the Diagnosis on the basis Of the given car
    WHAT IS THE DIAGNOSIS: ....
    HOW TO FIX IT: ....

    STRICTLY USE THIS FORMAT TO ANSWER

    {chat_history}
    Human: {human_input}
    Chatbot:"""

    prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
    )
    memory = ConversationBufferMemory(memory_key="chat_history")
    # Define Language Model
    llm = ChatOpenAI(model_name='gpt-3.5-turbo',
                 temperature=0.5,
                 max_tokens=256) 
    
    # Load in some tools to use - serpapi for google use and llm-math for math ops
    tools = load_tools(["serpapi"], llm=llm)  

    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

    # Accept input from user
    user_input = st.text_input("Enter your message:")   
    # Accept input from user
    # Submit Button Logic
    if st.button("Submit") and user_input:
        with st.spinner('Generating response...'):
            try:
                # Generate response
                try: 
                    # print('type(response)') 
                    # response = llm_chain.predict(human_input=user_input)
                    response = agent.invoke(f"AI Prompt: {PromptTemplate} User Question: {user_input}")  
                    response = response['output'] 
                    st.write(response)
                    # if isinstance(response, dict):
                    #     response = response.get('result', 'Sorry I am unable to answer your question') 
                    #     st.write(response)
                except:
                    response = "Sorry I am unable to answer your question"

                # Store conversation
                st.session_state.past.append(user_input)
                st.session_state.generated.append(response)

                # Display conversation
                for i in range(len(st.session_state.past)-1,-1,-1):
                    st.write(bot_template.replace("{{MSG}}", st.session_state.generated[i]), unsafe_allow_html=True)
                    st.write(user_template.replace("{{MSG}}", st.session_state.past[i]), unsafe_allow_html=True)
                    st.write("")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == '__main__': 
    load_dotenv()
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    os.environ["SERPAPI_API_KEY"] = os.getenv('SERPAPI_API_KEY')
    main()

