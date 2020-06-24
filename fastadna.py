import argparse
import random
from itertools import groupby

LINE_LENGTH = 70

def read_all(file_name):
  fh = open(file_name, 'r')
  faiter = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
  for header in faiter:
    headerStr = header.__next__()[:].strip()
    seq = "".join(s.strip() for s in faiter.__next__())
    yield (headerStr, seq)

def print_long(table):
  for i in range(0, len(table)):
    if((i+1)%LINE_LENGTH == 0):
      print(table[i])
    else:
      print(table[i], end='')
      if(i==len(table)-1):
        print('')

def slice_middle(table, arg):
  table = table[:arg[0]] + table[arg[1]:]
  return table

def insert_fragment(table, start, fragment):
  table = table[:start] + fragment + table[start:]
  return table

def print_lengths(file_name):
  fiter = read_all(file_name)

  for ff in fiter:
    headerStr, seq = ff
    print(headerStr)
    print(len(seq))

def get_fragment(file_name, arg, name):
  fiter = read_all(file_name)
  for ff in fiter:
    headerStr, seq = ff 
    if(arg[0] == headerStr.split()[0][1:]):
      if name:
        print(headerStr)
      if(len(arg) > 1):
        coords = list(map(int,arg[1].split(':')))
        return seq[coords[0]:coords[1]]
      else:
        return seq

def get_without_fragment(file_name, arg):
  fiter = read_all(file_name)
  for ff in fiter:
    headerStr, seq = ff 
    print(headerStr)
    if(arg[0] == headerStr.split()[0][1:]):
      coords = list(map(int,arg[1].split(':')))
      return slice_middle(seq,coords)

def view(file_name, arg, name):
  print_long(get_fragment(file_name, arg, name))

def delete(file_name, arg):
  fiter = read_all(file_name)
  for ff in fiter:
    headerStr, seq = ff 
    print(headerStr)
    if(arg[0] == headerStr.split()[0][1:]):
      coords = list(map(int,arg[1].split(':')))
      print_long(slice_middle(seq,coords))
    else:
      print_long(seq)

def insert(file_name, arg):
  fiter = read_all(file_name)
  for ff in fiter:
    headerStr, seq = ff 
    print(headerStr)
    if(arg[0] == headerStr.split()[0][1:]):
      print_long(insert_fragment(seq,int(arg[1]),arg[2]))
    else:
      print_long(seq)

def insert_random(file_name, arg):
  pass_arg = [arg[0], arg[1], ''.join(random.choices("ACGT", k=int(arg[2])))]
  insert(file_name, pass_arg)

def translocate(file_name, arg):
  if len(arg) < 3:
    print("Error: Too few arguments in translate")
  elif len(arg) > 4:
    print("Error: Too many arguments in translate")
  else:
    dic = {}
    name_dic = {}
    fiter = read_all(file_name)
    for ff in fiter:
      headerStr, seq = ff
      name_dic[headerStr.split()[0][1:]] = headerStr
      dic[headerStr.split()[0][1:]] = seq
  if len(arg) == 3:
    coords = list(map(int,arg[1].split(':')))
    fragment = dic[arg[0]][coords[0]:coords[1]]
    if(int(arg[2]) > coords[1]):
      dic[arg[0]] = dic[arg[0]][:int(arg[2])] + fragment + dic[arg[0]][int(arg[2]):]
      dic[arg[0]] = dic[arg[0]][:coords[0]] + dic[arg[0]][coords[1]:]
    elif(int(arg[2]) < coords[0]):
      dic[arg[0]] = dic[arg[0]][:coords[0]] + dic[arg[0]][coords[1]:]
      dic[arg[0]] = dic[arg[0]][:int(arg[2])] + fragment + dic[arg[0]][int(arg[2]):]
    for key in dic:
      print(name_dic[key])
      print_long(dic[key])
  elif len(arg) == 4:
    coords = list(map(int,arg[1].split(':')))
    fragment = dic[arg[0]][coords[0]:coords[1]]
    dic[arg[0]] = dic[arg[0]][:coords[0]] + dic[arg[0]][coords[1]:]
    dic[arg[2]] = dic[arg[2]][:int(arg[3])] + fragment + dic[arg[2]][int(arg[3]):]
    for key in dic:
      print(name_dic[key])
      print_long(dic[key])


def run():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  parser.add_argument("file", help="name of the file with extension in program catalog or path to file.")

  group.add_argument("-l","--length", help="shows length of all sequences.", action="store_true")
  group.add_argument("-v", "--view", nargs='+', help="Shows sequence. Slice with 'name start:end'")
  group.add_argument("-d", "--delete", nargs=2, help="Shows sequence with part deleted. 'name start:end'")
  group.add_argument("-i", "--insert", nargs=3, help="Shows sequence with added part. 'name start additional_sequence'")
  group.add_argument("-ir", "--insert_random", nargs=3, help="Shows sequence with added random part. 'name start length'")
  group.add_argument("-t", "--translocate", nargs="+")


  parser.add_argument("-n", "--name", action="store_true", help="Prints name in --view [-v]")
  parser.add_argument("-ver", "--version", action="version", version="%(prog)s 0.1")
  parser.add_argument("-ll", "--line_length", nargs=1, help="Allows to decide lenght of line in prints")

  args = parser.parse_args()

  

  if args.file:
    if args.line_length:
      global LINE_LENGTH
      LINE_LENGTH = int(args.line_length[0])
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
    elif args.translocate:
      translocate(args.file, args.translocate)
  if args.length and not args.file:
    parser.error("File should be provided first, use --help [-h] for more information.")

if __name__ == "__main__":
  run()