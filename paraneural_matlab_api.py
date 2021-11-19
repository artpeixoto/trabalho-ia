import paraneural
from timeit import timeit
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
    timer = timeit(number=1)
    timer.start()
    results = testFunction()
    timer.stop()
    return results

def main(dna: bytearray):
    logger = getLog()
    logger.debug(f"Parsing DNA: {dna}")
    hParams = parseDna(dna)
    
    logger.debug(f"Building neuralNetwork...")
    model, testFunction, trainResults = paraneural.buildNeuralNet(hParams)
    
    logger.debug(f"Gotten these results:\n\tmodel:{model}\n\ttrain results: {trainResults}")
    logger.info("Evaluating this individual")
    
    finalResults = evaluateTest(testFunction)
    logger.info(f"Results:\n\t{finalResults}")
    return locals()
