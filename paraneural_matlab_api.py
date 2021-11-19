import paraneural
from timeit import Timer
import enum
import itertools as itert
#nesse modulo, testamos os algoritmos de paraneural, alterando o parametros das redes neurais. Os parametros sao codificados em genes e otimizados por algoritmos geneticos

def getLog():
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger

def parseDna(dna): #recebe uma lista de inteiros e transforma em genes que o modulo paraneural pode entender
    def parseTrainGenes(epochs, batchSize, use_multiprocessing, workers):
        return {
            "epochs" : epochs,
            "batchSize" : 2**n,
            "use_multiprocessing" : use_multiprocessing != 0,
            "workers" : workers
        }
    def parseLayerGenes(n_units, activation):
        return {
            "n_units" : n_units,
            "activation" : [
                "relu",
                "leaky_relu",
                "sigmoid",
                "softmax",
                "softplus",
                "tanh",
                "hard_sigmoid",
                "exponential"
            ] [activation]
        }
    def parseOptimizer(optimizer):
        return {
            "optimizer" : [
                "adadelta",
                "adagrad",
                "adam",
                "adamax"
            ][optimizer]
    }
    hParams = {
        "train": parseTrainGenes(dna[:4]),
        "model": {
            "layersArgs" : [parseLayerGenes(dna[4+ i*2], dna[4+ i*2 + 1]) for i in range(4)],
            "optimizer" : parseOptimizer(dna[12])
        }
    }
    #temos 13 genes, os 4 primeiros servem para definir as caracteristicas do processo de treinamentos


def evaluateTest(testFunction):
    return testFunction()

def evaluateTrain(trainFunction):
    import timeit
    start_time = timeit.default_timer()
    results = trainFunction()
    end_time = timeit.default_timer()
    delta_time = end_time - start_time
    return results, delta_time

def main(dna: bytearray):
    logger = getLog()
    logger.debug(f"Parsing DNA: {dna}")
    hParams = parseDna(dna)
    
    logger.debug(f"Building neuralNetwork...")
    testFunction, trainFunction, model= paraneural.buildAll(hParams)
    
    logger.info("Evaluating this individual")
    trainRes = evaluateTrain(trainFunction)
    testRes = evaluateTest(testFunction)
    
    logger.info(f"Results:\n\t{trainRes, testRes}")
    return locals()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])