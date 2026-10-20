LangGraph Complete Project: Basic to Advanced
A hands-on Python project for learning LangGraph in VS Code, from simple state graphs to tool-using agents, conversation checkpointing, human approval, structured output, and Retrieval-Augmented Generation (RAG).
Status: This README documents the nine learning examples described below. src/10_complete_assistant.py is a planned integration step, not a completed runnable script unless you implement it yourself.

Table of Contents
- Project Goals
- Concepts Covered
- Project Structure
- Prerequisites
- Setup in VS Code on Windows
- Configure Groq
- Run the Examples
- RAG Data Setup
- Run Tests
- Troubleshooting
- Security Notes
- Official Documentation
Project Goals
By completing this project, you will learn how to:
1. Model a workflow as a graph.
2. Define state, nodes, edges, and graph entry/exit points.
3. Route work with conditional edges.
4. Combine state updates using reducers.
5. Build an LLM agent that can call tools.
6. Preserve conversation state using checkpointing and thread IDs.
7. Stream graph events and updates.
8. Pause a workflow for human approval.
9. request structured output using Pydantic.
10. Build a basic RAG workflow using local embeddings and Chroma.
Concepts Covered
Example	Main concepts	Groq API required?
01_basic_graph.py	StateGraph, TypedDict, nodes, edges, START, END, compile(), invoke()	No
02_conditional_routing.py	Conditional edges and routing	No
03_reducers_and_loops.py	State reducers and combining updates	No
04_agent_with_tools.py	Groq chat model, @tool, bind_tools, ToolNode, tools_condition	Yes
05_memory_and_threads.py	MessagesState, checkpointers, thread_id	Yes
06_streaming.py	Streaming graph updates	Yes, with the example setup
07_human_approval.py	interrupt(), Command(resume=...), approval workflow	No
08_structured_output.py	Pydantic schema and structured model output	Yes
09_rag_workflow.py	Document loading, chunking, embeddings, Chroma, retrieval, generation	Yes, plus first-run embedding download


