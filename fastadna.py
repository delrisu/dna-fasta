import argparse
import re

def print_lengths(file_name, extra = False):
  f = open(file_name, "r")

  line_len = 0
  for line in f:
    if(line[0] == ">"):
      if(line_len != 0):
        print(line_len)
        if extra:
          print('')
      line_len = 0
      if(line[-1] != "\n"):
        print(line)
      else:
        print(line[:-1])
    elif(line != "\n"):
      line_len += len(line) - line.count("\n")
      
  print(line_len)

def view(file_name, arg):
  f = open(file_name, "r")
  data = ''

  if(len(arg) > 1):
    coords = list(map(int,arg[1].split(':')))
    if(coords[1] <= coords[0]):
      print("Error: End <= Start!")
    else:
      found = False
      for line in f:
        if(found):
          
          if(line[0] == ">"):
            break
          elif(line[0] == '\n'):
            continue
          else:
            data+=line[:-1]
            if (len(data) >= coords[1]):
              print(data[coords[0]:coords[1]])
              break

        if(line[0] == ">"):
          if(arg[0] == line.split()[0][1:]):
            found = True
  else:
    found = False
    for line in f:
      if(found):
        if(line[0] == ">"):
          break
        else:
          print(line, end = '')
      if(line[0] == ">"):
        if(arg[0] == line.split()[0][1:]):
          found = True

def run():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  parser.add_argument("file", help="name of the file with extension in program catalog or path to file.")

  group.add_argument("-l","--length", help="shows length of all sequences.", action="store_true")
  group.add_argument("-v", "--view", nargs='+', help="shows sequence.")

  parser.add_argument("-enl", "--extranl", help="prints extra new lines between results of --length [-l].", action="store_true")
  parser.add_argument("-ver", "--version", action="version", version="%(prog)s 0.1")

  args = parser.parse_args()

  if args.file:
    if args.length:
      if args.extranl:
        print_lengths(args.file, True)
      else:
        print_lengths(args.file)
    if args.view:
      view(args.file, args.view)
  if args.length and not args.file:
    parser.error("File should be provided first, use --help [-h] for more information.")
  if args.extranl and not args.length:
    parser.error("Extra new lines options works only with --length [-l].")

if __name__ == "__main__":
  run()