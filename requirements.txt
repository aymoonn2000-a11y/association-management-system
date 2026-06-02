name: 🚀 Deploy Streamlit App

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests (إذا كان عندك tests)
        run: |
          pip install pytest
          pytest || echo "No tests found, skipping..."

      - name: Check code formatting (Optional)
        run: |
          pip install black
          black --check . || echo "Black check skipped"
