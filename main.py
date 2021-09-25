from ui.cli import Cli


def run_cli():
    """
    Starts the command line interface for themed word generator
    :return: None
    """
    cli = Cli()
    cli.run()


if __name__ == "__main__":
    run_cli()
