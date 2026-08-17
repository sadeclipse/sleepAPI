# sleepAPI 

This project takes your health metrics and predicts your sleep quality score (0 - 10) as well as daily stress level (low, medium, high).

This project is my first experience building an ML/AI application outside of a local Jupyter Notebook (`.ipynb`). It is built using **FastAPI** and **Uvicorn** to serve the models.

## Requirements
* Python 3.12+
* Windows PowerShell (to run the setup script)

The project requires libraries like `fastapi`, `tensorflow`, `pandas`, `scikit-learn`, etc. However, you do not need to install them manually, i gotchu. I got a setup script for you to run and chill.

## Installation & Setup

1. **Clone this repository** to your local machine:
   ```bash
   git clone <repository-url>
   cd sleepapi
   ```

2. **Run the setup script** to install dependencies and prepare the data and models:
   ```powershell
   ./setup.ps1
   ```

3. **Start the FastAPI server**:
   ```powershell
   python run.py
   ```

Once the server is running, you can access the interactive API documentation (Swagger UI) at:
**http://127.0.0**

## Environment Variables

Create a `.env` file in the root directory. Currently, there is only one required variable for the database connection (SQLite is used as the default since the project does not require scaling):

```text
DATABASE_URL=sqlite:///./sleep.db
```
