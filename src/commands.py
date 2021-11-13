from typing import Union

from typer import Exit, Option, prompt, echo, progressbar
from github import GithubException

from src import app
from src.git_repo import GithubRepo
from src.settings import NV_URL
from src.request import APIRequest
from src.response import APIResponse
from src.enums import Genre
from src.utils.echo import err_echo, success_echo
from src.utils.random_ import rand_int, rand_word, rand_letter


@app.command(help="Recommend a movie randomly")
def recommend(
    genre: str = Option("", prompt=True),
    query: str = Option("", show_default=False),
    year_from: Union[None, int] = Option(None, show_default=False),
    year_to: Union[None, int] = Option(None, show_default=False),
    post: bool = Option(False),
):
    if not NV_URL:
        err_echo("No environment variables.")
        err_echo("You should set environment variables first or initialize for this.")
        raise Exit()
    if genre and genre.upper() not in Genre.member_names():
        err_echo("Not supported genre.")
        raise Exit()
    try:
        api_result = APIRequest(
            query=query or rand_letter(),
            start=rand_int(1, 1001),
            display=100,
            genre=genre or rand_word(Genre.member_names()),
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

    if post:
        gh_obj = GithubRepo()
        gh_obj.create_issue(rcmd_movie, genre)
        success_echo("* movie is posted successfully!")


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


@app.command()
def initialize():
    """
    Initialize for recommender.\n
    Setting environments and create genre labels.
    """
    if not NV_URL:
        echo("# Set environment for recommender...")
        set_env()

    echo("# Create labels of genre in repository...")
    gh = GithubRepo()
    with progressbar(Genre.member_names()) as genres:
        for genre in genres:
            try:
                gh.create_genre_labels(genre)
            except GithubException:
                pass
    success_echo("Creating genre labels is done successfully!")
