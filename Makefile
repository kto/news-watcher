
init:
	pip install -r requirements.txt --use-mirrors

test:
	nosetests

check:
	find . -name \*.py | xargs pylint --errors-only --reports=n
	find . -name \*.py | xargs flake8

clean:
	find . -name '*.pyc' -delete

