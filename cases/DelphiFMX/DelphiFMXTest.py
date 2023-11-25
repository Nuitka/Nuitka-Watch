# nuitka-project: --standalone
# nuitka-project: --include-data-file={MAIN_DIRECTORY}/Unit3.pyfmx=Unit3.pyfmx

from delphifmx import *
from Unit3 import Form3


def main():
    Application.Initialize()
    Application.Title = "app3"
    Application.MainForm = Form3(Application)
    Application.MainForm.Show()
    Application.Run()
    Application.MainForm.Destroy()


if __name__ == "__main__":
    main()
