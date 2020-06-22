import argparse
import textwrap
import random
from itertools import groupby

def read_all(file_name):
  fh = open(file_name, 'r')
  faiter = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
  for header in faiter:
    headerStr = header.__next__()[:].strip()
    seq = "".join(s.strip() for s in faiter.__next__())
    yield (headerStr, seq)

def print_long(table):
  for i in range(0, len(table)):
    if((i+1)%70 == 0):
      print(table[i])
    else:
      print(table[i], end='')
      if(i==len(table)-1):
        print('')

def slice_middle(table, arg):
  table = table[:arg[0]] + table[arg[1]:]
  print_long(table)

def insert_fragment(table, start, fragment):
  table = table[:start] + fragment + table[start:]
  print_long(table)

def print_lengths(file_name):
  fiter = read_all(file_name)

  for ff in fiter:
    headerStr, seq = ff
    print(headerStr)
    print(len(seq))

def view(file_name, arg, name):
  fiter = read_all(file_name)
  for ff in fiter:
    headerStr, seq = ff 
    if(arg[0] == headerStr.split()[0][1:]):
      if name:
        print(headerStr)
      if(len(arg) > 1):
        coords = list(map(int,arg[1].split(':')))
        print_long(seq[coords[0]:coords[1]])
      else:
        print_long(seq)

def delete(file_name, arg):
  fiter = read_all(file_name)
  for ff in fiter:
    headerStr, seq = ff 
    print(headerStr)
    if(arg[0] == headerStr.split()[0][1:]):
      coords = list(map(int,arg[1].split(':')))
      slice_middle(seq,coords)
    else:
      print_long(seq)

def insert(file_name, arg):
  fiter = read_all(file_name)
  for ff in fiter:
    headerStr, seq = ff 
    print(headerStr)
    if(arg[0] == headerStr.split()[0][1:]):
      insert_fragment(seq,int(arg[1]),arg[2])
    else:
      print_long(seq)

def insert_random(file_name, arg):
  pass_arg = [arg[0], arg[1], ''.join(random.choices("ACGT", k=int(arg[2])))]
  insert(file_name, pass_arg)

def run():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  parser.add_argument("file", help="name of the file with extension in program catalog or path to file.")

  group.add_argument("-l","--length", help="shows length of all sequences.", action="store_true")
  group.add_argument("-v", "--view", nargs='+', help="Shows sequence. Slice with 'name start:end'")
  group.add_argument("-d", "--delete", nargs=2, help="Shows sequence with part deleted. 'name start:end'")
  group.add_argument("-i", "--insert", nargs=3, help="Shows sequence with added part. 'name start additional_sequence'")
  group.add_argument("-ir", "--insert_random", nargs=3, help="Shows sequence with added random part. 'name start length'")


  parser.add_argument("-n", "--name", action="store_true")
  parser.add_argument("-ver", "--version", action="version", version="%(prog)s 0.1")

  args = parser.parse_args()

  if args.file:
    if args.length:
      print_lengths(args.file)
    elif args.view:
      if args.name:
        view(args.file, args.view, True)
      else:
        view(args.file, args.view, False)
    elif args.delete:
      delete(args.file, args.delete)
    elif args.insert:
      insert(args.file, args.insert)
    elif args.insert_random:
      insert_random(args.file, args.insert_random)
  if args.length and not args.file:
    parser.error("File should be provided first, use --help [-h] for more information.")

if __name__ == "__main__":
  run()