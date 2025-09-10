# ✨ Multilingual Translator 💬🗣

A modern Streamlit web app for translating text between 50+ languages using Facebook's mBART-50 model from Huggingface. Powered by deep learning, it provides fast, accurate, and multilingual translation in a simple interface.

---

## Demo
![Demo GIF](demo.gif)

---

## Features
- Translate text between 50+ languages
- Powered by mBART-50 (Facebook/Huggingface)
- Simple, responsive Streamlit UI
- Docker support for easy deployment

---

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/<your-username>/Multilingual-Translator.git
   cd Multilingual-Translator
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

---

## Usage
1. Start the app:
   ```sh
   streamlit run app.py
   ```
2. Open your browser and go to [http://localhost:8501](http://localhost:8501)
3. Select source and target languages, enter text, and click "Translate"

---

## Docker Deployment
1. Make sure Docker is installed ([instructions](https://docs.docker.com/engine/install/))
2. Build the Docker image:
   ```sh
   docker build -f Dockerfile -t multilingual-translator:latest .
   ```
3. Run the container:
   ```sh
   docker run -p 8501:8501 multilingual-translator:latest
   ```
4. Visit [http://localhost:8501](http://localhost:8501) in your browser

---

## Credits
Made with ❤️ by [B Sai Teja Goud](mailto:saitej0045@gmail.com)

---

## License
This project is licensed under the MIT License.

---
