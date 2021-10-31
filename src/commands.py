import typer
import random
import string

from src import app
from src.settings import NV_URL
from src.request import APIRequest
from src.response import APIResponse
from src.enums import Genre
from src.utils import err_echo


@app.callback()
def callback():
    if not NV_URL:
        err_echo("No environment variables. You should set environment variables first.")
        err_echo("Execute 'set-env' automatically.")
        set_env()
        raise typer.Exit()


@app.command(help="Recommend a movie randomly")
def recommend(genre: str = typer.Option(str)):
    if genre and genre.upper() not in Genre.member_names():
        err_echo("Not supported genre.")
        raise typer.Exit()
    try:
        api_result = APIRequest(
            query=random.choice(list(string.ascii_lowercase)),
            start=random.randrange(10, 101),
            display=100,
            genre=genre or random.choice(Genre.member_names()),
        ).to_api()
    except Exception as e:
        err_echo(str(e))
        raise typer.Exit()

    resp = APIResponse.from_api(**api_result)

    if not resp.items or all(item.user_rating == 0 for item in resp.items):
        recommend(genre)
        return

    rcmd_movie = sorted(resp.items, key=lambda k: k.user_rating, reverse=True)[0]
    rcmd_movie.echo()


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
    client_id = typer.prompt("Naver Client ID: ")
    client_secret = typer.prompt("Naver Client Secret Key: ")
    github_access_token = typer.prompt("Github Acces Token: ")
    github_repo = typer.prompt("Repository to issue: ")

    with open(".env", "w") as env_file:
        env_file.write(f"NV_URL=https://openapi.naver.com/v1/search/movie\n")
        env_file.write(f"NV_CLIENT_ID={client_id}\n")
        env_file.write(f"NV_CLIENT_SECRET={client_secret}\n")
        env_file.write(f"GITHUB_ACCESS_TOKEN={github_access_token}\n")
        env_file.write(f"GITHUB_REPO={github_repo}\n")

    msg = typer.style("Setting Environment is completed successfully!", fg=typer.colors.GREEN)
    typer.echo(msg)
