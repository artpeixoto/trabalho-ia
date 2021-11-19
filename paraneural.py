import keras
import keras.layers as layers
import keras.preprocessing as preprocessing
import tensorflow as tf2
import tensorflow.data as tfds
import keras.datasets as datasets
import numpy as np
from collections import defaultdict
#dddict = lambda *args, **kwargs: defaultdict(*args, **kwargs).setdefault(dddict)
#oldDict = dict
#dict = dddict

#para executar o codigo externamente:
#

exampleHyperParams = {
    "test": {

    }, 
    "train": {
        "epochs": 10,                                               #gen1
        "batch_size" : 128,                                         #gen2
        "use_multiprocessing" : True,                               #gen3    
        "workers" : 8                                               #gen4
    }, 
    "model":{
        "layersArgs": [
            ("Dense", {"units": 64, "activation":"ReLU"}),          #gen5, 6
            ("Dense", {"units": 128,"activation":"ReLU"}),          #gen7, 8
            ("Dense", {"units": 32, "activation":"ReLU"}),          #gen9, 10
            ("Dense", {"units": 10, "activation":"log_softmax"})    #gen11, 12
        ], "optimizer": "adam"                                      #gen13
        ,  "loss" : "SparseCategoricalCrossentropy"                 #gen14 mas nao posso mudar
    }
}

def buildAll(
        hParams= exampleHyperParams,
        verbose=True
    ):
    dataset = getDataset(
        #datasetPreparers=getDatasetPreparers(),                    
        datasetName="mnist")
    model = makeModel(**hParams["model"])
    trainFunction = lambda **x: trainModel(model, dataset["train"], **hParams["train"], **x)
    testFunction = lambda **x: testModel(model, dataset["test"], **x) 
    return testFunction, trainFunction, model, dataset

def getDataset(datasetPreparers = [(lambda x: x),( lambda x: x)], datasetName="mnist"):
#   eval(f"import datasets.{datasetName} as dsModule")
    import keras.datasets.mnist as dsModule
    dsDict = \
        {i: (data) for i, data in 
            zip(
                ["train", "test"],
                dsModule.load_data(),
                )
            }
    for key, data in dsDict.items():
        x, y = data
        newData = datasetPreparers[0](x), datasetPreparers[1](y)
        dsDict.update({key: newData})
    
    return dsDict

def getDatasetPreparers():
    prepareY = lambda y: preprocessing.utils.to_categorical(y, dtype="int8") #transformando a matriz em esparsa
    prepareX = lambda x: x
    return (prepareX, prepareY)


def makeModel(layersArgs=[
            ("Dense", {"units": 64, "activation":"ReLU"}),
            ("Dense", {"units": 128,"activation":"ReLU"}),
            ("Dense", {"units": 32,"activation":"ReLU"}),
            ("Dense", {"units": 10,"activation":"log_softmax"})
        ],  optimizer="adagrad",
            loss="SparseCategoricalCrossentropy"
    ):

    layers = [eval(f"keras.layers.{layerName}") (**parm) for (layerName, parm) in layersArgs]
    model = keras.Sequential([
                keras.layers.InputLayer((28,28)), 
                keras.layers.Flatten(),
                *layers,
                keras.layers.Softmax()
            ])
    model.compile(optimizer=optimizer, loss=loss)
    return model

def trainModel(
        model: keras.Sequential, 
        train_dataset,
        use_multiprocessing=True,
        **kwargs
    ):
    from copy import deepcopy
    xTrain, yTrain = train_dataset
    results = model.fit(x=xTrain, y=yTrain,
                        use_multiprocessing=use_multiprocessing,
                        **kwargs)
    return model, results

def testModel(model: keras.Sequential,
        testingDataset, 
        **kwargs
    ):
    return model.evaluate(*testingDataset, **kwargs)



