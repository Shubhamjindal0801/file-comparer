# 📄 Enhanced Document Comparison Tool

A powerful web-based tool to compare Word documents, PDFs, and text files with multiple algorithms and interactive visualizations.

## 🚀 One-Click Setup & Launch

Simply run the setup script to automatically install everything and start the web interface:

```bash
cd document-comparision-script
./setup.sh
```

That's it! The web interface will automatically open at `http://localhost:8501`

## ✨ Features

- **🔍 Multiple Comparison Algorithms**: 
  - Unified diff (line-by-line)
  - Context diff (with surrounding lines)
  - Levenshtein distance (character-level)
  - Jaro-Winkler similarity
  - Semantic similarity

- **📊 Interactive Visualizations**: 
  - Real-time similarity gauges
  - Statistical charts and graphs
  - Visual difference highlighting

- **📁 File Format Support**:
  - ✅ Word Documents (.docx)
  - ✅ PDF Files (.pdf) 
  - ✅ Text Files (.txt)

- **📤 Export Options**:
  - Word documents (.docx)
  - HTML reports (.html)
  - JSON data (.json)
  - Markdown (.md)

## 🎯 How to Use

1. **Start the tool**: Run `./setup.sh`
2. **Upload files**: Drag & drop or browse for two documents
3. **Choose settings**: Select comparison algorithm and options
4. **Compare**: Click "Compare Documents" 
5. **Review results**: View statistics, charts, and detailed differences
6. **Export**: Download results in your preferred format

## 🛠️ Manual Setup (if needed)

If you need to set up manually:

```bash
# Create virtual environment
python3 -m venv doc-env

# Activate environment
source doc-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start web interface
streamlit run streamlit_app.py
```

## 📋 Requirements

- Python 3.8 or higher
- Web browser (Chrome, Firefox, Safari, etc.)

## 🚀 Get Started

```bash
git clone <repository-url>
cd document-comparision-script
./setup.sh
```

The web interface will automatically launch at `http://localhost:8501`

## 🔄 Starting After Initial Setup

After the first setup, you can quickly start the tool anytime with:

```bash
./start.sh
```

Happy comparing! 🎉

## 🌐 Live Demo

Try the live version: [Document Comparison Tool](https://your-app-name.streamlit.app)

## 🚀 Deploy Your Own

### Option 1: Streamlit Community Cloud (Recommended - Free)

1. **Fork this repository** on GitHub
2. **Visit [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your GitHub account**
4. **Deploy** by selecting your repository
5. **Set main file**: `streamlit_app.py`
6. **Deploy!** Your app will be live at `https://your-app-name.streamlit.app`

### Option 2: Heroku

1. **Install Heroku CLI**
2. **Create Heroku app**: `heroku create your-app-name`
3. **Deploy**: `git push heroku main`

### Option 3: Railway

1. **Visit [railway.app](https://railway.app)**
2. **Connect GitHub repository**
3. **Deploy automatically** 