from descriptor import ColorDescriptor
from searcher import Searcher
import matplotlib.pyplot as plt
from tqdm import tqdm
import glob
import cv2
import os.path
from operator import itemgetter
import shutil
import pandas as pd
import csv

class VisualCluster():
  def __init__(self):
    self.clusters = [0]
    self.dataset_pth = "clustered/"
    self.cd = ColorDescriptor((8, 12, 3))
    self.copied = []
    self.cluster_ind = 0
    self.tag_file = "Tag.csv"
    self.tag_path = 'clustered/0/tag.csv'
    self.frequent_tags = {'seattle': 7564, 'washington': 2958, 'usa': 785, 'wa': 718, 'convention': 667, '2009': 533, 'square': 512, 'redmond': 509, '2012': 501, 'iphoneography': 492, 'uploaded:by=instagram': 489, 'squareformat': 481, 'instagramapp': 478, 'park': 474, 'rf': 444, 'unitedstates': 431, '2010': 411, 'furry': 402, 'con': 402, 'rainfurrest': 402, 'rf2012': 402}
    self.tags_csv = pd.read_csv(self.tag_file, names= ['img number', 'num tag', 'str tag'])

  def write_tags(self, searchResults, writer):
    # print(searchResults)
    tags = []
    for (score, resultID) in searchResults:
      tag = self.tags_csv.loc[(self.tags_csv['img number'].astype(str) == resultID.split('.')[0])]['str tag']
      for t in tag:
        if t not in self.frequent_tags and t not in tags:
          tags.append(t)
    writer.writerow(tags)

  def make_index(self, cluster_pth, index_file):
    # open the output index file for writing
    output = open(index_file, "w")

    # use glob to grab the image paths and loop over them
    for imagePath in glob.glob(cluster_pth + "*.jpg"):
      # extract the image ID (i.e. the unique filename) from the image
      # path and load the image itself
      imageID = imagePath[imagePath.rfind("/") + 1:]
      image = cv2.imread(imagePath)
      # print(imageID)

      # describe the image
      features = self.cd.describe(image)

      # write the filename of the image
      # and its associated feature vector to file.
      features = [str(f) for f in features]
      output.write("%s,%s\n" % (imageID, ",".join(features)))

    # close the index file
    output.close()


  def run_search(self, query_pth, index_file, cluster, writer):
    # load the query image and describe it
    query = cv2.imread(query_pth)
    features = self.cd.describe(query)

    # perform the search
    searcher = Searcher(index_file)
    results = searcher.search(features, limit=5)

    for (score, resultID) in results:
      img = self.dataset_pth + '0/' + resultID
      copy_dir = self.dataset_pth + '0/' + str(self.cluster_ind) + '/' + resultID
      # print(resultID, img, copy_dir)
      shutil.copy(img, copy_dir)
      self.copied.append(resultID)
    self.write_tags(results,writer)

  def createDirectory(self, directory):
    try:
      if not os.path.exists(directory):
        os.makedirs(directory)
    except OSError:
      print("Error: Failed to create the directory.")

  def main(self):

    #iterate over all primary geo-clusters
    for cluster in tqdm(self.clusters):
      cluster_pth = self.dataset_pth + str(cluster) + "/"
      idx_file = cluster_pth + "index.csv"

      #make index file
      if (os.path.isfile(idx_file)):
        print(idx_file + ' already exists.')
      else:
        self.make_index(cluster_pth, idx_file)
        print("index file created: " + idx_file)

      with open(self.tag_path, 'w') as writefile:
        writer = csv.writer(writefile)
        for imagePath in glob.glob(cluster_pth + "*.jpg"):
          if imagePath not in self.copied:
            print(self.cluster_ind)
            self.createDirectory(self.dataset_pth + '0/' + str(self.cluster_ind))
            self.run_search(imagePath, idx_file, cluster_pth, writer)
            self.cluster_ind += 1

if __name__ == "__main__":
  VC = VisualCluster()
  VC.main()
