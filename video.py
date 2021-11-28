from files.cli import *
import os


def main():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp')
    try:
        os.mkdir(path)
    except Exception:
        pass
    cli = Cli()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("завершение сеанса...")
    finally:
        clear_temps()


if __name__ == "__main__":
    main()
