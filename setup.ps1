# setup.ps1
$env:PYTHONPATH = "./app"



echo "Installing requirements..."
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

echo "Running preprocessing..."
python app\notebooks\preprocessing.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

echo "Setup completed successfully."
