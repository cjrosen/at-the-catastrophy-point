import sys
import os
from pdf2image import convert_from_path

if __name__ == "__main__":
    #print(sys.argv)
    if len(sys.argv) < 2:
        print("Usage:\n  'python pdf_to_image.py path/to/file.pdf'\n 'python pdf_to_image.py path/to/file.pdf PNG target/path'")
        exit(1)
    path = sys.argv[1]
    fmt = ('PNG' if len(sys.argv) < 3 else sys.argv[2]).lower()

    filenames = []

    if os.path.isdir(path):
        print(f"Will convert all files in folder '{path}' to '{fmt}' images")
        filenames = os.listdir(path)
    elif os.path.isfile(path):
        print(f"Will convert the file '{path}' to '{fmt}' image")
        path, filename = path.rsplit('/', maxsplit=1)
        filenames = [filename]
    else:
        print(f"File not found: '{path}'")
        exit(1)

    targetPath = path if len(sys.argv) < 4 else sys.argv[3]

    if not os.path.exists(targetPath):
        os.mkdir(targetPath)

    for filename in filenames:
        filebase, ext = os.path.splitext(filename)
        if ext.lower() == '.pdf':
            print(f"Converting '{path}/{filename}' ... ", end='', flush=True)
            convert_from_path(
                pdf_path = f"{path}/{filename}",
                output_folder = targetPath,
                single_file = True,
                output_file = f"{filebase}",
                fmt = fmt,
                dpi = 300
            )
            print("DONE")

    
    
