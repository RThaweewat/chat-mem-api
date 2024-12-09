from typing import Sequence, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, RemoveMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import Annotated

from src.config import OPENAI_API_KEY
from src.services.observatory import opik_tracer
from src.services.prompt_loader import formatted_prompt
from src.services.vectorstore import vectorstore


class ConversationState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    question: str


workflow = StateGraph(state_schema=ConversationState)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=OPENAI_API_KEY,
    temperature=0,
    max_tokens=None,
    timeout=30,
    max_retries=3,
)

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            formatted_prompt
        ),
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)
print(prompt)


def call_model(state: ConversationState):
    """
    Calls the language model with the provided conversation state to generate a
    response based on the user's question and relevant context documents. The function
    retrieves relevant documents based on similarity to the user's question, constructs
    an input dictionary, and invokes the language model to generate a response.

    :param state: A dictionary representing the current conversation state, including
                  a "question" key for the user's question and a "messages" key for the
                  conversation history.
    :type state: ConversationState
    :return: A dictionary containing a "messages" key with the updated conversation
             history, including the response from the language model.
    :rtype: dict
    """
    user_question = state["question"]
    docs = vectorstore.similarity_search(user_question, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    input_dict = {
        "messages": state["messages"],
        "question": user_question,
        "context": context,
    }

    response = (prompt | llm).invoke(input_dict, config={"callbacks": [opik_tracer]})
    return {
        "messages": [response]
    }


# Add nodes to the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Set up memory (persistence)
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def handle_chat(query: str, thread_id: str = "default_thread"):
    """
    Handle a chat interaction with the AI application by sending a query and
    receiving a response. This function utilizes an AI model to process the input
    messages, configurable with a thread ID to maintain state or context if needed.

    It invokes the AI application with the provided query, processes the
    output messages, and returns the response from the AI if available. If
    the AI does not provide a message back, it returns a default "No response".

    :param query: The input query string to send to the AI for processing.
    :type query: str
    :param thread_id: Identifier for maintaining thread-specific context.
                      Defaults to "default_thread".
    :type thread_id: str, optional
    :return: The response from the AI model or a default message if no response
             is provided.
    :rtype: str
    """
    config = {"configurable": {"thread_id": thread_id}}
    output = app.invoke({"messages": [HumanMessage(content=query)], "question": query}, config)
    messages = output["messages"]
    ai_message = messages[-1] if messages else None
    if ai_message and isinstance(ai_message, AIMessage):
        return ai_message.content
    return "No response"


def reset_conversation(thread_id: str = "default_thread"):
    """
    Resets the conversation state by deleting all messages associated
    with the specified thread ID. This operation updates the state of
    the application to reflect the absence of any previous conversation
    history.

    :param thread_id: Identifier for the thread whose conversation state
                      is to be reset. Defaults to 'default_thread'.
    :type thread_id: str
    :return: None
    """
    # Get the current state messages
    config = {"configurable": {"thread_id": thread_id}}
    messages = app.get_state(config).values.get("messages", [])

    # Create a list of RemoveMessage instances for each message in the state
    remove_messages = [RemoveMessage(id=msg.id) for msg in messages] if messages else []

    # Update the state to remove the messages
    app.update_state(config, {"messages": remove_messages})
