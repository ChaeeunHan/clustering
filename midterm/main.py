from descriptor import ColorDescriptor
from searcher import Searcher
import matplotlib.pyplot as plt
from tqdm import tqdm
import glob
import cv2
import os.path

class VisualCluster():
  def __init__(self):
    self.clusters = list(range(8))
    # self.clusters = [2,3,4,5,6]
    # self.clusters = [4,5,6]
    self.dataset_pth = "clustered/"

    self.cd = ColorDescriptor((8, 12, 3))

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


  def run_search(self, query_pth, index_file, cluster):
    # load the query image and describe it
    query = cv2.imread(query_pth)
    features = self.cd.describe(query)

    # perform the search
    searcher = Searcher(index_file)
    results = searcher.search(features, limit=15)

    # display the query
    # cv2.imshow("Query", query)

    # output file for img names
    save_name = query_pth.replace("/", "_") + '.csv'
    output = open(save_name, "w")

    # loop over the results
    imgs = []
    for (score, resultID) in results:
      # load the result image and display it
      imgs.append(cv2.imread(cluster + resultID))
      # print(resultID)
      output.write('%s\n' % resultID)
      # result = cv2.imread(self.dataset_pth + "/" + resultID)
      # cv2.imshow("Result", result)
      # cv2.waitKey(0)

    output.close()
    # save_name = query_pth.replace("clustered/","").replace("/","_")
    # print("visual cluster saved at: " + save_name)
    # self.show_images(imgs, save_name)


  # def show_images(self, images, name, figsize=(20, 10), columns=5):
  #   plt.figure(figsize=figsize)
  #   plt.tight_layout()
  #
  #   for i, image in enumerate(images):
  #     ax = plt.subplot(len(images) / columns + 1, columns, i + 1)
  #     plt.setp(ax.get_xticklabels(), visible=False)
  #     plt.setp(ax.get_yticklabels(), visible=False)
  #     plt.imshow(image)
  #
  #   plt.suptitle("Visual cluster from Geo-cluster " + name[:name.index("_")])
  #   fig = plt.gcf()
  #   plt.show()
  #   #save as a single image file
  #   fig.savefig("results/" + name  + ".png")
  #   plt.cla()

  def save_txt(self, imgaes):
    for i, image in enumerate(images):
      break


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

      #actual search (each img)
      # print(len(glob.glob(cluster_pth + "*.jpg")))
      for imagePath in ['clustered/0/3286772707.jpg']:
        # print(imagePath)
        self.run_search(imagePath, idx_file, cluster_pth)


if __name__ == "__main__":
  VC = VisualCluster()
  VC.main()
