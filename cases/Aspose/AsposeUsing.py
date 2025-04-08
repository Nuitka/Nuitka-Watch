# nuitka-project: --mode=standalone
# nuitka-project: --include-data-file={MAIN_DIRECTORY}/testing.eml=testing.eml

import os

from aspose.email import mapi

def main():
    msg = mapi.MapiMessage.load(os.path.join(os.path.dirname(__file__), r"testing.eml"))
    print("Subject:", msg.subject)
    print("From:", msg.sender_email_address)


if __name__ == "__main__":
    main()