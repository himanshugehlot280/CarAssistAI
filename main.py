# # Imports
# import os
# from langchain.agents import load_tools
# from langchain.agents import initialize_agent
# from langchain.llms import OpenAI
# import streamlit as st
# from htmlTemplates import css, bot_template, user_template
# from apikey import serpapikey, openaikey

# def main():
#     # Streamlit page configuration
#     st.set_page_config(page_title='Serpapi Agent', layout='wide')

#     # Apply CSS styling
#     st.write(css, unsafe_allow_html=True)

#     # Initialize Session States
#     if 'generated' not in st.session_state: 
#         st.session_state['generated'] = []

#     if 'past' not in st.session_state: 
#         st.session_state['past'] = []

#     # Set up the Streamlit app layout
#     st.title("Intelligent Google Search ChatBot")
#     st.subheader(" Powered by LangChain + OpenAI + Serpapi + Streamlit") 


#     # Define Language Model
#     llm = OpenAI(model_name='gpt-3.5-turbo',
#                 temperature=0.9,
#                 max_tokens=256)
    
#     # Load in some tools to use - serpapi for google use and llm-math for math ops
#     tools = load_tools(["serpapi", "llm-math"], llm=llm)

#     # Initialize ageny
#     agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

#     # Accept input from user
#     user_input = st.text_input("Enter your message:")  

#     # Submit Button Logic
#     if st.button("Submit") and user_input:
#         with st.spinner('Generating response...'):
#             try:
#                 # Generate response
#                 try:
#                     response = agent.run(user_input)
#                 except:
#                     response = "Sorry I am unable to answer your question"

#                 # Store conversation
#                 st.session_state.past.append(user_input)
#                 st.session_state.generated.append(response)

#                 # Display conversation
#                 for i in range(len(st.session_state.past)-1,-1,-1):
#                     st.write(bot_template.replace("{{MSG}}",st.session_state.generated[i] ), unsafe_allow_html=True)
#                     st.write(user_template.replace("{{MSG}}",st.session_state.past[i] ), unsafe_allow_html=True)
#                     st.write("")

#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")


# if __name__ == '__main__':
#     os.environ['OPENAI_API_KEY'] = openaikey
#     os.environ["SERPAPI_API_KEY"] = serpapikey
#     main() 

# Imports
# import os
# from langchain.agents import load_tools
# from langchain.agents import initialize_agent
# from langchain.llms import OpenAI
# import streamlit as st 
# from langchain_community.chat_models import ChatOpenAI
# from apikey import serpapikey, openaikey

# def main():
#     # Streamlit page configuration
#     st.set_page_config(page_title='Serpapi Agent', layout='wide')

#     # CSS styling
#     css = """
#     <style>
#     body {
#         font-family: Arial, sans-serif;
#     }
#     .bot-message {
#         background-color: #f1f1f1;
#         border-radius: 10px;
#         padding: 10px;
#         margin-bottom: 10px;
#     }
#     .user-message {
#         background-color: #d1f1d1;
#         border-radius: 10px;
#         padding: 10px;
#         margin-bottom: 10px;
#         text-align: right;
#     }
#     </style>
#     """
#     st.write(css, unsafe_allow_html=True)

#     # HTML templates
#     bot_template = """
#     <div class="bot-message">
#         <p>{{MSG}}</p>
#     </div>
#     """
#     user_template = """
#     <div class="user-message">
#         <p>{{MSG}}</p>
#     </div>
#     """

#     # Initialize Session States
#     if 'generated' not in st.session_state: 
#         st.session_state['generated'] = []

#     if 'past' not in st.session_state: 
#         st.session_state['past'] = []

#     # Set up the Streamlit app layout
#     st.title("Intelligent Google Search ChatBot")
#     st.subheader("Powered by LangChain + OpenAI + Serpapi + Streamlit") 

#     # Define Language Model
#     llm = ChatOpenAI(model_name='gpt-3.5-turbo',
#                  temperature=0.9,
#                  max_tokens=256)
    
#     # Load in some tools to use - serpapi for google use and llm-math for math ops
#     tools = load_tools(["serpapi", "llm-math"], llm=llm)

#     # Initialize agent
#     agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

#     # Accept input from user
#     user_input = st.text_input("Enter your message:")  

#     # Submit Button Logic
#     if st.button("Submit") and user_input:
#         with st.spinner('Generating response...'):
#             try:
#                 # Generate response
#                 try:
#                     response = agent.invoke(user_input)
#                 except:
#                     response = "Sorry I am unable to answer your question"

#                 # Store conversation
#                 st.session_state.past.append(user_input)
#                 st.session_state.generated.append(response)

#                 # Display conversation
#                 for i in range(len(st.session_state.past)-1,-1,-1):
#                     st.write(bot_template.replace("{{MSG}}", st.session_state.generated[i]), unsafe_allow_html=True)
#                     st.write(user_template.replace("{{MSG}}", st.session_state.past[i]), unsafe_allow_html=True)
#                     st.write("")

#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")

# if __name__ == '__main__':
#     os.environ['OPENAI_API_KEY'] = openaikey
#     os.environ["SERPAPI_API_KEY"] = serpapikey
#     main()


# Imports
import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
import streamlit as st 
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI 
from langchain.chains import SequentialChain 
from langchain.agents import ChainToolkit


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
    toolkit = ChainToolkit()
    # Define Language Model
    llm = ChatOpenAI(model_name='gpt-3.5-turbo',
                 temperature=0.5,
                 max_tokens=256)
    
    # Load in some tools to use - serpapi for google use and llm-math for math ops
    tools = load_tools(["serpapi"], llm=llm) 
    # tools = load_tools(["llm-math"], llm=llm)

    # Prompt = "You are AI Bot specialized in gathering information about vehicles and cars. To provide you with the best solutions, ask some details about thier cars. According to the car please provide the Solution but first car model, name, milegae and basic information about cars then give the solution according to the car ?" 

    # Prompt = "You are an expert mechanic with extensive knowledge of vehicles and their problems. Your task is to resolve vehicle-related issues for any user by providing accurate answers based on your expertise. To do this, you need to gather detailed information about the vehicle from the user, including its specifications, model number, mileage, etc., through a series of questions. Based on the user's Query, you should offer solutions using the information available on the internet of that particular and provide actionable advice. If you are unable to provide a solution."

    # Initialize agent
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

    
    llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory, 
    )

    # Accept input from user
    user_input = st.text_input("Enter your message:")  
    toolkit.add_tool(name="chain", tool=llm_chain)
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
