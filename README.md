# dna-fasta

[Trello](https://trello.com/b/BbZVxT4g/dna-fasta)

## Command line arguments:

```
file - name of the file with extension in program catalog or path to file. ex: fastadna.py test.fa
--length [-l] - Shows length of all sequences.
--view [-v] - Shows sequence. Use: --view name <start:end>
--delete [-d] - Shows sequence with part deleted. Use: --delete name start:end
--insert [-i] - Shows sequence with added part. Use: --insert name start additional_sequence
--insert_random [-ir] - Shows sequence with added random part. Use: --insert_random name start length
--translocate [-t] - Translocates fragment. Use: --translocate name1 start:end <name2> index
--reverse [-r] - Reverses and translates fragment. Use: --reverse name <start:end>
--version [-ver] - Prints version
--name [-n] - Prints name in --view [-v]
--line_length [-ll] - Allows to decide lenght of line in prints. Use: --line_length length
```
