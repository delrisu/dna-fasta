import argparse
import textwrap
import random

def print_long(table):
  for i in range(0, len(table)):
    if((i+1)%70 == 0):
      print(table[i])
    else:
      print(table[i], end='')

def slice_middle(table, arg):
  table = table[:arg[0]] + table[arg[1]:]
  print_long(table)

def insert_fragment(table, start, fragment):
  table = table[:start] + fragment + table[start:]
  print_long(table)

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
                print_long(data[coords[0]:coords[1]])   
                outed = True
                break

          if(line[0] == ">"):
            if(arg[0] == line.split()[0][1:]):
              print(line[:-1] + ' ' + arg[1])
              found = True
        if(found and not outed):
          print_long(data[coords[0]:coords[1]])     
    else:
      found = False
      for line in f:
        if(found):
          if(line[0] == ">"):
            break
          elif(line[0] == "\n"):
            continue
          else:
            print(line, end = '')
        if(line[0] == ">"):
          if(arg[0] == line.split()[0][1:]):
            found = True

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

def insert(file_name, arg):
  with open(file_name, "r") as f:
    data = ''
    found = False
    for line in f:
      if(found):
        if(line[0] == ">"):
          break
        elif(line[0] == "\n"):
          continue
        else:
          data+=line[:-1]
      if(line[0] == ">"):
        if(arg[0] == line.split()[0][1:]):
          found = True
    insert_fragment(data,int(arg[1]),arg[2])

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
    elif args.insert:
      insert(args.file, args.insert)
    elif args.insert_random:
      insert_random(args.file, args.insert_random)
  if args.length and not args.file:
    parser.error("File should be provided first, use --help [-h] for more information.")
  if args.extranl and not args.length:
    parser.error("Extra new lines options works only with --length [-l].")

if __name__ == "__main__":
  run()