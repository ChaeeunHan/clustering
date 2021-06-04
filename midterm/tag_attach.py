from tqdm import tqdm
import glob
import os.path
import csv
import pandas as pd
from operator import itemgetter

class Tag():
  def __init__(self):
    self.tag_file = "Tag.csv"
    self.write_path = ['tag_attached/', 'tag_attached_filtered/']
    self.frequency = {}

    self.tag_path = 'clustered/0/tag.csv'

    self.cluster_ind = 0
    self.dataset_pth = "clustered/0/"

  def tag_attach(self, tags_csv, frequent, filter):
    for clustered_file in glob.glob("*.jpg.csv"):
        with open(clustered_file,  newline='') as csvfile, \
            open(self.write_path[filter] + clustered_file, 'w') as writefile:
            reader = csv.reader(csvfile)
            writer = csv.writer(writefile)
            for row in reader:
                img_number = row[0].split('.')[0]
                tag = tags_csv.loc[(tags_csv['img number'].astype(str) == img_number)]['str tag']

                for t in tag:
                    if filter == 1:
                        if t not in frequent:
                            writer.writerow([img_number] + [t])
                    else:
                        writer.writerow([img_number] + [t])

  def tag_frequency(self, tags_csv):
    for tag in tags_csv['str tag']:
        if tag in self.frequency:
            self.frequency[tag] += 1
        else:
            self.frequency[tag] = 1

  def tags_in_row(self, tags_csv, frequent):
      with open(self.tag_path, 'w') as writefile:
        writer = csv.writer(writefile)
        for cluster_ind in range(892):
            print(cluster_ind)
            tags = []
            for imagePath in glob.glob(self.dataset_pth + str(cluster_ind) + "/*.jpg"):
                tag = tags_csv.loc[(tags_csv['img number'].astype(str) == imagePath.split('/')[3][:-4])][
                      'str tag']
                for t in tag:
                    if t not in frequent and t not in tags:
                        tags.append(t)
            writer.writerow(tags)
            # print(tags)

  def main(self):

    tags_csv = pd.read_csv(self.tag_file, names= ['img number', 'num tag', 'str tag'])

    #get the tags with high frequency
    self.tag_frequency(tags_csv)
    sort = dict(sorted(self.frequency.items(), key=itemgetter(1), reverse=True)[:21])
    # print(sort)

    # self.tag_attach(tags_csv, sort, 0)
    # self.tag_attach(tags_csv, sort, 1)

    self.tags_in_row(tags_csv, sort)

if __name__ == "__main__":
  T = Tag()
  T.main()
