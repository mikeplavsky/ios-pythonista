rm -rf htmlcov
pytest --cov-report html --cov
open htmlcov/index.html