black --check --diff --line-length 79 ../app/
echo "black tool done..."
isort --check -only --diff --line-length 79 --profile black ../app/
echo "isort tool done..."
flake8 ../app/
echo "flake8 tool done..."
mypy --ignore-missing-imports ../app/
echo "mypy tool done..."
