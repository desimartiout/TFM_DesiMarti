import yaml

# Cargar textos desde un archivo YAML
with open("./locale/es/text.yaml", "r", encoding="utf-8") as file:
    texts = yaml.safe_load(file)

####################################################################################################
#                                   TEXTOS
####################################################################################################
PROMPT_TEMPLATE = texts["prompt_template"]  #Template de Ollama
OPENAI_TEMPLATE = texts["openai_template"]  #Template de OPENAI

CHATBOT_CAB = texts["chatbot_cab"]
CHATBOT_TITLE = texts["chatbot_title"]
CHATBOT_WELLCOME = texts["chatbot_wellcome"]
CHATBOT_INTRO = texts["chatbot_intro"]
CAB_AVISOLEGAL = texts["cab_avisolegal"]
TEXTO_AVISOLEGAL = texts["texto_avisolegal"]

REPORT_CAB = texts["report_cab"]
REPORT_TITLE = texts["report_title"]

DATASET_CAB = texts["dataset_cab"]
DATASET_TITLE = texts["dataset_title"]

CAB_AYUDAS_ALMACENADAS = texts["cab_ayudas_almacenadas"]


####################################################################################################
#                                   ESTILOS
####################################################################################################

ESTILOS = """
    <style>
    /* Main background and text colors */
    body { background-color: #f0f8ff; color: #002B5B; }
    .sidebar .sidebar-content { background-color: #00233A; color: white; padding: 20px; border-right: 2px solid #003d5c; }
    .sidebar h2, .sidebar h4 { color: white; }
    .block-container { background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); }
    .footer-text { font-size: 1.1rem; font-weight: bold; color: black; text-align: center; margin-top: 10px; }
    .stButton button { background-color: #118ab2; color: white; border-radius: 5px; padding: 10px 20px; font-size: 16px; }
    .stButton button:hover { background-color: #07a6c2; color: white; }
    h1, h2, h3, h4 { color: #00233A; }
    .stChatMessage { background-color: #C8E1F0; color: #00233A; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .stChatMessage.user { background-color: #118ab2; color: white; }
    .st-emotion-cache-1c7y2kd {
        flex-direction: row-reverse;
        text-align: right;
        background-color: white;
    }
    .st-emotion-cache-1dj3ksd {
        background-color: #00233A;
    }
    .st-emotion-cache-1373cj4 {
        color: #00233A;
    }
    /*
    .st-cf {
        background: linear-gradient(to right, rgb(0, 36, 58) 0%, rgb(0, 36, 58) 90%, rgba(151, 166, 195, 0.25) 90%, rgba(151, 166, 195, 0.25) 100%);
    }
    */
    ::-webkit-scrollbar:active {
        background: #00233A;
    }
    </style>
    """

ESTILOS_INICIO = """
  <style>
  /* Main background and text colors */
  body {
      background-color: #f0f8ff;  /* Light cyan background */
      color: #002B5B;  /* Dark blue text for readability */
  }
  .sidebar .sidebar-content {
      background-color: #00233A;  /* Dark cyan sidebar background */
      color: white;
      padding: 20px;
      border-right: 2px solid #003d5c;  /* Darker border */
  }
  .sidebar h2, .sidebar h4 {
      color: white;  /* White text for sidebar headings */
  }
  .block-container {
      background-color: white;  /* White content background */
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);  /* Subtle shadow for modern look */
  }

  /* Center content inside columns */
  .stColumn {
      text-align: center;
  }
  /* Style for the centered and bold footer text */
  .footer-text {
      font-size: 1.1rem;
      font-weight: bold;
      color: black;
      text-align: center;
      margin-top: 10px;
  }
  /* Style buttons to look modern and attractive */
  .stButton button {
      background-color: #118ab2;
      color: white;
      border-radius: 5px;
      border: none;
      padding: 10px 20px;
      font-size: 16px;
      box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
  }
  .stButton button:hover {
      background-color: #07a6c2;
      color: white;
  }
  /* Headings inside the main page */
  h1, h2, h3, h4 {
      color: #00233A;
  }
  
    .st-emotion-cache-1dj3ksd {
        background-color: #00233A;
    }
    .st-emotion-cache-1373cj4 {
        color: #00233A;
    }
    /*
    .st-cf {
        background: linear-gradient(to right, rgb(0, 36, 58) 0%, rgb(0, 36, 58) 90%, rgba(151, 166, 195, 0.25) 90%, rgba(151, 166, 195, 0.25) 100%);
    }
    */
    ::-webkit-scrollbar:active {
        background: #00233A;
    }
  </style>
  """