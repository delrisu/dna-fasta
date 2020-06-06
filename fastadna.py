import argparse

def print_lengths(file_name, extra = False):
  f = open(file_name, "r")
  line_len = 0
  for line in f:
    if(line[0] == ">"):
      if(line_len != 0):
        print(line_len)
        if not extra:
          print('\n')
      line_len = 0
      if(line[-1] != "\n"):
        print(line)
      else:
        print(line[:-1])
    elif(line != "\n"):
      line_len += len(line) - line.count("\n")
  print(line_len)

def run():
  parser = argparse.ArgumentParser()
  parser.add_argument("-f","--file", help="name of the file with extention in program catalog. ex: fastadna.py --file test.fa")
  parser.add_argument("-l","--length", help="shows length of all sequences. Use ONLY with --file [-f]", action="store_true")
  parser.add_argument("-nn", "--nonl", help="don't print extra new lines in result of --length [-l]", action="store_true")

  args = parser.parse_args()

  if args.file:
    if args.length:
      if args.nonl:
        print_lengths(args.file, True)
      else:
        print_lengths(args.file)
  if args.length and not args.file:
    print("Error: File should be provided first, use --help [-h] for more information.")

if __name__ == "__main__":
  run()