Project Structure
Create this structure in your project root:
langgraph-complete-project/
├── src/
│   ├── __init__.py
│   ├── 01_basic_graph.py
│   ├── 02_conditional_routing.py
│   ├── 03_reducers_and_loops.py
│   ├── 04_agent_with_tools.py
│   ├── 05_memory_and_threads.py
│   ├── 06_streaming.py
│   ├── 07_human_approval.py
│   ├── 08_structured_output.py
│   └── 09_rag_workflow.py
├── data/
│   └── langgraph_notes.txt
├── tests/
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
Do not commit .env to version control. The .env.example file should contain placeholders only.
Prerequisites
- Windows 10/11
- Visual Studio Code
- Python 3.11 or 3.12 recommended for broad package compatibility
- Internet connection for package installation, Groq API calls, and the first embedding-model download
- A Groq API key for the LLM examples
Check installed Python versions in PowerShell:
py --list
If Python 3.11 is installed, create the environment with py -3.11. Otherwise, use an installed Python version supported by the dependencies.
Setup in VS Code on Windows
1. Open the project folder
Open the project folder in VS Code. Open Terminal → New Terminal, then change directory to the project root. Example:
cd "D:\New folder\Gen_AI\langgraph-complete-project"
Replace the example path with your actual path.
2. Create a virtual environment
py -3.11 -m venv .venv
If Python 3.11 is unavailable, substitute an installed supported version, for example:
py -3.12 -m venv .venv
3. Activate the environment
.\.venv\Scripts\Activate.ps1
If PowerShell blocks activation, allow it for the current terminal process only:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
You should see (.venv) in the terminal prompt.
4. Select the Python interpreter in VS Code
1. Press Ctrl+Shift+P.
2. Search for Python: Select Interpreter.
3. Choose the interpreter inside this project: .venv\Scripts\python.exe.
5. Install dependencies
Make sure requirements.txt exists in the project root. Then run:
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Using python -m pip helps ensure that pip belongs to the active Python environment.
The example dependency list is:
langgraph
langchain-core
langchain-groq
python-dotenv
pydantic
pytest
langchain-community
langchain-text-splitters
langchain-chroma
langchain-huggingface
sentence-transformers
typing-extensions
If you update dependencies, consider pinning tested versions for reproducible installations. Package APIs and supported model names can change over time.
Configure Groq
Create a .env file in the project root:
GROQ_API_KEY=replace_with_your_actual_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
Replace the API key placeholder with your own key. Confirm that the configured model ID is currently supported by your Groq account; if not, use a currently available chat model.
Create .env.example with placeholders only:
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=your_supported_groq_model
Make sure .gitignore contains:
.venv/
__pycache__/
*.py[cod]
.env
.pytest_cache/
chroma_db/
Never upload your real API key to GitHub or paste it into public logs.
Run the Examples
Run commands from the project root, with the virtual environment activated.
1. Basic graph
python src/01_basic_graph.py
Learn how state moves through nodes connected by edges. This example does not need a Groq API key.
2. Conditional routing
python src/02_conditional_routing.py
A router selects a path based on the current state.
3. Reducers and state updates
python src/03_reducers_and_loops.py
Learn how Annotated reducers combine updates. Despite the filename, the basic example demonstrates sequential state updates; implement a conditional cycle to practise loops.
4. AI agent with tools
python src/04_agent_with_tools.py
Enter a question such as:
What is 125 multiplied by 8?
This example uses a Groq model and tools such as a calculator. The model decides whether to call a tool; a tool call is not guaranteed for every prompt.
5. Memory and conversation threads
python src/05_memory_and_threads.py
The example uses an in-memory checkpointer and thread IDs to separate conversations. The in-memory checkpoint store is for learning and does not survive process restarts.
6. Streaming
python src/06_streaming.py
This example demonstrates graph update streaming. If it imports graph from the memory example, ensure the graph setup is available in the file or factor the shared graph into a separate module. stream_mode="updates" reports node updates, not necessarily individual text tokens.
7. Human approval
python src/07_human_approval.py
The graph pauses for a decision and resumes using Command(resume=...). The example prints a proposed action; it does not actually send an email or perform an external action.
8. Structured output
python src/08_structured_output.py
The model returns a structured result described by a Pydantic model. The selected Groq model must support the structured-output method used by the code.
9. RAG workflow
First, create data/langgraph_notes.txt and add some text about LangGraph, your project notes, or another topic you want to query. Then run:
python src/09_rag_workflow.py
On the first run, the embedding model may need to download and can take time. The workflow creates a local chroma_db/ directory. If you change or replace documents, implement a re-indexing strategy or remove the local database before rebuilding it to avoid stale chunks.
RAG Data Setup
Create the data directory if it does not exist. Add one or more .txt files, for example:
data/
└── langgraph_notes.txt
The RAG script follows this flow:
1. Load .txt documents.
2. Split text into overlapping chunks.
3. Generate embeddings using a local sentence-transformer model.
4. Store and search vectors with Chroma.
5. Retrieve the top matching chunks.
6. Pass the retrieved context and question to Groq.
7. Print the answer and retrieved excerpts.
This is a learning implementation. Before production use, add source metadata and citations, document update/deduplication logic, retrieval evaluation, access controls, and monitoring. A generated answer can still be wrong even when context is provided.
Run Tests
Add src/__init__.py and create tests under tests/. Example:
python -m pytest -q
For a basic-graph test, the module must be importable and should not prompt for input during import. Python cannot import a module using a filename that begins with a number using ordinary dotted import syntax, so either rename 01_basic_graph.py to basic_graph.py or load it using another supported approach.
Prefer unit tests for deterministic graph nodes. Keep tests that call Groq or download embedding models separate from quick offline tests.
Troubleshooting
ModuleNotFoundError
Check that the virtual environment is activated and dependencies were installed:
python -m pip install -r requirements.txt
python -c "import langgraph; print('LangGraph import OK')"
pip launcher points to a different Python path
Use:
python -m pip --version
python -m pip install -r requirements.txt
If the virtual environment was moved from another folder, recreate it rather than relying on old launcher paths.
Groq authentication or model error
- Check that .env is in the project root.
- Confirm the API key is valid and available to the account.
- Confirm the model ID is currently supported.
- Do not share the API key when asking for help.
Tool does not run
Inspect the assistant message's tool_calls, verify tool descriptions, and confirm that tools_condition routes to ToolNode. The model can choose to answer without calling a tool.
Memory seems to disappear
Use the same checkpointer instance and the same thread_id for the same conversation. An in-memory checkpointer is lost when the process ends.
RAG returns poor answers or old content
Inspect the retrieved chunks before the generated answer. Check that the intended documents were loaded and that the vector database was re-indexed after document changes. Experiment with chunk size, overlap, embedding model, and retrieval count.
Embedding model download fails
Check internet access and available disk space. The first run of sentence-transformers/all-MiniLM-L6-v2 needs the model files unless they are already cached locally.
Security Notes
- Never commit .env or API credentials.
- Treat retrieved documents and tool outputs as untrusted input.
- Require human approval before consequential external actions.
- Limit tool permissions and validate tool arguments.
- Do not expose private conversation state across thread IDs or users.
- Use persistent, access-controlled checkpoint storage for production systems.
Official Documentation
- LangGraph Python overview
- LangChain models
- Groq API documentation
- Chroma documentation
- Pydantic documentation
Suggested Learning Path
Complete the examples in order. First understand deterministic graphs and routing. Then add Groq and tool calling, followed by checkpointing, streaming, interrupts, structured output, and RAG. Once each part works independently, integrate them into a single assistant with a shared state schema and tests.
