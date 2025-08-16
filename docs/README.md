# Buildathon Project Documentation

Welcome to the Buildathon project documentation! This repository contains multiple AI/ML projects with comprehensive documentation and implementation details.

## 📚 **Project Overview**

### **Project 1: Visual Memory Search** 🖼️
A sophisticated screenshot search system that combines OCR, computer vision, and AI to enable natural language queries for visual content.

**Key Features:**
- **OCR Text Extraction**: Extract text from screenshots using Tesseract
- **AI-Powered Visual Analysis**: Generate detailed descriptions using OpenAI GPT-4 Vision
- **Semantic Search**: Find images using natural language queries
- **Smart Scoring**: AI-validated confidence scores with explainable results
- **Comprehensive Testing**: 12 diverse screenshot types for thorough validation

**Documentation:**
- [📖 Project Overview](PROJECT_1_README.md) - Complete project description and setup
- [🤖 OpenAI Integration](PROJECT_1_OPENAI_README.md) - Advanced AI features and configuration
- [🏗️ Architecture Details](PROJECT_1_STRUCTURE.md) - Technical implementation and file structure
- [🧪 Test Dataset Guide](PROJECT_1_TEST_DATASET.md) - Testing procedures and dataset details

**Quick Start:**
```bash
cd p1
chmod +x quick_start.sh
./quick_start.sh
python main.py test_screenshots --query "blue button"
```

---

### **Project 2: [Coming Soon]** 🚧
*Documentation will be added as projects are developed*

---

### **Project 3: [Coming Soon]** 🚧
*Documentation will be added as projects are developed*

---

### **Project 4: [Coming Soon]** 🚧
*Documentation will be added as projects are developed*

---

### **Project 5: [Coming Soon]** 🚧
*Documentation will be added as projects are developed*

---

## 🛠️ **Repository Structure**

```
buildathon/
├── docs/                           # 📚 All project documentation
│   ├── README.md                   # This file - main documentation index
│   ├── PROJECT_1_README.md         # Project 1 overview and setup
│   ├── PROJECT_1_OPENAI_README.md  # Project 1 AI features
│   ├── PROJECT_1_STRUCTURE.md      # Project 1 architecture
│   └── PROJECT_1_TEST_DATASET.md   # Project 1 testing guide
├── p1/                             # 🖼️ Visual Memory Search implementation
│   ├── main.py                     # Core application
│   ├── requirements.txt            # Python dependencies
│   ├── quick_start.sh              # Automated setup script
│   ├── demo.py                     # Interactive demo
│   ├── test_search.py              # Automated testing
│   ├── generate_test_dataset.py    # Test data generation
│   ├── config.py                   # Configuration settings
│   └── setup_openai.py             # OpenAI setup helper
├── p2/                             # 🚧 Future project
├── p3/                             # 🚧 Future project
├── p4/                             # 🚧 Future project
├── p5/                             # 🚧 Future project
├── README.md                       # Repository overview
└── .gitignore                      # Git exclusions
```

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.8+
- Git
- Tesseract OCR (for Project 1)
- OpenAI API key (optional, for enhanced features)

### **Installation**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/sakomws/buildathon.git
   cd buildathon
   ```

2. **Choose a project:**
   - For **Project 1**: Follow the [quick start guide](PROJECT_1_README.md)
   - For other projects: Check their respective documentation

3. **Set up environment:**
   - Create virtual environment: `python -m venv venv`
   - Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
   - Install dependencies: `pip install -r p1/requirements.txt`

## 🔧 **Development**

### **Adding New Projects**
1. Create project folder: `mkdir pX`
2. Add implementation files
3. Create documentation in `docs/` folder
4. Update this main README.md
5. Update `.gitignore` if needed

### **Documentation Standards**
- Use clear, descriptive filenames
- Include setup instructions
- Provide usage examples
- Document configuration options
- Include troubleshooting guides

## 📝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Update documentation
5. Submit a pull request

## 📄 **License**

This project is open source. Please check individual project files for specific licensing information.

## 🤝 **Support**

For questions or issues:
1. Check the relevant project documentation
2. Review the troubleshooting guides
3. Open an issue on GitHub
4. Check the project-specific README files

---

**Happy Building! 🚀**

*Last updated: August 2025* 