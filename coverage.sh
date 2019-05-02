rm -rf htmlcov
pytest $1 --cov-report html --cov
open htmlcov/index.html