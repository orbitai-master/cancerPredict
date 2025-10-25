
# Contributing to the Breast Cancer Predictor App

Thank you for your interest in contributing to this Streamlit-based Breast Cancer Diagnosis tool\! We rely on community contributions to improve accuracy, user experience, and educational resources.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct. Please be respectful and welcoming in all interactions.

## How to Contribute

We primarily accept contributions through **Pull Requests (PRs)** following the **Fork and Branch** model.

### 1\. Set Up Your Environment

1.  **Fork the Repository:** Click the **Fork** button at the top right of the original repository page (`https://github.com/orbitai-master/cancerPredict`). This creates a copy under your own GitHub account.
2.  **Clone Your Fork:** Clone your personal copy to your local machine:
    ```bash
    git clone https://github.com/YOUR-USERNAME/cancerPredict.git
    cd cancerPredict
    ```
3.  **Install Dependencies:** This project uses Streamlit, Pandas, and Plotly.
    ```bash
    pip install -r requirements.txt
    # (Assuming you have a requirements.txt file)
    ```

### 2\. Create a Feature Branch

Always create a new branch for your specific change. **Do not commit directly to `main` or `master`.**

```bash
# Update your local main branch before starting
git checkout main
git pull origin main

# Create and switch to a new branch (use a descriptive name)
git checkout -b feature/your-awesome-feature
# Example: git checkout -b fix/sidebar-bug
```

### 3\. Implement Your Changes

1.  **Write Code:** Implement your feature or fix.

2.  **Test Locally:** Run the application locally to ensure your changes work and haven't introduced bugs:

    ```bash
    streamlit run main.py
    ```

3.  **Commit Changes:** Stage only the files you modified and write a clear commit message. We follow **Conventional Commits**:

      * `feat:` for a new feature (e.g., `feat: Add user login functionality`)
      * `fix:` for a bug fix (e.g., `fix: Correct minor spacing issue in sidebar`)
      * `docs:` for documentation changes (e.g., `docs: Update README with deployment guide`)

    <!-- end list -->

    ```bash
    git add <file-name>
    git commit -m "feat: Your descriptive commit message here"
    ```

### 4\. Create a Pull Request (PR)

1.  **Push to Your Fork:** Push your local feature branch to your personal GitHub fork:
    ```bash
    git push origin feature/your-awesome-feature
    ```
2.  **Open the PR:** Go to your **Fork** on GitHub. A prompt will usually appear to open a Pull Request.
      * The PR should go from: **`YOUR-USERNAME/cancerPredict` (your feature branch)** $\rightarrow$ **`orbitai-master/cancerPredict` (main branch)**.
3.  **Fill Out the PR Template:** Provide a detailed description explaining:
      * The goal of your contribution.
      * The specific changes made.
      * If applicable, which issue number it **closes** (e.g., `Closes #15`).

## Code Standards

  * **Python Style:** Follow **PEP 8** standards (variable naming, line length).
  * **Comments:** Use comments sparingly to explain *why* code is doing something, not *what* it is doing.
  * **Streamlit Code:** Ensure all Streamlit components are clearly labeled and do not disrupt the overall app layout.
  * **Keep Changes Focused:** A PR should ideally contain one feature or one fix. If you have multiple unrelated changes, submit them as separate PRs.

