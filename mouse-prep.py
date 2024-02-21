import glob
import numpy
import os

basePath = "/home/maga/Desktop/nnmouse/"

sourcePath = f"{basePath}/bl6_192"
sourceLabelPath = f"{sourcePath}/labels/final"

nnPath = f"{basePath}/raw/Dataset001_mouse/"
trainPath = f"{nnPath}/imagesTr"
testPath = f"{nnPath}/imagesTs"
labelPath = f"{nnPath}/labelsTr"

for path in [nnPath, trainPath, testPath, labelPath]:
    os.system(f"mkdir -p {path}")

cts = 0
labels = 0
for ctFile in glob.glob(f"{sourcePath}/*.nii.gz"):
    fileBase = ctFile.split("/")[-1][:-7]
    labelFile = f"{sourceLabelPath}/{fileBase}.nii.gz"
    cts += 1
    if os.path.exists(labelFile):
        labels += 1
        os.system(f"ln -s {ctFile} {trainPath}/{fileBase}_0000.nii.gz")
        os.system(f"ln -s {labelFile} {labelPath}/{fileBase}.nii.gz")
    else:
        os.system(f"ln -s {ctFile} {testPath}/{fileBase}_0000.nii.gz")
print(f"{cts} cts and {labels} labels")
print('done')

# from mouse-remap.py
# re-arrangine labelmaps

for labelFile in glob.glob(f"{labelPath}/*.nii.gz"):
    labelNode = slicer.util.loadVolume(labelFile)
    labelArray = slicer.util.arrayFromVolume(labelNode)
    for x in numpy.arange(5, 18, 1):
      labelArray[labelArray == x] = x-4
    #labelArray[labelArray == 102] = 49
    #labelArray[labelArray == 103] = 50
      slicer.util.arrayFromVolumeModified(labelNode)
      slicer.util.saveNode(labelNode, labelFile)
      slicer.mrmlScene.RemoveNode(labelNode)

