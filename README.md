# AIprep ✍️📘

*A TOEFL Writing Task Assistant Powered by LLMs*

**AIprep** is a web application designed to help students **prepare for the TOEFL Writing Task** with intelligent, contextualized feedback. Unlike generic grammar checkers, AIprep evaluates writing by **considering both the student's response and the original question prompt**. It provides **automated scoring**, **personalized feedback**, and a **professional PDF report** that students can easily share with teachers.

---

## 🌟 Key Features

* 🧠 **Contextual Evaluation**: Analyzes the student's writing **in relation to the actual question**, not in isolation.
* 📝 **TOEFL-Specific Feedback**: Covers all TOEFL writing rubric aspects: **task achievement, coherence, grammar, vocabulary**, and **organization**.
* 🎯 **Score Estimation**: Automatically estimates the student's **TOEFL writing grade** based on evaluation criteria.
* 📄 **PDF Report Generation**: Generates a clean, downloadable **report** with scores, comments, and suggestions for improvement.
* ⚙️ **LLM-Powered Analysis**: Uses advanced **language models** (e.g., OpenAI GPT) to deliver high-quality, human-like feedback.
* 🌐 **User-Friendly Web App**: Simple interface to input question & response, view results, and download the report.

---

## 🏗️ Tech Stack

* **Backend**: Python, Django
* **AI/NLP**: Large Language Models (e.g., OpenAI API)
* **PDF Reports**: `reportlab` or equivalent
* **Frontend**: HTML/CSS (Django templates)
* **Database**: SQLite / MySQL
  
---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/alireza-jahandoost/AIprep.git
cd AIprep
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and define the following:

```
DEBUG=True
SECRET_KEY=your_django_secret_key
OPENAI_API_KEY=your_openai_api_key
```

*(You can add other environment variables like `ALLOWED_HOSTS`, `DATABASE_URL`, etc., as needed.)*

### 5. Apply Migrations and Create Superuser (optional)

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The web app will now be available at `http://127.0.0.1:8000/`.

---

## 💡 Example Workflow

1. Student enters their **TOEFL writing question** and **essay response**.
2. The system:

   * Analyzes the response using an **LLM**
   * Estimates the **score (0–5)**
   * Highlights strengths and areas for improvement
   * Generates a professional **PDF report**
3. Student downloads the report or sends it to their teacher.

---

## 🙋 Who Is It For?

* 🧑‍🎓 **TOEFL candidates** seeking reliable, fast feedback on their writing
* 👩‍🏫 **Teachers** who want to assist students efficiently
* 🏫 **Language institutes** aiming to offer AI-assisted training tools

---

## 📘 License

Licensed under the MIT License. See the `LICENSE` file for details.

---

## 🤝 Contributions

All contributions are welcome! Whether you're fixing bugs, improving scoring logic, or enhancing the UI, feel free to fork, commit, and open a pull request.
