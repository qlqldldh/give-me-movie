from typing import Union

from typer import Exit, Option, prompt, echo, progressbar

from src import app, cmd_manager
from src.git_repo import GithubRepo
from src.settings import NV_URL
from src.enums import Genre
from src.utils.echo import err_echo, success_echo


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
    if genre and not Genre.is_valid_value(genre.upper()):
        err_echo("Not supported genre.")
        raise Exit()
    try:
        movie = cmd_manager.recommend_movie(genre, query, year_from, year_to)
        movie.show()
    except Exception as e:
        err_echo(str(e))
        raise Exit()

    if post:
        gh_obj = GithubRepo()
        gh_obj.create_issue(movie, genre)
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

    cmd_manager.reset_env(
        client_id=client_id,
        client_secret=client_secret,
        github_access_token=github_access_token,
        github_repo=github_repo,
    )

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
    with progressbar(Genre.member_names()) as genres:
        cmd_manager.set_genre_categories(genres)
    success_echo("Creating genre labels is done successfully!")
