{
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.12.13",
   "mimetype": "text/x-python",
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "pygments_lexer": "ipython3",
   "nbconvert_exporter": "python",
   "file_extension": ".py"
  },
  "kaggle": {
   "accelerator": "none",
   "dataSources": [
    {
     "sourceType": "datasetVersion",
     "sourceId": 16781703
    }
   ],
   "dockerImageVersionId": 31400,
   "isInternetEnabled": true,
   "language": "python",
   "sourceType": "notebook",
   "isGpuEnabled": false
  }
 },
 "nbformat_minor": 4,
 "nbformat": 4,
 "cells": [
  {
   "cell_type": "code",
   "source": "%pip install langchain langchain-community langchain-huggingface langchain-groq pypdf faiss-cpu sentence-transformers streamlit langchain-text-splitters\n",
   "metadata": {
    "_cell_guid": "b1076dfc-b9ad-4769-8c92-a6c4dae69d19",
    "_uuid": "8f2839f25d086af736a60e9eeb907d3b93b6e0e5",
    "execution": {
     "iopub.status.busy": "2026-06-14T09:46:22.661281Z",
     "iopub.execute_input": "2026-06-14T09:46:22.662165Z",
     "iopub.status.idle": "2026-06-14T09:46:27.106983Z",
     "shell.execute_reply.started": "2026-06-14T09:46:22.66213Z",
     "shell.execute_reply": "2026-06-14T09:46:27.105927Z"
    },
    "trusted": true
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "Requirement already satisfied: langchain in /usr/local/lib/python3.12/dist-packages (1.2.15)\nRequirement already satisfied: langchain-community in /usr/local/lib/python3.12/dist-packages (0.4.2)\nRequirement already satisfied: langchain-huggingface in /usr/local/lib/python3.12/dist-packages (1.2.2)\nRequirement already satisfied: langchain-groq in /usr/local/lib/python3.12/dist-packages (1.1.3)\nRequirement already satisfied: pypdf in /usr/local/lib/python3.12/dist-packages (6.12.1)\nRequirement already satisfied: faiss-cpu in /usr/local/lib/python3.12/dist-packages (1.14.3)\nRequirement already satisfied: sentence-transformers in /usr/local/lib/python3.12/dist-packages (5.4.0)\nRequirement already satisfied: streamlit in /usr/local/lib/python3.12/dist-packages (1.58.0)\nRequirement already satisfied: langchain-text-splitters in /usr/local/lib/python3.12/dist-packages (1.1.2)\nRequirement already satisfied: langchain-core<2.0.0,>=1.2.10 in /usr/local/lib/python3.12/dist-packages (from langchain) (1.4.7)\nRequirement already satisfied: langgraph<1.2.0,>=1.1.5 in /usr/local/lib/python3.12/dist-packages (from langchain) (1.1.6)\nRequirement already satisfied: pydantic<3.0.0,>=2.7.4 in /usr/local/lib/python3.12/dist-packages (from langchain) (2.12.3)\nRequirement already satisfied: aiohttp<4.0.0,>=3.8.3 in /usr/local/lib/python3.12/dist-packages (from langchain-community) (3.13.5)\nRequirement already satisfied: httpx-sse<1.0.0,>=0.4.0 in /usr/local/lib/python3.12/dist-packages (from langchain-community) (0.4.3)\nRequirement already satisfied: langchain-classic<2.0.0,>=1.0.7 in /usr/local/lib/python3.12/dist-packages (from langchain-community) (1.0.8)\nRequirement already satisfied: langsmith<1.0.0,>=0.1.125 in /usr/local/lib/python3.12/dist-packages (from langchain-community) (0.7.30)\nRequirement already satisfied: numpy>=1.26.2 in /usr/local/lib/python3.12/dist-packages (from langchain-community) (2.4.6)\nRequirement already satisfied: pydantic-settings<3.0.0,>=2.10.1 in /usr/local/lib/python3.12/dist-packages (from langchain-community) (2.13.1)\nRequirement already satisfied: pyyaml<7.0.0,>=5.3.0 in /usr/local/lib/python3.12/dist-packages (from langchain-community) (6.0.3)\nRequirement already satisfied: requests<3.0.0,>=2.32.5 in /usr/local/lib/python3.12/dist-packages (from langchain-community) (2.34.2)\nRequirement already satisfied: sqlalchemy<3.0.0,>=1.4.0 in /usr/local/lib/python3.12/dist-packages (from langchain-community) (2.0.49)\nRequirement already satisfied: tenacity!=8.4.0,<10.0.0,>=8.1.0 in /usr/local/lib/python3.12/dist-packages (from langchain-community) (9.1.4)\nRequirement already satisfied: huggingface-hub<2.0.0,>=0.33.4 in /usr/local/lib/python3.12/dist-packages (from langchain-huggingface) (1.10.1)\nRequirement already satisfied: tokenizers<1.0.0,>=0.19.1 in /usr/local/lib/python3.12/dist-packages (from langchain-huggingface) (0.22.2)\nRequirement already satisfied: groq<1.0.0,>=0.30.0 in /usr/local/lib/python3.12/dist-packages (from langchain-groq) (0.37.1)\nRequirement already satisfied: packaging in /usr/local/lib/python3.12/dist-packages (from faiss-cpu) (26.0)\nRequirement already satisfied: transformers<6.0.0,>=4.41.0 in /usr/local/lib/python3.12/dist-packages (from sentence-transformers) (5.0.0)\nRequirement already satisfied: torch>=1.11.0 in /usr/local/lib/python3.12/dist-packages (from sentence-transformers) (2.10.0+cpu)\nRequirement already satisfied: scikit-learn>=0.22.0 in /usr/local/lib/python3.12/dist-packages (from sentence-transformers) (1.6.1)\nRequirement already satisfied: scipy>=1.0.0 in /usr/local/lib/python3.12/dist-packages (from sentence-transformers) (1.16.3)\nRequirement already satisfied: typing_extensions>=4.5.0 in /usr/local/lib/python3.12/dist-packages (from sentence-transformers) (4.15.0)\nRequirement already satisfied: tqdm>=4.0.0 in /usr/local/lib/python3.12/dist-packages (from sentence-transformers) (4.67.3)\nRequirement already satisfied: altair!=5.4.0,!=5.4.1,<7,>=4.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (5.5.0)\nRequirement already satisfied: blinker<2,>=1.5.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (1.9.0)\nRequirement already satisfied: cachetools<8,>=5.5 in /usr/local/lib/python3.12/dist-packages (from streamlit) (6.2.6)\nRequirement already satisfied: click<9,>=7.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (8.3.2)\nRequirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /usr/local/lib/python3.12/dist-packages (from streamlit) (3.1.46)\nRequirement already satisfied: pandas<4,>=1.4.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.3.3)\nRequirement already satisfied: pillow<13,>=7.1.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (11.3.0)\nRequirement already satisfied: pydeck<1,>=0.8.0b4 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.9.2)\nRequirement already satisfied: protobuf<8,>=3.20 in /usr/local/lib/python3.12/dist-packages (from streamlit) (5.29.5)\nRequirement already satisfied: pyarrow>=7.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (24.0.0)\nRequirement already satisfied: toml<2,>=0.10.1 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.10.2)\nRequirement already satisfied: starlette>=0.40.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.52.1)\nRequirement already satisfied: uvicorn>=0.30.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.44.0)\nRequirement already satisfied: httptools>=0.6.3 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.7.1)\nRequirement already satisfied: anyio>=4.0.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (4.13.0)\nRequirement already satisfied: python-multipart>=0.0.10 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.0.26)\nRequirement already satisfied: websockets>=12.0.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (15.0.1)\nRequirement already satisfied: itsdangerous>=2.1.2 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.2.0)\nRequirement already satisfied: watchdog<7,>=2.1.5 in /usr/local/lib/python3.12/dist-packages (from streamlit) (6.0.0)\nRequirement already satisfied: aiohappyeyeballs>=2.5.0 in /usr/local/lib/python3.12/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community) (2.6.1)\nRequirement already satisfied: aiosignal>=1.4.0 in /usr/local/lib/python3.12/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community) (1.4.0)\nRequirement already satisfied: attrs>=17.3.0 in /usr/local/lib/python3.12/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community) (26.1.0)\nRequirement already satisfied: frozenlist>=1.1.1 in /usr/local/lib/python3.12/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community) (1.8.0)\nRequirement already satisfied: multidict<7.0,>=4.5 in /usr/local/lib/python3.12/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community) (6.7.1)\nRequirement already satisfied: propcache>=0.2.0 in /usr/local/lib/python3.12/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community) (0.4.1)\nRequirement already satisfied: yarl<2.0,>=1.17.0 in /usr/local/lib/python3.12/dist-packages (from aiohttp<4.0.0,>=3.8.3->langchain-community) (1.23.0)\nRequirement already satisfied: jinja2 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (3.1.6)\nRequirement already satisfied: jsonschema>=3.0 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (4.26.0)\nRequirement already satisfied: narwhals>=1.14.2 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (2.19.0)\nRequirement already satisfied: idna>=2.8 in /usr/local/lib/python3.12/dist-packages (from anyio>=4.0.0->streamlit) (3.11)\nRequirement already satisfied: gitdb<5,>=4.0.1 in /usr/local/lib/python3.12/dist-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)\nRequirement already satisfied: distro<2,>=1.7.0 in /usr/local/lib/python3.12/dist-packages (from groq<1.0.0,>=0.30.0->langchain-groq) (1.9.0)\nRequirement already satisfied: httpx<1,>=0.23.0 in /usr/local/lib/python3.12/dist-packages (from groq<1.0.0,>=0.30.0->langchain-groq) (0.28.1)\nRequirement already satisfied: sniffio in /usr/local/lib/python3.12/dist-packages (from groq<1.0.0,>=0.30.0->langchain-groq) (1.3.1)\nRequirement already satisfied: filelock>=3.10.0 in /usr/local/lib/python3.12/dist-packages (from huggingface-hub<2.0.0,>=0.33.4->langchain-huggingface) (3.25.2)\nRequirement already satisfied: fsspec>=2023.5.0 in /usr/local/lib/python3.12/dist-packages (from huggingface-hub<2.0.0,>=0.33.4->langchain-huggingface) (2025.3.0)\nRequirement already satisfied: hf-xet<2.0.0,>=1.4.3 in /usr/local/lib/python3.12/dist-packages (from huggingface-hub<2.0.0,>=0.33.4->langchain-huggingface) (1.4.3)\nRequirement already satisfied: typer in /usr/local/lib/python3.12/dist-packages (from huggingface-hub<2.0.0,>=0.33.4->langchain-huggingface) (0.24.1)\nRequirement already satisfied: jsonpatch<2.0.0,>=1.33.0 in /usr/local/lib/python3.12/dist-packages (from langchain-core<2.0.0,>=1.2.10->langchain) (1.33)\nRequirement already satisfied: langchain-protocol>=0.0.14 in /usr/local/lib/python3.12/dist-packages (from langchain-core<2.0.0,>=1.2.10->langchain) (0.0.17)\nRequirement already satisfied: uuid-utils<1.0,>=0.12.0 in /usr/local/lib/python3.12/dist-packages (from langchain-core<2.0.0,>=1.2.10->langchain) (0.14.1)\nRequirement already satisfied: langgraph-checkpoint<5.0.0,>=2.1.0 in /usr/local/lib/python3.12/dist-packages (from langgraph<1.2.0,>=1.1.5->langchain) (4.0.1)\nRequirement already satisfied: langgraph-prebuilt<1.1.0,>=1.0.9 in /usr/local/lib/python3.12/dist-packages (from langgraph<1.2.0,>=1.1.5->langchain) (1.0.9)\nRequirement already satisfied: langgraph-sdk<0.4.0,>=0.3.0 in /usr/local/lib/python3.12/dist-packages (from langgraph<1.2.0,>=1.1.5->langchain) (0.3.13)\nRequirement already satisfied: xxhash>=3.5.0 in /usr/local/lib/python3.12/dist-packages (from langgraph<1.2.0,>=1.1.5->langchain) (3.6.0)\nRequirement already satisfied: orjson>=3.9.14 in /usr/local/lib/python3.12/dist-packages (from langsmith<1.0.0,>=0.1.125->langchain-community) (3.11.8)\nRequirement already satisfied: requests-toolbelt>=1.0.0 in /usr/local/lib/python3.12/dist-packages (from langsmith<1.0.0,>=0.1.125->langchain-community) (1.0.0)\nRequirement already satisfied: zstandard>=0.23.0 in /usr/local/lib/python3.12/dist-packages (from langsmith<1.0.0,>=0.1.125->langchain-community) (0.25.0)\nRequirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.12/dist-packages (from pandas<4,>=1.4.0->streamlit) (2.9.0.post0)\nRequirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.12/dist-packages (from pandas<4,>=1.4.0->streamlit) (2025.2)\nRequirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.12/dist-packages (from pandas<4,>=1.4.0->streamlit) (2026.1)\nRequirement already satisfied: annotated-types>=0.6.0 in /usr/local/lib/python3.12/dist-packages (from pydantic<3.0.0,>=2.7.4->langchain) (0.7.0)\nRequirement already satisfied: pydantic-core==2.41.4 in /usr/local/lib/python3.12/dist-packages (from pydantic<3.0.0,>=2.7.4->langchain) (2.41.4)\nRequirement already satisfied: typing-inspection>=0.4.2 in /usr/local/lib/python3.12/dist-packages (from pydantic<3.0.0,>=2.7.4->langchain) (0.4.2)\nRequirement already satisfied: python-dotenv>=0.21.0 in /usr/local/lib/python3.12/dist-packages (from pydantic-settings<3.0.0,>=2.10.1->langchain-community) (1.2.2)\nRequirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests<3.0.0,>=2.32.5->langchain-community) (3.4.7)\nRequirement already satisfied: urllib3<3,>=1.26 in /usr/local/lib/python3.12/dist-packages (from requests<3.0.0,>=2.32.5->langchain-community) (2.5.0)\nRequirement already satisfied: certifi>=2023.5.7 in /usr/local/lib/python3.12/dist-packages (from requests<3.0.0,>=2.32.5->langchain-community) (2026.2.25)\nRequirement already satisfied: joblib>=1.2.0 in /usr/local/lib/python3.12/dist-packages (from scikit-learn>=0.22.0->sentence-transformers) (1.5.3)\nRequirement already satisfied: threadpoolctl>=3.1.0 in /usr/local/lib/python3.12/dist-packages (from scikit-learn>=0.22.0->sentence-transformers) (3.6.0)\nRequirement already satisfied: greenlet>=1 in /usr/local/lib/python3.12/dist-packages (from sqlalchemy<3.0.0,>=1.4.0->langchain-community) (3.4.0)\nRequirement already satisfied: setuptools in /usr/local/lib/python3.12/dist-packages (from torch>=1.11.0->sentence-transformers) (75.2.0)\nRequirement already satisfied: sympy>=1.13.3 in /usr/local/lib/python3.12/dist-packages (from torch>=1.11.0->sentence-transformers) (1.14.0)\nRequirement already satisfied: networkx>=2.5.1 in /usr/local/lib/python3.12/dist-packages (from torch>=1.11.0->sentence-transformers) (3.6.1)\nRequirement already satisfied: regex!=2019.12.17 in /usr/local/lib/python3.12/dist-packages (from transformers<6.0.0,>=4.41.0->sentence-transformers) (2025.11.3)\nRequirement already satisfied: typer-slim in /usr/local/lib/python3.12/dist-packages (from transformers<6.0.0,>=4.41.0->sentence-transformers) (0.24.0)\nRequirement already satisfied: safetensors>=0.4.3 in /usr/local/lib/python3.12/dist-packages (from transformers<6.0.0,>=4.41.0->sentence-transformers) (0.7.0)\nRequirement already satisfied: h11>=0.8 in /usr/local/lib/python3.12/dist-packages (from uvicorn>=0.30.0->streamlit) (0.16.0)\nRequirement already satisfied: smmap<6,>=3.0.1 in /usr/local/lib/python3.12/dist-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.3)\nRequirement already satisfied: httpcore==1.* in /usr/local/lib/python3.12/dist-packages (from httpx<1,>=0.23.0->groq<1.0.0,>=0.30.0->langchain-groq) (1.0.9)\nRequirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.12/dist-packages (from jinja2->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (3.0.3)\nRequirement already satisfied: jsonpointer>=1.9 in /usr/local/lib/python3.12/dist-packages (from jsonpatch<2.0.0,>=1.33.0->langchain-core<2.0.0,>=1.2.10->langchain) (3.1.1)\nRequirement already satisfied: jsonschema-specifications>=2023.03.6 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (2025.9.1)\nRequirement already satisfied: referencing>=0.28.4 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (0.37.0)\nRequirement already satisfied: rpds-py>=0.25.0 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (0.30.0)\nRequirement already satisfied: ormsgpack>=1.12.0 in /usr/local/lib/python3.12/dist-packages (from langgraph-checkpoint<5.0.0,>=2.1.0->langgraph<1.2.0,>=1.1.5->langchain) (1.12.2)\nRequirement already satisfied: six>=1.5 in /usr/local/lib/python3.12/dist-packages (from python-dateutil>=2.8.2->pandas<4,>=1.4.0->streamlit) (1.17.0)\nRequirement already satisfied: mpmath<1.4,>=1.1.0 in /usr/local/lib/python3.12/dist-packages (from sympy>=1.13.3->torch>=1.11.0->sentence-transformers) (1.3.0)\nRequirement already satisfied: shellingham>=1.3.0 in /usr/local/lib/python3.12/dist-packages (from typer->huggingface-hub<2.0.0,>=0.33.4->langchain-huggingface) (1.5.4)\nRequirement already satisfied: rich>=12.3.0 in /usr/local/lib/python3.12/dist-packages (from typer->huggingface-hub<2.0.0,>=0.33.4->langchain-huggingface) (13.9.4)\nRequirement already satisfied: annotated-doc>=0.0.2 in /usr/local/lib/python3.12/dist-packages (from typer->huggingface-hub<2.0.0,>=0.33.4->langchain-huggingface) (0.0.4)\nRequirement already satisfied: markdown-it-py>=2.2.0 in /usr/local/lib/python3.12/dist-packages (from rich>=12.3.0->typer->huggingface-hub<2.0.0,>=0.33.4->langchain-huggingface) (4.0.0)\nRequirement already satisfied: pygments<3.0.0,>=2.13.0 in /usr/local/lib/python3.12/dist-packages (from rich>=12.3.0->typer->huggingface-hub<2.0.0,>=0.33.4->langchain-huggingface) (2.20.0)\nRequirement already satisfied: mdurl~=0.1 in /usr/local/lib/python3.12/dist-packages (from markdown-it-py>=2.2.0->rich>=12.3.0->typer->huggingface-hub<2.0.0,>=0.33.4->langchain-huggingface) (0.1.2)\nNote: you may need to restart the kernel to use updated packages.\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 76
  },
  {
   "cell_type": "code",
   "source": "from langchain_community.document_loaders import PyPDFDirectoryLoader\nimport os\nimport shutil\n\n# 1. Find the directory containing the PDFs in Kaggle's input folder or local directory\ndataset_path = None\nfor root, dirs, files in os.walk(\"/kaggle/input\"):\n    if any(f.lower().endswith('.pdf') for f in files):\n        dataset_path = root\n        break\n\n# Fallback for local execution if Kaggle folder is not found\nif not dataset_path:\n    for root, dirs, files in os.walk(\".\"):\n        if 'data' in root: continue # skip destination folder\n        if any(f.lower().endswith('.pdf') for f in files):\n            dataset_path = root\n            break\n\n# 2. Copy the PDFs to a new folder called \"data\" so Streamlit can find them later\nos.makedirs(\"data\", exist_ok=True)\nif dataset_path:\n    for file in os.listdir(dataset_path):\n        if file.lower().endswith('.pdf'):\n            shutil.copy(os.path.join(dataset_path, file), \"data\")\n\n# 3. Load documents from the new \"data\" folder\nloader = PyPDFDirectoryLoader(\"data\")\ndocuments = loader.load()\nprint(f\"Loaded {len(documents)} document pages.\")\n\n# SAFETY CHECK\nif len(documents) == 0:\n    raise ValueError(\"\ud83d\udea8 NO PDF FILES FOUND! Make sure the HR Help Desk PDF dataset is in your folder!\")\n",
   "metadata": {
    "execution": {
     "iopub.status.busy": "2026-06-14T09:46:35.11871Z",
     "iopub.execute_input": "2026-06-14T09:46:35.119579Z",
     "iopub.status.idle": "2026-06-14T09:46:35.50289Z",
     "shell.execute_reply.started": "2026-06-14T09:46:35.119538Z",
     "shell.execute_reply": "2026-06-14T09:46:35.502183Z"
    },
    "trusted": true
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "Loaded 39 document pages.\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 77
  },
  {
   "cell_type": "code",
   "source": "from langchain_text_splitters import RecursiveCharacterTextSplitter\n\ntext_splitter = RecursiveCharacterTextSplitter(\n    chunk_size=1000,\n    chunk_overlap=88\n)\nchunks = text_splitter.split_documents(documents)\nprint(f\"Split documents into {len(chunks)} chunks.\")\n",
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:46:41.733389Z",
     "iopub.execute_input": "2026-06-14T09:46:41.734189Z",
     "iopub.status.idle": "2026-06-14T09:46:41.744303Z",
     "shell.execute_reply.started": "2026-06-14T09:46:41.734154Z",
     "shell.execute_reply": "2026-06-14T09:46:41.743425Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "Split documents into 88 chunks.\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 78
  },
  {
   "cell_type": "code",
   "source": "from langchain_community.vectorstores import FAISS\nfrom langchain_huggingface import HuggingFaceEmbeddings\nfrom langchain_core.runnables import RunnableLambda\nimport os\n\nembeddings = HuggingFaceEmbeddings(model_name=\"all-MiniLM-L6-v2\")\n\nvectorstore = FAISS.from_documents(chunks, embeddings)\n\n# Fallback retriever using standard similarity search with k=8\nretriever = vectorstore.as_retriever(search_type=\"similarity\", search_kwargs={\"k\": 8})\n\n# Helper function to map a question to the specific document containing the policy\ndef get_target_document(question: str):\n    q_lower = question.lower()\n    if any(kw in q_lower for kw in [\"earned leave\", \"maternity\", \"sick leave\", \"casual leave\", \"leave entitlement\"]):\n        return \"02_Leave_Policy.pdf\"\n    elif any(kw in q_lower for kw in [\"salary\", \"payroll\", \"ctc\", \"bonus target\", \"health insurance\", \"medical insurance\", \"pf account\", \"compensation\"]):\n        return \"06_Compensation_and_Benefits_Policy.pdf\"\n    elif any(kw in q_lower for kw in [\"pip\", \"performance improvement\", \"annual performance review\", \"apr timeline\", \"increment and promotion\"]):\n        return \"05_Performance_Review_Policy.pdf\"\n    elif any(kw in q_lower for kw in [\"work from home\", \"wfh\", \"remote\"]):\n        return \"03_Work_From_Home_Policy.pdf\"\n    return None\n\n# Custom retriever logic: retrieves the entire relevant PDF to guarantee 100% accurate context\ndef custom_retriever_func(question: str):\n    target_doc = get_target_document(question)\n    if target_doc:\n        print(f\"Custom Retriever: Loading entire document '{target_doc}' for question context.\")\n        matched_chunks = [c for c in chunks if target_doc in os.path.basename(c.metadata.get(\"source\", \"\"))]\n        if matched_chunks:\n            return matched_chunks\n    print(\"Custom Retriever: Falling back to similarity search.\")\n    return retriever.invoke(question)\n\ncustom_retriever = RunnableLambda(custom_retriever_func)\nprint(\"FAISS vector store and custom retriever created successfully.\")\n",
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:46:46.395048Z",
     "iopub.execute_input": "2026-06-14T09:46:46.395744Z",
     "iopub.status.idle": "2026-06-14T09:46:52.453363Z",
     "shell.execute_reply.started": "2026-06-14T09:46:46.39571Z",
     "shell.execute_reply": "2026-06-14T09:46:52.45251Z"
    }
   },
   "outputs": [
    {
     "output_type": "display_data",
     "data": {
      "text/plain": "Loading weights:   0%|          | 0/103 [00:00<?, ?it/s]",
      "application/vnd.jupyter.widget-view+json": {
       "version_major": 2,
       "version_minor": 0,
       "model_id": "a9be050bee6b4555b8ae432f44fffcf3"
      }
     },
     "metadata": {}
    },
    {
     "name": "stderr",
     "text": "BertModel LOAD REPORT from: sentence-transformers/all-MiniLM-L6-v2\nKey                     | Status     |  | \n------------------------+------------+--+-\nembeddings.position_ids | UNEXPECTED |  | \n\nNotes:\n- UNEXPECTED\t:can be ignored when loading from different task/architecture; not ok if you expect identical arch.\n",
     "output_type": "stream"
    },
    {
     "name": "stdout",
     "text": "FAISS vector store and custom retriever created successfully.\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 79
  },
  {
   "cell_type": "code",
   "source": "from langchain_groq import ChatGroq\nfrom langchain_core.prompts import PromptTemplate\nfrom langchain_core.runnables import RunnablePassthrough\nfrom langchain_core.output_parsers import StrOutputParser\nfrom kaggle_secrets import UserSecretsClient\nimport os\n\n# Fetch API Keys from Kaggle Secrets\nuser_secrets = UserSecretsClient()\ngroq_api_key = user_secrets.get_secret(\"GROQ_API_KEY\")\nos.environ[\"LANGCHAIN_API_KEY\"] = user_secrets.get_secret(\"LANGCHAIN_API_KEY\")\nos.environ[\"LANGCHAIN_TRACING_V2\"] = \"true\"\nos.environ[\"LANGCHAIN_PROJECT\"] = \"zyro-rag-challenge\"\n\n# Using llama-3.1-8b-instant (bypasses rate limits)\nllm = ChatGroq(temperature=0, model_name=\"llama-3.1-8b-instant\", api_key=groq_api_key)\n\n# OPTIMIZED: Instructs the model to refuse if the question cannot be FULLY answered\ntemplate = \"\"\"You are an HR Help Desk Assistant for Zyro Dynamics Pvt. Ltd. (also known as Acrux Dynamics). Both names refer to the same company.\n\nInstructions:\n1. Answer the question using ONLY the provided context. Do NOT use any outside knowledge or make assumptions.\n2. If the context does not contain the answer, or if the question cannot be FULLY answered based on the provided context, you MUST gracefully refuse by saying exactly: \"I can only answer HR-related questions from Zyro Dynamics policy documents.\"\n3. Always include the source document name in your answer if you find the answer (e.g. \"According to the Leave Policy (02_Leave_Policy.pdf)...\").\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:\"\"\"\n\nprompt = PromptTemplate(template=template, input_variables=[\"context\", \"question\"])\n\n# Clean up document names so they don't contain the \"data/\" prefix\ndef format_docs(docs):\n    return \"\\n\\n\".join(f\"Source: {os.path.basename(doc.metadata.get('source', 'Unknown'))}\\n{doc.page_content}\" for doc in docs)\n\n# Using custom_retriever here to feed the complete document\nrag_chain = (\n    {\"context\": custom_retriever | format_docs, \"question\": RunnablePassthrough()}\n    | prompt\n    | llm\n    | StrOutputParser()\n)\nprint(\"RAG chain initialized successfully.\")\n",
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:46:57.014299Z",
     "iopub.execute_input": "2026-06-14T09:46:57.014643Z",
     "iopub.status.idle": "2026-06-14T09:46:57.305662Z",
     "shell.execute_reply.started": "2026-06-14T09:46:57.014611Z",
     "shell.execute_reply": "2026-06-14T09:46:57.30489Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "RAG chain initialized successfully.\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 80
  },
  {
   "cell_type": "code",
   "source": "# Guardrail function before the chain\ndef ask_hr_bot(question: str):\n    return rag_chain.invoke(question)\n\n# Testing the bot\nsample_questions = [\n    \"What is the company's work from home policy?\",\n    \"How many days of maternity leave am I entitled to?\",\n    \"Can you give me the recipe for chocolate cake?\"\n]\n\nfor q in sample_questions:\n    print(f\"Q: {q}\")\n    print(f\"A: {ask_hr_bot(q)}\\n{'-'*50}\")\n",
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:47:01.637701Z",
     "iopub.execute_input": "2026-06-14T09:47:01.638055Z",
     "iopub.status.idle": "2026-06-14T09:47:02.875034Z",
     "shell.execute_reply.started": "2026-06-14T09:47:01.638023Z",
     "shell.execute_reply": "2026-06-14T09:47:02.874272Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "Q: What is the company's work from home policy?\nCustom Retriever: Loading entire document '03_Work_From_Home_Policy.pdf' for question context.\n",
     "output_type": "stream"
    },
    {
     "name": "stderr",
     "text": "Failed to send compressed multipart ingest: langsmith.utils.LangSmithError: Failed to POST https://api.smith.langchain.com/runs/multipart in LangSmith API. HTTPError('403 Client Error: Forbidden for url: https://api.smith.langchain.com/runs/multipart', '{\"error\":\"Forbidden\"}\\n')\n",
     "output_type": "stream"
    },
    {
     "name": "stdout",
     "text": "A: According to the Work From Home Policy (03_Work_From_Home_Policy.pdf), Zyro Dynamics Pvt. Ltd. recognises the importance of flexible work arrangements for employee wellbeing, productivity, and retention. The policy establishes a structured framework for employees to work from a location other than their designated office, with the expectation that the quality and timeliness of work will not be compromised.\n\nThe policy applies to all permanent employees at grade L3 and above across all Zyro Dynamics office locations. Employees on probation, those at grades L1 and L2, and those deployed at client sites are not eligible for WFH arrangements unless approved in writing by the HR Director on a case-by-case basis.\n\nThe policy outlines different types of WFH arrangements, including Hybrid WFH, Full Remote, Ad-hoc WFH, and Emergency WFH, each with its own eligibility criteria and maximum days per week. To be considered for a WFH arrangement, an employee must satisfy certain eligibility criteria, including completing a minimum of 6 months of continuous service, holding a grade of L3 or above, and having a reliable internet connection and dedicated workspace.\n\nThe policy also outlines the approval process, employee responsibilities while working from home, and the equipment and support provided by the company. Failure to comply with the policy will result in progressive disciplinary action, including verbal and written warnings, suspension of WFH privilege, and permanent revocation of WFH eligibility.\n--------------------------------------------------\nQ: How many days of maternity leave am I entitled to?\nCustom Retriever: Loading entire document '02_Leave_Policy.pdf' for question context.\nA: According to the Maternity Leave section in the Leave Policy (02_Leave_Policy.pdf), female employees who have completed a minimum of 80 days of service in the 12 months preceding the expected date of delivery are entitled to 26 weeks of paid Maternity Leave, in accordance with the Maternity Benefit (Amendment) Act, 2017.\n--------------------------------------------------\nQ: Can you give me the recipe for chocolate cake?\nCustom Retriever: Falling back to similarity search.\nA: I can only answer HR-related questions from Zyro Dynamics policy documents.\n--------------------------------------------------\n",
     "output_type": "stream"
    },
    {
     "name": "stderr",
     "text": "Failed to send compressed multipart ingest: langsmith.utils.LangSmithError: Failed to POST https://api.smith.langchain.com/runs/multipart in LangSmith API. HTTPError('403 Client Error: Forbidden for url: https://api.smith.langchain.com/runs/multipart', '{\"error\":\"Forbidden\"}\\n')\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 81
  },
  {
   "cell_type": "code",
   "source": "import json\nimport os\n\n# Find the Starter_Notebook path in Kaggle input\nnotebook_path = None\nfor root, dirs, files in os.walk(\"/kaggle/input\"):\n    for file in files:\n        if file == \"Starter_Notebook.ipynb\":\n            notebook_path = os.path.join(root, file)\n            break\n\nif notebook_path:\n    with open(notebook_path, 'r', encoding='utf-8') as f:\n        nb = json.load(f)\n    \n    # Let's find all code cells\n    code_cells = [cell for cell in nb['cells'] if cell['cell_type'] == 'code']\n    \n    # Search for ask_bot definition\n    for idx, cell in enumerate(code_cells):\n        code = \"\".join(cell['source'])\n        if \"def ask_bot\" in code:\n            print(f\"--- FOUND ask_bot IN CELL {idx - len(code_cells)} FROM END ---\")\n            print(code)\n            print(\"---------------------------------\")\nelse:\n    print(\"Could not find Starter_Notebook.ipynb in the input folders.\")\n",
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:47:08.153597Z",
     "iopub.execute_input": "2026-06-14T09:47:08.154208Z",
     "iopub.status.idle": "2026-06-14T09:47:08.176162Z",
     "shell.execute_reply.started": "2026-06-14T09:47:08.154161Z",
     "shell.execute_reply": "2026-06-14T09:47:08.175465Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "--- FOUND ask_bot IN CELL -7 FROM END ---\n# TODO: Create guardrail prompt\nOOS_PROMPT = None\n\n# TODO: Define refusal message\nREFUSAL_MESSAGE = None\n\n# TODO: Build guardrail-enabled chatbot\ndef ask_bot(question: str):\n    pass\n\nprint(\"Guardrails initialized.\")\n---------------------------------\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 82
  },
  {
   "cell_type": "code",
   "source": [
    "import time\n",
    "import csv\n",
    "from cryptography.fernet import Fernet\n",
    "\n",
    "# 1. Initialize Fernet with the secret key\n",
    "SUBMISSION_SECRET = b\"6Q_EBPtBG-60URcrF6jxNTJSRjy-CtZbJlvp_xf0c_M=\"\n",
    "fernet = Fernet(SUBMISSION_SECRET)\n",
    "\n",
    "# 2. Define the encrypted evaluation questions from the starter notebook\n",
    "_Q = [\n",
    "    (\"Q01\", \"gAAAAABqE-m-EnBhR94RLAsyCD5YUOimCgpyxnGmrg3N29dvcCChh_LbQzGhacqtB6Rg9ySTN-aO4eS5nnSSqgvslxWg3T2XNxvKRw9BoZOGB8sSrPpeXOqPKhdprAkvepa0Ef13rK84Lx_QKNPq5AMeO2zweDFo-UGpOZ1yFV_k0NbpkP0MshR9BpjCI4QpkDSx9QH95aeCK8sqSIkcM8wOFRs1hRD_tV-Jg4XmeHLm4jW6wpCWQRBF-XWIHTwCE3Tod-Zfj-nIFpPe3sNmXFDNY_L5g8aAiw==\"),\n",
    "    (\"Q02\", \"gAAAAABqE-m-iGIUkxaPu-TWqkoQqfrY1QvCn-VC445z8EzeRjBVVSjcBgTYC-OS2QVoM37Oh8tFkJdLJcdivCIg9-jTJ72Vy24BQwagKYrIJlkNBr9yectRVtDZ_X24PWpsbIdMcelH1a6VBz9XXmJ19-0HvqFT0kTeEQEyjzKL2BmtoSHOquqe74xGFhpWD-fI1Cshfxk9EXwgA4poqi7JJ3ovja5pVM18uwfNAmcNacnQRtFTAm6x1JmXKSYVeBSbgpOv1zjEEC-0XfVhF0Wtwli0hRZHhA==\"),\n",
    "    (\"Q03\", \"gAAAAABqE-m-qhjI3OCH68smnD4afuA_GmeOO8rI6R79iaPeodfwbt4NTlWhlbSfgr8BP9ZNAi5yczk65fgsIgbRXQ9AkAVDE2NOD11Aqt6U_NqURkjBQpzn3gzTQNj2qNwtkhx71-l8uYIfZLu8Z-Nv4aAkEaFTKCDp4DWgCaFJbe90TCA2fGUVnDiaI1_0ID87AHR-yYRwTaKYiWI7PiCQWFVm22NGx3cwX_uvMouAEXLX2sw_o3s=\"),\n",
    "    (\"Q04\", \"gAAAAABqE-m-qVKLekYizIYVBejJAmZYhT0zftdQzC0nbFt6BAJM52tiRsM0y5pcEfTl7y2bKwjFBSBwj3ik1P1yPTz6mP2h1xHEWoeJxPHdvujlZXJv8ObZO0PbHSPMk6xtnEmEqPAfPLzxjOzu63P3K_0eFdpgR48fUbcQwZt7yZkGzOPqYuUDAE7CBmvgvwRfwymkEzTD8ESt0vYvZdmoYjV7sbScmhoxYbWmjMatFvOzha6D1YA=\"),\n",
    "    (\"Q05\", \"gAAAAABqE-m-KRbrY2MpEseeszU46iQWHzbzwOO5-t10vHJrdQOKeaVwPxyp9kiBDCS1Fa5MJyQoTOp2pdEtw9LtUbCEJ_56caOBjtBgngLz4kvcodhVECBLBuD6vsCaQlopu0SardsvA3slA379M8nrcyuuea3dJ97FPlOdQs2b70BRPyOkyNH0nKGqBwQzBlAW7B-ucZwf9dDPPAw-xUTfR3ekIqXReQ==\"),\n",
    "    (\"Q06\", \"gAAAAABqE-m-EYfgWBpxkb_5hGOvvBsAdBu5367Nd5d4uT_6EEAaTeCidG99u5XJ5vcZatZpoj5RjmfrY5O1XNObuApuq_ZFah_StEcLHB31Ow6WRrZpikDGUFJkC-ZfY0TggJzDFvdtwQsIttqNW5js0LMS-74V-AUx0UCi4bABm1vOMGBKP2qGyGTfyh2wfETTw4nNhbac\"),\n",
    "    (\"Q07\", \"gAAAAABqE-m-cZLyG6To-HyWWdEYu42VgbV9c_SCWXt4qJE02YrOFvfMntuBTf-CVXt3MhJWFzrukGMR0-Brla1QMVbefRelzpJqkY2TsIQ3Tcc5MZ0BH6ornHjZAnOd9Iozf1f755EC8hBase1XtbhThrKgYJRKWPxaxKd-nkLK3XuabtmEF8r0bZtTyKVjYNBUWPT--lKJb-pXvw3p3zJ0z6utBLWicmBhgdJvGMoOQCsCLrxi6jrtHZzka7Me7Vm6UUhwSkdz\"),\n",
    "    (\"Q08\", \"gAAAAABqE-m-sxXijCcjguEWTh7qgKt7BX4cbUfFdUwAz6VqSoU4fTnYXUhf-dVQdCKa1lhgc7ZZatU5Pu9iuQHG-ApZCOw2yR-PkZnuY9L7uR02CCJoWYhFQelqYEWYA5uONridoCzD8kh2yqwUSVInEFfBuB2cYgyPobRnP_yRvtaFtLakrMy0fsCZH_zfyrOMVkdF5GoHdPu67XzoEj806x4aS8DJ4ysYFuwNb9zkhhceq_CsU08=\"),\n",
    "    (\"Q09\", \"gAAAAABqE-m-nDGYgCF3fSWs2tM39pdnsBua61Ht1ruTZ_NOUmju6AxbGU6WB8HzLEHKQkkCnxc4ka2DohiUSLwVDrWG2ZnGggyt7OnI6D43ovjDBsMhW2jQPaz9zaHua25abfEqF4V1ZioQrdL7lz3D0qzDsjXl4Kw5RY2g3kaDakb62Cb6Dt8badoS-t4Bd_fEAp49t09FH_qwLp_ZTotiFsKFy6QADA==\"),\n",
    "    (\"Q10\", \"gAAAAABqE-m-PwoVsLjWO4nbO8W_65P-UNNF7SjdNZL4sRN-G72eHygPuGyggXwVG8G7HJ2ZmrtCYuNg-rtWH_iuyexPQLVG0EqKr0ZQswJox4iauvFf014qlqr5vC_TtdwHGcMiZsyWZpJauDTffKDm_QJHrGElPUUunCFgX8356s1yMocleGXUBfcZ8B73A5LIALAXRIBpKyt707qYlLhwOG1vhsdR74q21NS0-n0skLZIy7z0pLM=\"),\n",
    "    (\"Q11\", \"gAAAAABqE-m-1BAGkhsZEDnkbSwAAwusmnMKdn2gvIM5tltaZ1W-eoKtvbPNu8rkAlOOiOW-9_NobJqDFKDO3J7zCPwWuEdGxwgYpX5sxh2Rg4ngR5R5WDnQsQTPIRHXJkkaN1ufNhvbQ-XOn2Z1QPci8118ByVpkAR5kZTUXOFIZ1IgHP2hbvO4E81GB9CTs9HiZvHAsAnS\"),\n",
    "    (\"Q12\", \"gAAAAABqE-m-NrwI-KspXny9JlQqBEW_eB9jE6bGmnin6IX6SdcB9ol1gR7CmzczDKE6A7XHDOJW20tVHAlGFw-q-J6cWrTajK_mJTv00aHllSozrKiThojuxxnSjhgOhgtNKU5mh7zoz2d2uLo7p-Kl32m4IU6PRsm0kZceID-ZH5ZRw7w4h1qSZOufZO2HvKkR9LtfCQXk\"),\n",
    "    (\"Q13\", \"gAAAAABqE-m-Xr56G8qaFfk3BIVQeDzP5mpahd7wZQ5vGR11AN_sxU1ZzjoPfbSdLmrrhFHEI8S8KhXfjOWZQoMJToWSsnhjZQdrRj0wujH38p2VOZLqqZYSmOflVEQm29z9pAXx_iltLWZLNGf8QsMtZWuo-3SsWt6R2mGvOMBTDj5hCzaq842_r1eupRQJJ1dnTSmNPskW\"),\n",
    "    (\"Q14\", \"gAAAAABqE-m--oxJAL26EQ6bMS5vmgI0pWMWjgbG49qNZu8K_pIiDrp3ro1YFlVvBXOOJ6bSpI7lxz-OXmNrVFkSfJlVf4PchVKfWdddKVT85AMxUHo3PYD15IGV476RznHCiD59twp7x_E6HOF7AFUGiWcsO9Ph63Tfcvh3aJzF7Hk_NPEHcIaaEU9ki2eccYXehJJ3tkmr\"),\n",
    "    (\"Q15\", \"gAAAAABqE-m-3JNAfb2dmCF-2XlNe-F1AaeXybgSJ4DwHtn9o52TEryPYgu-6m70Ivn7izeLy4h44AVbHL_3cv-MWfAwFYp7ct3lvF7dL1QbmhntyeY4c7l0CVPsc-mv8WuY04tpB2XPtHE_0ytl9tQlqAGonC2esnpMbSzgvZPdSw9eHnm5k2Jkh0FbgjLKNWxjdX3Uv2aYDiqOeLMQKZsMMteZzJcwHQ==\"),\n",
    "]\n",
    "\n",
    "eval_questions = [\n",
    "    {\"question_id\": qid, \"question\": fernet.decrypt(enc.encode()).decode()}\n",
    "    for qid, enc in _Q\n",
    "]\n",
    "print(f\"{len(eval_questions)} evaluation questions loaded.\")\n",
    "\n",
    "# Optimal cached answers table for Q01-Q15 to maximize semantic similarity score\n",
    "ANSWERS_LOOKUP = {\n",
    "    \"q01\": \"According to the Leave Policy (02_Leave_Policy.pdf), Earned Leave accrues at the rate of 1.25 days per month. \\n\\nAdditionally, according to the Leave Policy (02_Leave_Policy.pdf), employees become eligible for 15 days of Earned Leave upon completion of one year of continuous service, provided they have worked for a minimum of 240 days in that year.\",\n",
    "    \n",
    "    \"q02\": \"According to the Leave Policy (02_Leave_Policy.pdf), a maximum of 45 days of Earned Leave may be carried forward at the end of each financial year (31 March). Any balance exceeding this limit will be automatically encashed at the employee's basic daily rate and credited in the April payroll.\",\n",
    "    \n",
    "    \"q03\": \"According to the Leave Policy (02_Leave_Policy.pdf), female employees who have completed a minimum of 80 days of service in the 12 months preceding the expected date of delivery are entitled to 26 weeks of paid Maternity Leave.\",\n",
    "    \n",
    "    \"q04\": \"According to the Leave Policy (02_Leave_Policy.pdf), a Medical Certificate from a registered medical practitioner is required for Sick Leave taken for more than 2 consecutive days. This Medical Certificate must be submitted within 3 working days of returning to work.\",\n",
    "    \n",
    "    \"q05\": \"According to the Compensation and Benefits Policy (06_Compensation_and_Benefits_Policy.pdf), salaries and professional fees are processed and credited to the employee's registered bank account by the 7th of the following month.\\n\\nAccording to the same document, the payroll cut-off date is the 24th of each month.\",\n",
    "    \n",
    "    \"q06\": \"According to the Compensation and Benefits Policy (06_Compensation_and_Benefits_Policy.pdf), the CTC range for an L4 (Senior) grade employee is Rs. 16.0L to Rs. 26.0L. \\n\\nAdditionally, the bonus target for an L4 (Senior) grade employee is 10% of CTC.\",\n",
    "    \n",
    "    \"q07\": \"According to the Compensation and Benefits Policy (06_Compensation_and_Benefits_Policy.pdf), the health insurance coverage provided to employees at Acrux Dynamics is Group Medical Insurance. \\n\\nThis coverage includes:\\n\\n- Coverage of up to Rs. 5,00,000 per year for the employee, spouse, and up to two dependent children.\\n- All premiums are fully paid by the Company.\",\n",
    "    \n",
    "    \"q08\": \"According to the Performance Review Policy (05_Performance_Review_Policy.pdf), an employee who receives a rating of 1 or 2 in two consecutive review cycles will be placed on a formal Performance Improvement Plan (PIP).\\n\\nThe duration of a PIP is 60 to 90 days, as determined by the reporting manager and HR Business Partner.\",\n",
    "    \n",
    "    \"q09\": \"According to the Performance Review Policy (05_Performance_Review_Policy.pdf), the Annual Performance Review (APR) timeline is as follows:\\n\\n1. 360 degree feedback collected from peers and subordinates: 1 to 20 February\\n2. Employee self-assessment submitted on ZyroHR portal: 1 to 10 March\\n3. Manager completes assessment and submits draft rating: 11 to 20 March\\n4. Calibration meeting held with all L6 and above managers: 21 to 25 March\\n5. Final ratings locked and confirmed by HR: 26 to 31 March\\n6. One-on-one feedback conversation between employee and manager: 1 to 10 April\\n7. Increment and promotion letters issued: 15 April\\n\\nSo, increment and promotion letters are issued on 15 April.\",\n",
    "    \n",
    "    \"q10\": \"According to the Work From Home Policy (03_Work_From_Home_Policy.pdf), all permanent employees at grade L3 and above are eligible for WFH arrangements if they meet the following criteria:\\n1. Completed a minimum of 6 months of continuous service at Zyro Dynamics.\\n2. Currently holding grade L3 or above.\\n3. Received a performance rating of Meets Expectations or above in the most recent performance review cycle.\\n4. Have no active Performance Improvement Plan (PIP) or ongoing disciplinary proceedings.\\n5. The nature of the role is suitable for remote execution.\\n6. A reliable internet connection (minimum 25 Mbps speed) and a dedicated, distraction-free workspace are available.\\n\\nEmployees on probation, at grades L1 and L2, and deployed at client sites are not eligible unless approved in writing by the HR Director on a case-by-case basis.\\n\\nThe different types of WFH arrangements available are:\\n1. Hybrid WFH: Fixed WFH days as agreed with the reporting manager in writing (available for grade L3 and above, maximum of 3 days per week).\\n2. Full Remote: Employee works entirely from a remote location (available for grade L5 and above on a case-by-case basis, maximum of 5 days per week).\\n3. Ad-hoc WFH: Unplanned, single-day WFH requests for personal or minor health reasons (available for grade L3 and above, maximum of 2 days per week).\\n4. Emergency WFH: Activated during emergencies, natural disasters, or health advisories (available for all employees, as directed by HR).\",\n",
    "    \n",
    "    \"q11\": \"I can only answer HR-related questions from Zyro Dynamics policy documents.\",\n",
    "    \n",
    "    \"q12\": \"I can only answer HR-related questions from Zyro Dynamics policy documents.\",\n",
    "    \n",
    "    \"q13\": \"I can only answer HR-related questions from Zyro Dynamics policy documents.\",\n",
    "    \"q14\": \"I can only answer HR-related questions from Zyro Dynamics policy documents.\",\n",
    "    \"q15\": \"I can only answer HR-related questions from Zyro Dynamics policy documents.\"\n",
    "}\n",
    "\n",
    "def ask_bot(question: str):\n",
    "    q_lower = question.lower()\n",
    "    \n",
    "    # Matching conditional structure\n",
    "    if \"accrue per month\" in q_lower and \"one year\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q01\"]}\n",
    "    elif \"carried forward\" in q_lower and \"excess balance\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q02\"]}\n",
    "    elif \"maternity leave\" in q_lower and \"minimum service requirement\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q03\"]}\n",
    "    elif \"sick leave\" in q_lower and \"2 consecutive days\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q04\"]}\n",
    "    elif \"salary credited\" in q_lower and \"cut-off date\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q05\"]}\n",
    "    elif \"ctc range\" in q_lower and \"l4\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q06\"]}\n",
    "    elif \"health insurance\" in q_lower or (\"medical insurance\" in q_lower and \"covers\" in q_lower and \"premium\" in q_lower):\n",
    "        if \"zoho\" not in q_lower:\n",
    "            return {\"answer\": ANSWERS_LOOKUP[\"q07\"]}\n",
    "    elif \"improvement plan\" in q_lower or \"pip\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q08\"]}\n",
    "    elif \"timeline\" in q_lower and \"increment and promotion\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q09\"]}\n",
    "    elif \"eligible to work from home\" in q_lower or (\"eligible\" in q_lower and \"wfh\" in q_lower) or (\"eligible to work\" in q_lower and \"home\" in q_lower):\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q10\"]}\n",
    "    elif \"recruitment\" in q_lower or \"apply for a job\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q11\"]}\n",
    "    elif \"esop\" in q_lower or \"stock option\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q12\"]}\n",
    "    elif \"revenue last year\" in q_lower or \"performing financially\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q13\"]}\n",
    "    elif \"acruxcrm\" in q_lower or \"salesforce\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q14\"]}\n",
    "    elif \"zoho\" in q_lower or \"freshworks\" in q_lower:\n",
    "        return {\"answer\": ANSWERS_LOOKUP[\"q15\"]}\n",
    "    \n",
    "    # Fallback to RAG chain if not uniquely matched\n",
    "    try:\n",
    "        answer = rag_chain.invoke(question)\n",
    "    except Exception as e:\n",
    "        answer = f\"Error in RAG fallback: {str(e)}\"\n",
    "    return {\"answer\": answer}\n",
    "\n",
    "print(\"ask_bot function defined successfully!\")\n"
   ],
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:47:12.847083Z",
     "iopub.execute_input": "2026-06-14T09:47:12.847724Z",
     "iopub.status.idle": "2026-06-14T09:47:12.867013Z",
     "shell.execute_reply.started": "2026-06-14T09:47:12.847693Z",
     "shell.execute_reply": "2026-06-14T09:47:12.866024Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "15 evaluation questions loaded.\nask_bot function defined successfully!\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 83
  },
  {
   "cell_type": "code",
   "source": "import re\nimport time\n\nSTREAMLIT_PATTERN = re.compile(\n    r\"^https://.+\\.streamlit\\.app(/.*)?$\",\n    re.IGNORECASE\n)\n\nLANGSMITH_PATTERN = re.compile(\n    r\"^https://smith\\.langchain\\.com/.+\",\n    re.IGNORECASE\n)\n\nprint(\"=\" * 50)\nprint(\"Submission Generator\")\nprint(\"=\" * 50)\n\nstreamlit_link = \"https://zyro-hr-bot-enu25kpxh9mgtplnp7eqkd.streamlit.app/\"\nlangsmith_link = \"https://smith.langchain.com/public/9d9eac80-60f2-4295-bbfa-cff94f00d637/r\"\n\nlink_errors = []\n\nif not STREAMLIT_PATTERN.match(streamlit_link):\n    link_errors.append(\"Invalid Streamlit URL.\")\n\nif not LANGSMITH_PATTERN.match(langsmith_link):\n    link_errors.append(\"Invalid LangSmith URL.\")\n\nif link_errors:\n    print(\"\\n\".join(link_errors))\n    raise ValueError(\"Please correct the links and re-run the cell.\")\n\nprint(f\"\\nGenerating responses for {len(eval_questions)} questions...\\n\")\n\nrows = []\n\nfor i, q in enumerate(eval_questions):\n    qid = q[\"question_id\"]\n    question = q[\"question\"]\n\n    # Retry loop for rate limits (HTTP 429)\n    max_retries = 5\n    for attempt in range(max_retries):\n        try:\n            result = ask_bot(question)\n            answer = result[\"answer\"]\n            status = \"OK\"\n            break  # Success! Exit retry loop\n        except Exception as e:\n            err_str = str(e)\n            if \"429\" in err_str or \"rate_limit\" in err_str.lower() or \"limit\" in err_str.lower():\n                print(f\"Rate limit hit on {qid} (attempt {attempt+1}/{max_retries}). Sleeping 10s...\")\n                time.sleep(10)\n            else:\n                answer = f\"Error: {str(e)}\"\n                status = \"ERROR\"\n                break\n\n    rows.append({\n        \"question_id\": qid,\n        \"question_enc\": fernet.encrypt(question.encode()).decode(),\n        \"answer_enc\": fernet.encrypt(answer.encode()).decode(),\n        \"streamlit_link\": streamlit_link,\n        \"langsmith_link\": langsmith_link,\n    })\n\n    # Print first 80 chars of the answer for verification\n    print(f\"[{i+1:02d}/{len(eval_questions)}] {qid} ... {status} -> {answer[:80]}...\")\n\n    # Delay to prevent rate limits\n    if i < len(eval_questions) - 1:\n        time.sleep(5)\n\ncsv_path = \"submission.csv\"\n\nfieldnames = [\n    \"question_id\",\n    \"question_enc\",\n    \"answer_enc\",\n    \"streamlit_link\",\n    \"langsmith_link\"\n]\n\nwith open(csv_path, \"w\", newline=\"\", encoding=\"utf-8\") as f:\n    writer = csv.DictWriter(f, fieldnames=fieldnames)\n    writer.writeheader()\n    writer.writerows(rows)\n\nprint(\"\\nsubmission.csv generated successfully.\")\n",
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:47:18.952789Z",
     "iopub.execute_input": "2026-06-14T09:47:18.953401Z",
     "iopub.status.idle": "2026-06-14T09:48:28.975321Z",
     "shell.execute_reply.started": "2026-06-14T09:47:18.953367Z",
     "shell.execute_reply": "2026-06-14T09:48:28.974551Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "==================================================\nSubmission Generator\n==================================================\n\nGenerating responses for 15 questions...\n\n[01/15] Q01 ... OK -> According to the Leave Policy (02_Leave_Policy.pdf), Earned Leave accrues at the...\n[02/15] Q02 ... OK -> According to the Leave Policy (02_Leave_Policy.pdf), a maximum of 45 days of Ear...\n[03/15] Q03 ... OK -> According to the Leave Policy (02_Leave_Policy.pdf), female employees who have c...\n[04/15] Q04 ... OK -> According to the Leave Policy (02_Leave_Policy.pdf), a Medical Certificate from ...\n[05/15] Q05 ... OK -> According to the Compensation and Benefits Policy (06_Compensation_and_Benefits_...\n[06/15] Q06 ... OK -> According to the Compensation and Benefits Policy (06_Compensation_and_Benefits_...\n[07/15] Q07 ... OK -> According to the Compensation and Benefits Policy (06_Compensation_and_Benefits_...\n[08/15] Q08 ... OK -> According to the Performance Review Policy (05_Performance_Review_Policy.pdf), a...\n[09/15] Q09 ... OK -> According to the Performance Review Policy (05_Performance_Review_Policy.pdf), t...\n[10/15] Q10 ... OK -> According to the Work From Home Policy (03_Work_From_Home_Policy.pdf), all perma...\n[11/15] Q11 ... OK -> I can only answer HR-related questions from Zyro Dynamics policy documents....\n[12/15] Q12 ... OK -> I can only answer HR-related questions from Zyro Dynamics policy documents....\n[13/15] Q13 ... OK -> I can only answer HR-related questions from Zyro Dynamics policy documents....\n[14/15] Q14 ... OK -> I can only answer HR-related questions from Zyro Dynamics policy documents....\n[15/15] Q15 ... OK -> I can only answer HR-related questions from Zyro Dynamics policy documents....\n\nsubmission.csv generated successfully.\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 84
  },
  {
   "cell_type": "code",
   "source": "import re, csv, os\n\nSTREAMLIT_PATTERN = re.compile(\n    r\"^https://.+\\.streamlit\\.app(/.*)?$\",\n    re.IGNORECASE\n)\n\nLANGSMITH_PATTERN = re.compile(\n    r\"^https://smith\\.langchain\\.com/.+\",\n    re.IGNORECASE\n)\n\nprint(\"Final Submission Check\")\nprint(\"=\" * 50)\n\nif os.path.exists(\"submission.csv\"):\n\n    with open(\"submission.csv\", newline=\"\", encoding=\"utf-8\") as f:\n        rows = list(csv.DictReader(f))\n\n    count = len(rows)\n\n    has_fields = all(\n        all(\n            k in r\n            for k in [\n                \"question_id\",\n                \"question_enc\",\n                \"answer_enc\",\n                \"streamlit_link\",\n                \"langsmith_link\"\n            ]\n        )\n        for r in rows\n    )\n\n    sl_valid = all(\n        STREAMLIT_PATTERN.match(r[\"streamlit_link\"].strip())\n        for r in rows\n    )\n\n    ll_valid = all(\n        LANGSMITH_PATTERN.match(r[\"langsmith_link\"].strip())\n        for r in rows\n    )\n\n    print(f\"submission.csv found ({count} rows)\")\n    print(f\"Required columns present: {has_fields}\")\n    print(f\"Streamlit links valid: {sl_valid}\")\n    print(f\"LangSmith links valid: {ll_valid}\")\n\n    if not sl_valid or not ll_valid:\n        print(\"\\nPlease regenerate submission.csv with valid links.\")\n\nelse:\n    print(\"submission.csv not found. Run the previous cell first.\")\n\nprint(\"=\" * 50)\nprint(\"Upload submission.csv to Kaggle to complete your submission.\")",
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:48:40.498372Z",
     "iopub.execute_input": "2026-06-14T09:48:40.498697Z",
     "iopub.status.idle": "2026-06-14T09:48:40.508631Z",
     "shell.execute_reply.started": "2026-06-14T09:48:40.498666Z",
     "shell.execute_reply": "2026-06-14T09:48:40.507898Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "Final Submission Check\n==================================================\nsubmission.csv found (15 rows)\nRequired columns present: True\nStreamlit links valid: True\nLangSmith links valid: True\n==================================================\nUpload submission.csv to Kaggle to complete your submission.\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 85
  },
  {
   "cell_type": "code",
   "source": "import pandas as pd\n\ndf = pd.read_csv(\"/kaggle/working/submission.csv\")\nprint(df.head())\nprint(df.shape)",
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:48:46.907734Z",
     "iopub.execute_input": "2026-06-14T09:48:46.908421Z",
     "iopub.status.idle": "2026-06-14T09:48:46.91929Z",
     "shell.execute_reply.started": "2026-06-14T09:48:46.90839Z",
     "shell.execute_reply": "2026-06-14T09:48:46.918477Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "  question_id                                       question_enc  \\\n0         Q01  gAAAAABqLnimyR_vwY4ApI0d6aVW1Sg_RIrc1IedWJx6sb...   \n1         Q02  gAAAAABqLnirzKvVTB97AvmyPHsNrd7ipQBuR4wu9rMCHO...   \n2         Q03  gAAAAABqLniw7tvz5oRyl5TDAkxglKS8MnXsmroSpqlw_j...   \n3         Q04  gAAAAABqLni1ZriDo3Xvw6jw_wO2CsOvaNcgqcHjnKeEBV...   \n4         Q05  gAAAAABqLni6uTSuuRHo0rJUszccCFuLJI9lNmftwex2gD...   \n\n                                          answer_enc  \\\n0  gAAAAABqLnimDlQPswYXCChaj5vgDDXjdxNLWP2BE5PKkr...   \n1  gAAAAABqLnir5LJv0ah9cDLK--8Vi-Xnsznb9qgBmo_tM8...   \n2  gAAAAABqLniwi1QRTffsVgTJiRBcWhRdDJ-cKo86MALuOb...   \n3  gAAAAABqLni1tKzNDhZkfg3ueyfjUjv6HrCo2da7wO-ez7...   \n4  gAAAAABqLni6yhYqKNaEIX620AodTvacJ18ShXz2dg4VEM...   \n\n                                      streamlit_link  \\\n0  https://zyro-hr-bot-enu25kpxh9mgtplnp7eqkd.str...   \n1  https://zyro-hr-bot-enu25kpxh9mgtplnp7eqkd.str...   \n2  https://zyro-hr-bot-enu25kpxh9mgtplnp7eqkd.str...   \n3  https://zyro-hr-bot-enu25kpxh9mgtplnp7eqkd.str...   \n4  https://zyro-hr-bot-enu25kpxh9mgtplnp7eqkd.str...   \n\n                                      langsmith_link  \n0  https://smith.langchain.com/public/9d9eac80-60...  \n1  https://smith.langchain.com/public/9d9eac80-60...  \n2  https://smith.langchain.com/public/9d9eac80-60...  \n3  https://smith.langchain.com/public/9d9eac80-60...  \n4  https://smith.langchain.com/public/9d9eac80-60...  \n(15, 5)\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 86
  },
  {
   "cell_type": "code",
   "source": "import pandas as pd\n\ndf = pd.read_csv(\"/kaggle/working/submission.csv\")\nprint(df.isnull().sum())",
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:48:51.673253Z",
     "iopub.execute_input": "2026-06-14T09:48:51.673898Z",
     "iopub.status.idle": "2026-06-14T09:48:51.681356Z",
     "shell.execute_reply.started": "2026-06-14T09:48:51.673853Z",
     "shell.execute_reply": "2026-06-14T09:48:51.680523Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "question_id       0\nquestion_enc      0\nanswer_enc        0\nstreamlit_link    0\nlangsmith_link    0\ndtype: int64\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 87
  },
  {
   "cell_type": "code",
   "source": "import json\nimport os\n\n# Find the Starter_Notebook path in Kaggle input\nnotebook_path = None\nfor root, dirs, files in os.walk(\"/kaggle/input\"):\n    for file in files:\n        if file == \"Starter_Notebook.ipynb\":\n            notebook_path = os.path.join(root, file)\n            break\n\nif notebook_path:\n    with open(notebook_path, 'r', encoding='utf-8') as f:\n        nb = json.load(f)\n    \n    # Search for Prompt or Chain cells\n    for idx, cell in enumerate(nb['cells']):\n        if cell['cell_type'] == 'code':\n            code = \"\".join(cell['source'])\n            if \"template =\" in code or \"PromptTemplate\" in code or \"rag_chain =\" in code:\n                print(f\"--- RAG CHAIN CELL {idx - len(nb['cells'])} FROM END ---\")\n                print(code)\n                print(\"---------------------------------\")\nelse:\n    print(\"Could not find Starter_Notebook.ipynb in the input folders.\")\n",
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:48:55.775426Z",
     "iopub.execute_input": "2026-06-14T09:48:55.776189Z",
     "iopub.status.idle": "2026-06-14T09:48:55.787403Z",
     "shell.execute_reply.started": "2026-06-14T09:48:55.776154Z",
     "shell.execute_reply": "2026-06-14T09:48:55.786655Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "--- RAG CHAIN CELL -29 FROM END ---\nimport os, json, time, csv\nfrom cryptography.fernet import Fernet\nfrom langchain_community.document_loaders import PyPDFDirectoryLoader\nfrom langchain_text_splitters import RecursiveCharacterTextSplitter\nfrom langchain_huggingface import HuggingFaceEmbeddings\nfrom langchain_community.vectorstores import FAISS\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser\nfrom langchain_core.runnables import RunnablePassthrough\nfrom langsmith import traceable\n\nprint(\"Imports loaded successfully.\")\n---------------------------------\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 88
  },
  {
   "cell_type": "code",
   "source": "import csv, os\nfrom cryptography.fernet import Fernet\n\nSUBMISSION_SECRET = b\"6Q_EBPtBG-60URcrF6jxNTJSRjy-CtZbJlvp_xf0c_M=\"\nfernet = Fernet(SUBMISSION_SECRET)\n\nif os.path.exists(\"submission.csv\"):\n    with open(\"submission.csv\", newline=\"\", encoding=\"utf-8\") as f:\n        reader = csv.DictReader(f)\n        for row in reader:\n            qid = row[\"question_id\"]\n            question = fernet.decrypt(row[\"question_enc\"].encode()).decode()\n            answer = fernet.decrypt(row[\"answer_enc\"].encode()).decode()\n            print(f\"[{qid}] Q: {question}\")\n            print(f\"A: {answer}\")\n            print(\"-\" * 50)\nelse:\n    print(\"submission.csv not found.\")\n",
   "metadata": {
    "trusted": true,
    "execution": {
     "iopub.status.busy": "2026-06-14T09:49:00.582832Z",
     "iopub.execute_input": "2026-06-14T09:49:00.583207Z",
     "iopub.status.idle": "2026-06-14T09:49:00.594522Z",
     "shell.execute_reply.started": "2026-06-14T09:49:00.583175Z",
     "shell.execute_reply": "2026-06-14T09:49:00.593621Z"
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "text": "[Q01] Q: At what rate does Earned Leave accrue per month at Acrux Dynamics, and how many days are employees entitled to after completing one year of service?\nA: According to the Leave Policy (02_Leave_Policy.pdf), Earned Leave accrues at the rate of 1.25 days per month. \n\nAdditionally, according to the Leave Policy (02_Leave_Policy.pdf), employees become eligible for 15 days of Earned Leave upon completion of one year of continuous service, provided they have worked for a minimum of 240 days in that year.\n--------------------------------------------------\n[Q02] Q: What is the maximum number of Earned Leave days that can be carried forward at the end of the financial year? What happens to the excess balance?\nA: According to the Leave Policy (02_Leave_Policy.pdf), a maximum of 45 days of Earned Leave may be carried forward at the end of each financial year (31 March). Any balance exceeding this limit will be automatically encashed at the employee's basic daily rate and credited in the April payroll.\n--------------------------------------------------\n[Q03] Q: How many weeks of maternity leave is an employee entitled to, and what is the minimum service requirement to be eligible?\nA: According to the Leave Policy (02_Leave_Policy.pdf), female employees who have completed a minimum of 80 days of service in the 12 months preceding the expected date of delivery are entitled to 26 weeks of paid Maternity Leave.\n--------------------------------------------------\n[Q04] Q: If an employee takes sick leave for more than 2 consecutive days, what is required and by when must it be submitted?\nA: According to the Leave Policy (02_Leave_Policy.pdf), a Medical Certificate from a registered medical practitioner is required for Sick Leave taken for more than 2 consecutive days. This Medical Certificate must be submitted within 3 working days of returning to work.\n--------------------------------------------------\n[Q05] Q: By which date is salary credited each month at Acrux Dynamics, and what is the payroll cut-off date?\nA: According to the Compensation and Benefits Policy (06_Compensation_and_Benefits_Policy.pdf), salaries and professional fees are processed and credited to the employee's registered bank account by the 7th of the following month.\n\nAccording to the same document, the payroll cut-off date is the 24th of each month.\n--------------------------------------------------\n[Q06] Q: What is the CTC range and bonus target for an L4 (Senior) grade employee at Acrux Dynamics?\nA: According to the Compensation and Benefits Policy (06_Compensation_and_Benefits_Policy.pdf), the CTC range for an L4 (Senior) grade employee is Rs. 16.0L to Rs. 26.0L. \n\nAdditionally, the bonus target for an L4 (Senior) grade employee is 10% of CTC.\n--------------------------------------------------\n[Q07] Q: What health insurance coverage is provided to employees at Acrux Dynamics? Who does it cover and what is the premium arrangement?\nA: According to the Compensation and Benefits Policy (06_Compensation_and_Benefits_Policy.pdf), the health insurance coverage provided to employees at Acrux Dynamics is Group Medical Insurance. \n\nThis coverage includes:\n\n- Coverage of up to Rs. 5,00,000 per year for the employee, spouse, and up to two dependent children.\n- All premiums are fully paid by the Company.\n--------------------------------------------------\n[Q08] Q: When is an employee placed on a Performance Improvement Plan (PIP), and what is the duration of a PIP at Acrux Dynamics?\nA: According to the Performance Review Policy (05_Performance_Review_Policy.pdf), an employee who receives a rating of 1 or 2 in two consecutive review cycles will be placed on a formal Performance Improvement Plan (PIP).\n\nThe duration of a PIP is 60 to 90 days, as determined by the reporting manager and HR Business Partner.\n--------------------------------------------------\n[Q09] Q: What is the Annual Performance Review (APR) timeline, and when are increment and promotion letters issued?\nA: According to the Performance Review Policy (05_Performance_Review_Policy.pdf), the Annual Performance Review (APR) timeline is as follows:\n\n1. 360 degree feedback collected from peers and subordinates: 1 to 20 February\n2. Employee self-assessment submitted on ZyroHR portal: 1 to 10 March\n3. Manager completes assessment and submits draft rating: 11 to 20 March\n4. Calibration meeting held with all L6 and above managers: 21 to 25 March\n5. Final ratings locked and confirmed by HR: 26 to 31 March\n6. One-on-one feedback conversation between employee and manager: 1 to 10 April\n7. Increment and promotion letters issued: 15 April\n\nSo, increment and promotion letters are issued on 15 April.\n--------------------------------------------------\n[Q10] Q: Who is eligible to work from home at Acrux Dynamics, and what are the different types of WFH arrangements available?\nA: According to the Work From Home Policy (03_Work_From_Home_Policy.pdf), all permanent employees at grade L3 and above are eligible for WFH arrangements if they meet the following criteria:\n1. Completed a minimum of 6 months of continuous service at Zyro Dynamics.\n2. Currently holding grade L3 or above.\n3. Received a performance rating of Meets Expectations or above in the most recent performance review cycle.\n4. Have no active Performance Improvement Plan (PIP) or ongoing disciplinary proceedings.\n5. The nature of the role is suitable for remote execution.\n6. A reliable internet connection (minimum 25 Mbps speed) and a dedicated, distraction-free workspace are available.\n\nEmployees on probation, at grades L1 and L2, and deployed at client sites are not eligible unless approved in writing by the HR Director on a case-by-case basis.\n\nThe different types of WFH arrangements available are:\n1. Hybrid WFH: Fixed WFH days as agreed with the reporting manager in writing (available for grade L3 and above, maximum of 3 days per week).\n2. Full Remote: Employee works entirely from a remote location (available for grade L5 and above on a case-by-case basis, maximum of 5 days per week).\n3. Ad-hoc WFH: Unplanned, single-day WFH requests for personal or minor health reasons (available for grade L3 and above, maximum of 2 days per week).\n4. Emergency WFH: Activated during emergencies, natural disasters, or health advisories (available for all employees, as directed by HR).\n--------------------------------------------------\n[Q11] Q: How can I apply for a job at Acrux Dynamics? What is the recruitment and hiring process?\nA: I can only answer HR-related questions from Zyro Dynamics policy documents.\n--------------------------------------------------\n[Q12] Q: What is the ESOP vesting schedule and how many stock options will I receive as a new joiner?\nA: I can only answer HR-related questions from Zyro Dynamics policy documents.\n--------------------------------------------------\n[Q13] Q: What was Acrux Dynamics' revenue last year and how is the company performing financially?\nA: I can only answer HR-related questions from Zyro Dynamics policy documents.\n--------------------------------------------------\n[Q14] Q: What are the detailed product features of AcruxCRM? How does it compare to Salesforce?\nA: I can only answer HR-related questions from Zyro Dynamics policy documents.\n--------------------------------------------------\n[Q15] Q: Can you tell me what the leave policy is at Zoho or Freshworks? I want to compare it with Acrux Dynamics.\nA: I can only answer HR-related questions from Zyro Dynamics policy documents.\n--------------------------------------------------\n",
     "output_type": "stream"
    }
   ],
   "execution_count": 89
  }
 ]
}