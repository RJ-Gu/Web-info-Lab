import gzip
import json
from tqdm import tqdm
# 第二次jump，根据第一次sample后的三元组集合获取相连的三元组集合
movie_triplet_dict = None

with open("output/sampled_movie_triplet_dict.json", "r") as f:
    movie_triplet_dict = json.load(f)
# 找出所有涉及到的entity
all_entity = set({})
for movie in movie_triplet_dict:
    all_triplet = movie_triplet_dict[movie]
    for triplet in all_triplet:
        head_entity = triplet[0]
        tail_entity = triplet[2]
        all_entity.add(head_entity)
        all_entity.add(tail_entity)

line_count = 395577070
# 遍历一遍字典，找出所有相关的triplet，存在gz文件中
with gzip.open("data/freebase_douban.gz", 'rb') as read_file:
    with gzip.open("data/2step.gz", "wb") as write_file:
        for line_num, line in tqdm(enumerate(read_file, start=1), total=line_count):
            line = line.strip()
            triplet = line.decode().split('\t')[:3]
            head_entity = triplet[0]
            relationship = triplet[1]
            tail_entity = triplet[2]
            if triplet[1].startswith("<http://rdf.freebase.com/ns"):
                if head_entity in all_entity or tail_entity in all_entity:
                    written_triplet = head_entity + "\t" + relationship + "\t" + tail_entity + "\n"
                    written_triplet = written_triplet.encode()
                    write_file.write(written_triplet)



