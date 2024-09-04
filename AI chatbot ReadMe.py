Setting Up Your AI Chatbot in Visual Studio Code

 Set Up Your Project Folder
---------------------------
Create a new folder for your project, e.g., C:\Projects\AIChatbot.
Open VS Code and navigate to the project folder using File -> Open Folder or drag and drop the folder into the VS Code window.

Create a Virtual Environment
---------------------------

Open a terminal in VS Code (Terminal -> New Terminal or Ctrl + \ Ctrl + \).

Run the following commands to create and activate a virtual environment:
python -m venv my_env
.\my_env\Scripts\activate  # On Windows PowerShell

Install Required Packages
-------------------------
With the virtual environment activated, install spaCy, transformers, and pypdf:

pip install spacy transformers pypdf

Download the spaCy model:
python -m spacy download en_core_web_sm


 Create the Python Script
 ------------------------
 In VS Code, create a new file named light_chatbot.py in your project folder.
 Copy and paste the following code into light_chatbot.py:
 


Create a PDF File
-----------------

Place your PDF file in the same directory as light_chatbot.py.

Run Your Script
---------------

In the terminal, with your virtual environment activated, run the script:
python light_chatbot.py

Verify the File Location
------------------------

Ensure that light_chatbot.py is indeed in the F:\AIApp directory. You can check this by navigating to the directory and listing the files:
dir F:\AIApp

Install TensorFlow
------------------

Install TensorFlow in your virtual environment:
pip install tensorflow


Verify Installation

python -c "import tensorflow as tf; print(tf.__version__)"

 Install the Compatible tf-keras Package
 ---------------------------------------
 
 Install tf-keras: Run the following command in your environment:
 pip install tf-keras

Run the Script Again: After installing tf-keras, try running your script again:
python light_chatbot.py
