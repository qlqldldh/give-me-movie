# Give Me Movie

> 매주 영화 한 편씩.

## Requirements
- Poetry
- Python 3.9
> you also need client id and secret key from Naver Development Center

## Installation
- __Poetry__<br>
`https://python-poetry.org/docs/#installation`

- Dependencies<br>
```
poetry install
```

## Run in local environment
```
poetry run python main.py
```

## Test
```
poetry run pytest
```

## Deployment
```
poetry run zappa deploy {stage_name}
```
