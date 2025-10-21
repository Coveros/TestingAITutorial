# 🔧 Repository Setup Instructions

## 📁 Files That Should NOT Be Committed to GitHub

### 🔐 **CRITICAL - Security Files (Never commit these!)**
```
.env                    # Contains your actual API keys
config/secrets.json     # Any secret configuration
*.key, *.pem           # Certificate and key files
```

### 💾 **Database Files (Large and regeneratable)**
```
*.sqlite3              # ChromaDB database files
embedding_experiment_db/ # Vector database experiments  
generation_experiment_db/
retrieval_experiment_db/
test_chroma_db_*/      # Test database directories
```

### 📊 **Results and Logs (Generated outputs)**
```
regression_test_results/  # Test result JSON files
evaluation_results.json   # Evaluation outputs
*.log                    # Log files
experiment_logs/         # Experiment output logs
```

### 🐍 **Python Generated Files**
```
__pycache__/            # Python cache directories
*.pyc                   # Compiled Python files
.pytest_cache/          # Test cache
.coverage               # Coverage reports
```

### 📓 **Jupyter Notebook Outputs**
```
.ipynb_checkpoints/     # Notebook checkpoints
Untitled*.ipynb         # Temporary notebooks
```

## ✅ Files That SHOULD Be Committed

### 📝 **Source Code**
```
app/                    # Your RAG application code
experiments/            # Experiment scripts
regression_testing/     # Testing framework
tests/                  # Unit tests
requirements.txt        # Python dependencies
```

### 📋 **Documentation**
```
README.md              # Project documentation
docs/                  # Documentation files
.env.template          # Environment template (safe)
```

### ⚙️ **Configuration**
```
.gitignore             # Git ignore rules
config/                # Non-secret configuration
templates/             # HTML templates
static/                # Static web assets
```

## 🚀 Git Setup Commands

To initialize your repository and commit the right files:

```bash
# Initialize git repository
git init

# Add all appropriate files (gitignore will exclude sensitive files)
git add .

# Make initial commit
git commit -m "Initial commit: RAG system with experiments and testing framework"

# Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/yourusername/your-repo-name.git

# Push to GitHub
git push -u origin main
```

## 🔄 Before Each Commit

Always check what you're about to commit:
```bash
git status                    # See what files are staged
git diff --cached            # Review changes to be committed
```

## 🛡️ Environment Setup for New Users

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Create environment file**
   ```bash
   cp .env.template .env
   # Edit .env with your actual API keys
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the system**
   ```bash
   python run.py
   ```

## 🔍 File Size Considerations

GitHub has limits:
- **Files > 100MB**: Cannot be pushed
- **Repository > 1GB**: Performance issues
- **Files > 50MB**: Warning

Large files to exclude:
- Vector databases (can be GBs)
- Model files (*.model, *.pkl)
- Large datasets
- Experiment result archives

## 📊 What Students Will Get

When someone clones your repository, they'll get:
✅ Complete source code
✅ Experiment frameworks
✅ Testing infrastructure  
✅ Documentation
✅ Setup instructions

❌ No API keys (they provide their own)
❌ No personal results/logs
❌ No large database files
❌ No temporary/cache files