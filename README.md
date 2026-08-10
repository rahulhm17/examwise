# 📚 ExamWise – AI-Powered Question Paper Intelligence System

🚀 **ExamWise is an AI-powered question paper analysis platform that uses OCR, NLP, and semantic similarity to identify repeated questions and important examination patterns.**

## 🎯 Problem Statement

Students often spend a lot of time manually analyzing previous-year question papers to identify repeated questions, important concepts, and frequently asked topics.

This becomes even more difficult when question papers are available as scanned PDFs or images.

## 💡 Solution

ExamWise automates question paper analysis by extracting questions from PDFs and images, cleaning the extracted content, and using NLP-based semantic similarity to identify repeated or conceptually similar questions.

## 🔥 Key Features

* 📄 Upload multiple question papers
* 🖼️ Support JPG, JPEG and PNG images
* 📑 Support text-based PDF files
* 📷 OCR support for scanned PDFs
* 🔍 Automatic question extraction
* 🧹 Text preprocessing and cleaning
* 🧠 NLP-based semantic similarity
* 🔁 Repeated question detection
* 📊 Examination pattern analysis
* 🎯 Study-focused insights
* 🌐 Interactive Streamlit interface

## ⚙️ How It Works

```text
Upload Question Papers
        ↓
File Detection
        ↓
PDF Text Extraction / OCR
        ↓
Text Preprocessing
        ↓
Question Detection
        ↓
Question Cleaning
        ↓
Semantic Embeddings
        ↓
Similarity Analysis
        ↓
Repeated Question Detection
        ↓
ExamWise Insights
```

## 🛠️ Technology Stack

| Technology            | Purpose              |
| --------------------- | -------------------- |
| Python                | Core application     |
| Streamlit             | Web interface        |
| PyMuPDF               | PDF text extraction  |
| Tesseract OCR         | Scanned document OCR |
| OpenCV                | Image preprocessing  |
| Pillow                | Image processing     |
| Sentence Transformers | Semantic embeddings  |
| Scikit-learn          | Similarity analysis  |

## 📄 Supported Formats

* PDF
* Scanned PDF
* PNG
* JPG
* JPEG

## 🧠 Semantic Question Analysis

ExamWise compares questions based on their meaning rather than only matching exact words.

For example:

```text
Implement a full adder using basic gates.

Design a full adder circuit using logic gates.
```

The system can identify these as conceptually similar questions.

## 📁 Project Structure

```text
ExamWise/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── utils/
│   ├── __init__.py
│   ├── file_processor.py
│   ├── image_extractor.py
│   ├── pdf_extractor.py
│   ├── question_parser.py
│   └── similarity.py
│
└── screenshots/
```

## 💻 Installation

```bash
git clone https://github.com/rahulhm17/examwise.git
cd examwise
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 🔤 OCR Setup

ExamWise uses Tesseract OCR for scanned PDFs and images.

For Windows, install Tesseract OCR and verify the installation:

```bash
tesseract --version
```

## ▶️ Run the Application

```bash
streamlit run app.py
```

## 🎓 Use Cases

* Students preparing for examinations
* Previous-year question paper analysis
* Repeated question identification
* Concept-based revision
* Examination pattern analysis
* Smart exam preparation

## 🔮 Future Enhancements

* 📚 Automatic topic and module classification
* 📝 Automatic marks detection
* 📊 Year-wise question frequency analysis
* 🎯 AI-based study priority scoring
* 📈 Examination trend visualization
* 📄 PDF and Excel report generation
* 🤖 AI-powered ExamWise assistant
* 💬 Ask ExamWise conversational interface
* 🌐 Cloud deployment
* 👤 Personalized student dashboards

## 👨‍💻 Author

**Rahul HM**

B.E. Artificial Intelligence & Data Science
CMR Institute of Technology (CMRIT), Bengaluru

## 🔗 Project

**GitHub:** [https://github.com/rahulhm17/examwise](https://github.com/rahulhm17/examwise)

⭐ If you find ExamWise useful, consider giving the repository a star.
