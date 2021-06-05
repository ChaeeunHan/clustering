from gensim.models import Word2Vec, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from gensim.test.utils import common_texts
from gensim.models.callbacks import CallbackAny2Vec
import pandas as pd
import operator
import numpy as np
import glob
import csv
import shutil
import os


class callback(CallbackAny2Vec):
  """Callback to print loss after each epoch."""

  def __init__(self):
    self.epoch = 0
    self.loss_to_be_subed = 0
  def on_epoch_end(self, model):
    loss = model.get_latest_training_loss()
    loss_now = loss - self.loss_to_be_subed
    self.loss_to_be_subed = loss
    print('Loss after epoch {}: {}'.format(self.epoch, loss_now))
    self.epoch += 1


csv_file = open("tag.csv")
reader = csv.reader(csv_file)
rows = list(reader)
print("# of clusters:{}".format(len(rows)))

vocab = []
corpus = []
cluster_tags = {}
for i,r in enumerate(rows):
  # vocab.extend(r)
  # corpus.extend(rows)
  cluster_tags.update({i:r})
# corpus = set(vocab)

# #train using corpus
documents = [TaggedDocument(row,[i]) for i,row in enumerate(rows)]
model = Doc2Vec(documents, vector_size=100, workers=4, callbacks=[callback()])
model.save("doc2vec.model")

path = "/nfs/home/hylee817/bigData/geo-clustering/new_clustered/"

for i in range(len(rows)):
  scores = []
  for idx, j in enumerate(range(len(rows))):
    score = model.similarity_unseen_docs(rows[i],rows[j])
    scores.append((score, idx))
  scores.sort(key=operator.itemgetter(0), reverse=True)

  print("cluster {} TOP 10 MATCH: {}".format(i, scores[:10]))

  #move photos
  threshold = 0.99
  candidates = [t[1] for t in scores if t[0] > threshold]
  candidates = candidates[:10]
  if len(candidates) >= 2:
    str_candidates = [str(c) for c in candidates]
    dir_name = "_".join(str_candidates) #new cluster name
    to_pth = path + dir_name + "/"
    if not os.path.exists(to_pth):
      os.makedirs(to_pth)
    for cand in candidates: #cand = dir / cluster
      from_pth = path + str(cand) + "/"
      for photo in glob.glob(from_pth +"*.jpg"): #imgs in single cluster
        try:
          shutil.copy(photo, to_pth + photo.replace(from_pth, ""))
        except shutil.SameFileError:
          continue
    print("CLUSTER {} COMBINED!".format(str_candidates))

# model = Word2Vec(rows, vector_size=100, workers=4, epochs=30, compute_loss=True, callbacks=[callback()])
# model.save("word2vec.model")

# model = Word2Vec.load("word2vec.model")
# with open('cluster_similarity.csv','w') as f:
#   wr = csv.writer(f)
#
#   for i in range(len(rows)):
#     scores = []
#     for j in range(len(rows)):
#       #compute similarity btw clusters
#       score = 0
#       for wi in range(len(rows[i])):
#         for wj in range(len(rows[j])):
#           score += model.n_similarity(rows[i][wi], rows[j][wj])
#       score /= (len(rows[i]) + len(rows[j]))
#       scores.append(score)
#     wr.writerow(scores)



# for
# model.similarity()
# # result = model.wv.most_similar("train")
# # print(result)

# labeled_clusters=[]
#
#
# model = Doc2Vec()
# model.build_vocab(labeled_clusters)
#
# for epoch in range(20):
#     model.train(labeled_clusters,epochs=model.iter,total_examples=model.corpus_count)
#     print("Epoch #{} is complete.".format(epoch+1))
# model.save("Doc2Vec.model")
# model.most_similar('lake')
# score = model.n_similarity(labe)