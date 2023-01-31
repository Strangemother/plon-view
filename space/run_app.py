"""Run plon, configured to look at a booted plew.
"""
from plon import run

def main():
    print('Run.')
    url = "http://localhost:8000/alpha/"
    run(url=url)


if __name__ == '__main__':
    main()
