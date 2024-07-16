# Imports
import os
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent
from langchain_community.chat_models import ChatOpenAI
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
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
        background-color: #FFFDD0;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        color: black;
    }
    .user-message {
        background-color: #D0D2FF;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        text-align: right;
        color: black;
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
    st.title("CarAssistAI - Bot")
    # st.subheader("Powered by LangChain + OpenAI + Serpapi + Streamlit")

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
    llm = ChatOpenAI(model_name='gpt-4',
                     temperature=0.5,
                     max_tokens=2048)

    # Load in some tools to use - serpapi for google use
    tools = load_tools(["serpapi"], llm=llm)

    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True,memory=memory)

    # Accept input from user 
    car_name = st.text_input("Enter Your Car Name: ",key="1") 
    car_year = st.text_input("Enter Your Car Year: ",key="2")  
    car_model = st.text_input("Enter Your Car Model",key="3")
    model = car_name + car_year + car_model
    user_input = st.text_input("Describe your issue:",key="4")
    # Accept input from user
    # Submit Button Logic
    if st.button("Submit") and user_input:
        with st.spinner('Generating response...'):
            try:
                # Generate response
                response = agent.invoke(f"""
                                        You are a Virtual Assistant to SUGGEST CAR DIAGNOSIS. BASED ON THIS CAR {model}, PROVIDE A DESCRIPTION OF WHAT IS WRONG AND HOW TO FIX IT. CAREFULLY ASSESS THE CONTEXT BEFORE ANSWERING.
                                           
                                        Customer Issue: {user_input}

                                        Format:
                                        Give the Diagnosis on the basis of the given car.
                                        WHAT IS THE DIAGNOSIS: ....
                                        HOW TO FIX IT: ....
                                        """)
                response_text = response['output'] if isinstance(response, dict) and 'output' in response else "Sorry I am unable to answer your question"
                
                # Store conversation
                st.session_state.past.append(user_input)
                st.session_state.generated.append(response_text)

                # Display conversation
                for i in range(len(st.session_state.past)-1, -1, -1):
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
