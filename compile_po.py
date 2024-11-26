import polib


def compile_po(po_file):
    po = polib.pofile(po_file)
    po.save_as_mofile(po_file.replace('.po', '.mo'))


if __name__ == "__main__":
    compile_po('locales/en/LC_MESSAGES/messages.po')
    compile_po('locales/de/LC_MESSAGES/messages.po')
