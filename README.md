# Give Me Movie

> 매주 영화 한 편씩.

## Install
- __Poetry__<br>
`https://python-poetry.org/docs/#installation`

- Dependencies<br>
```
poetry install
```

## Usage
- Activate the environment<br>
```
poetry shell
```

- Initialize settings
```
python main.py initialize
```
> You should prepare the followings to initialize:<br>
> - __Naver Client ID__ from Naver Developer Center
> - __Naver Secret key__ from Naver Developer Center
> - __Github Access Token__
> - __Github Repository__ (`{your github id}/{your github repository name}`)<br>to post recommended movies

- Run commands<br>
```
python main.py [OPTIONS] COMMAND [ARGS]...
```

You can get detail usages by `--help` option.
```
python main.py --help
```
