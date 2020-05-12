import sys
sys.path.append("./scripts")

from server import Server

def main():
    s = Server()
    s.startPolling()

if __name__ == "__main__":
    main()