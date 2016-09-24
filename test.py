string = "do you have flights of (indigo) from (chennai) to (delhi)<=> airlines <=> location <=> location"

string_split = string.split("<=>")

string_example = string_split[0]

string_entities = string_split[1:]

no_of_entities = len(string_split)-1

open_paran_count = string_example.count('(')
close_paran_count = string_example.count(')')


if no_of_entities > 0:
    start_pos = 0
    entities_count = 0

    while entities_count != no_of_entities:
        start_pos = string_example.find('(',start_pos,len(string_example)) + 1
        end_pos   = string_example.find(')',start_pos,len(string_example)) - 1

        entity = string_example[start_pos:end_pos]
        entityLabel = string_entities[entities_count]

        print entity, entityLabel, start_pos, end_pos, string[start_pos],string[end_pos]

        entities_count+=1