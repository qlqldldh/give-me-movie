from typing import Union
import random
import string

from typer import Exit, Option, prompt

from src import app
from src.settings import NV_URL
from src.request import APIRequest
from src.response import APIResponse
from src.enums import Genre
from src.utils.echo import err_echo, success_echo


@app.callback()
def callback():
    if not NV_URL:
        err_echo(
            "No environment variables. You should set environment variables first."
        )
        err_echo("Execute 'set-env' automatically.")
        set_env()
        raise Exit()


@app.command(help="Recommend a movie randomly")
def recommend(
    genre: str = Option("", prompt=True),
    query: str = Option("", show_default=False),
    year_from: Union[None, int] = Option(None, show_default=False),
    year_to: Union[None, int] = Option(None, show_default=False),
):
    if genre and genre.upper() not in Genre.member_names():
        err_echo("Not supported genre.")
        raise Exit()
    try:
        api_result = APIRequest(
            query=query or random.choice(list(string.ascii_lowercase)),
            start=random.randrange(1, 1001),
            display=100,
            genre=genre or random.choice(Genre.member_names()),
            year_from=year_from,
            year_to=year_to,
        ).to_api()
    except Exception as e:
        err_echo(str(e))
        raise Exit()

    resp = APIResponse.from_api(**api_result)

    if not resp.items:
        recommend(genre, query, year_from, year_to)
        return

    rcmd_movie = sorted(resp.items, key=lambda k: k.user_rating, reverse=True)[0]
    rcmd_movie.show()


@app.command()
def set_env():
    """
    Set necessary environmental variables to use this recommender.\n
    Data about movies come from Naver's API server,\n
    so you need to set Naver-related variables.\n
    You can get 'Naver Client ID', 'Naver Client Secret Key' from here:\n
        [https://developers.naver.com/main/]\n
    Github access token is your issued access token from Github,\n
    and it is necessary when you issue recommended movie to your Github repository.\n
    """
    client_id = prompt("Naver Client ID: ")
    client_secret = prompt("Naver Client Secret Key: ")
    github_access_token = prompt("Github Acces Token: ")
    github_repo = prompt("Repository to issue: ")

    with open(".env", "w") as env_file:
        env_file.write(f"NV_URL=https://openapi.naver.com/v1/search/movie\n")
        env_file.write(f"NV_CLIENT_ID={client_id}\n")
        env_file.write(f"NV_CLIENT_SECRET={client_secret}\n")
        env_file.write(f"GITHUB_ACCESS_TOKEN={github_access_token}\n")
        env_file.write(f"GITHUB_REPO={github_repo}\n")

    success_echo("Setting Environment is completed successfully!")
