from src.client import client
from src.server import server




def main():
    return server.Server(), client.Client()


if __name__ == "__main__":
    main()

    