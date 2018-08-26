import re;
import commands;

from random import randint;

def feed_tree1(blob, chain_tree, seed_list):
    blob = blob.replace("\n", " ");
    blob = blob + " ENDOFLINE";
    
    word_arr = blob.split(" ");

    if(word_arr and len(word_arr) > 0):
        # print('Leading word: ' + word_arr[0]);
        seed_list.append(word_arr[0]);

    for i in range(0, len(word_arr)):
        # print(str(i) + ': ' + word_arr[i] + '_' + word_arr[i+1]);
        if i+1 < len(word_arr):
            new_key = word_arr[i];
            if(not new_key in chain_tree):
                chain_tree[new_key] = list();
                
            chain_tree[new_key].append(word_arr[i+1]);
            # chain_tree[new_key] = word_arr[i+2];

    return chain_tree, seed_list;

    
def feed_tree2(blob, chain_tree):
    blob = blob.replace("\n", " ");

    word_arr = blob.split(" ");
    
    for i in range(0, len(word_arr)-1, 2):
        # print(str(i) + ': ' + word_arr[i] + '_' + word_arr[i+1]);
        if i+2 < len(word_arr):
            new_key = word_arr[i] + '_' + word_arr[i+1];
            # print(new_key);
            # print word_arr[i+2];
            if(not new_key in chain_tree):
                chain_tree[new_key] = list();
                
            chain_tree[new_key].append(word_arr[i+2]);
            # chain_tree[new_key] = word_arr[i+2];

    return chain_tree;

# def feed_tree3(blob, chain_tree)
#     blob = blob.replace("\n", " ");

#     word_arr = blob.split(" ");
#     for i in range(0, len(word_arr)-3, 3):
#         print(str(i) + ': ' + word_arr[i] + '_' + word_arr[i+1] + '_' + word_arr[i+2]);

def babble(chain_tree, seed_list, key, bab_phrase):
    bab_word = chain_tree[key][randint(0, len(chain_tree[key])-1)];

    # if re.match('.*[\.\?\!]', bab_word):
    if bab_word == "ENDOFLINE":
        return bab_phrase;
    else:
        bab_phrase = bab_phrase + ' ' + bab_word;
        bab_phrase = babble(chain_tree, seed_list, bab_word, bab_phrase);
        return bab_phrase;

def markov(name):
    chain_tree = {};
    seed_list = list();
    
    file_suffix = '_markov.txt';
    filename = name + file_suffix;
    
    cmd_out = commands.getstatusoutput('ls ' + name + '*' + file_suffix)[1];
    
    if(cmd_out.startswith('ls: cannot access') or len(cmd_out) < 2):
        return 'fail';
    else:
        print(cmd_out);
    
    with open(cmd_out) as file_content:
        blob_list = file_content.read().split('\n\n');

        for blob in blob_list:
            chain_tree, seed_list = feed_tree1(blob, chain_tree, seed_list);
        
        key = seed_list[randint(0, len(seed_list)-1)];

        bab_phrase = key;
        bab_phrase = babble(chain_tree, seed_list, key, bab_phrase);
        print('phrase: ' + bab_phrase);
        
        return bab_phrase;


# # filename = "test_sample.txt";
# # filename = "dave_yeager_markov.txt";
# with open(filename) as file_content:
#     chain_tree = {};

#     seed_list = list();
#     blob_list = file_content.read().split('\n\n');

#     # # For plays + dialogs + chats
#     # # THE NINA STRINGS ARE STILL IN THE TREE!
#     # for blob in blob_list:
#     #     # if blob.startswith("MASHA"):
#     #     if blob.startswith("NINA"):
#     #         chain_tree = feed_tree1(blob, chain_tree);

#     for blob in blob_list:
#         chain_tree, seed_list = feed_tree1(blob, chain_tree, seed_list);
    
#     # key = "a";
#     # while not (key.istitle()):
#     #     key = chain_tree.keys()[randint(0, len(chain_tree.keys())-1)];

#     key = seed_list[randint(0, len(seed_list)-1)];

#     for item in seed_list:
#         print('Seed: ' + item);

#     bab_phrase = key;
#     bab_phrase = babble(chain_tree, seed_list, key, bab_phrase);
#     print('phrase: ' + bab_phrase);

