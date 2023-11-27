from view import View
from server import Server
from controller import Controller


def main():
    server = Server()
    view = View()
    controller = Controller(view, server)
    controller.run_view()
    server.server_close()


if __name__ == "__main__":
    main()
