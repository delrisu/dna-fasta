import argparse
import re
import textwrap

def print_lengths(file_name, extra = False):
  with open(file_name, "r") as f:

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
  with open(file_name, "r") as f:
    data = ''
    outed = False

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
                for wrap in textwrap.wrap(data[coords[0]:coords[1]],70):
                  print(wrap)
                  outed = True
                break

          if(line[0] == ">"):
            if(arg[0] == line.split()[0][1:]):
              print(line[:-1] + ' ' + arg[1])
              found = True
        if(found and not outed):
          for wrap in textwrap.wrap(data[coords[0]:coords[1]],70):
            print(wrap)      
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

def slice_middle(table, arg):
  table = table[:arg[0]] + table[arg[1]:]
  for i in range(0, len(table)):
    if(i > 0 and i%70 == 0):
      print(table[i])
    else:
      print(table[i], end='')

def delete(file_name, arg):
  with open(file_name, "r") as f:
    data = ''
    outed = False

    coords = list(map(int,arg[1].split(':')))
    if(coords[1] <= coords[0]):
      print("Error: End <= Start!")
    else:
      found = False
      for line in f:
        if(found):
          if(line[0] == ">"):
            slice_middle(data,coords)
            outed = True
            break
          elif(line[0] == '\n'):
            if(len(data) == 0):
              continue
            else:
              slice_middle(data,coords)
              outed = True
              break
          else:
            data+=line[:-1]
        if(line[0] == ">"):
          if(arg[0] == line.split()[0][1:]):
            print(line[:-1] + ' -' + arg[1])
            found = True
      if(found and not outed):
        slice_middle(data,coords)

def run():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  parser.add_argument("file", help="name of the file with extension in program catalog or path to file.")

  group.add_argument("-l","--length", help="shows length of all sequences.", action="store_true")
  group.add_argument("-v", "--view", nargs='+', help="Shows sequence. Slice with 'name start:end'")
  group.add_argument("-d", "--delete", nargs=2, help="Shows sequence with part deleted. 'name start:end'")

  parser.add_argument("-enl", "--extranl", help="prints extra new lines between results of --length [-l].", action="store_true")
  parser.add_argument("-ver", "--version", action="version", version="%(prog)s 0.1")

  args = parser.parse_args()

  if args.file:
    if args.length:
      if args.extranl:
        print_lengths(args.file, True)
      else:
        print_lengths(args.file)
    elif args.view:
      view(args.file, args.view)
    elif args.delete:
      delete(args.file, args.delete)
  if args.length and not args.file:
    parser.error("File should be provided first, use --help [-h] for more information.")
  if args.extranl and not args.length:
    parser.error("Extra new lines options works only with --length [-l].")

if __name__ == "__main__":
  run()