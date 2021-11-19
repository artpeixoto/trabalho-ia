import paraneural
from timeit import Timer
import enum
import itertools as itert
#nesse modulo, testamos os algoritmos de paraneural, alterando o parametros das redes neurais. Os parametros sao codificados em genes e otimizados por algoritmos geneticos

def getLog():
    import logging
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    return logger

def parseDna(dna): #recebe uma lista de inteiros e transforma em genes que o modulo paraneural pode entender
    def parseTrainGenes(epochs, batchSize, use_multiprocessing, workers):
        return {
            "epochs" : epochs,
            "batch_size" : 2**batchSize,
            "use_multiprocessing" : use_multiprocessing != 0,
            "workers" : workers
        }
    def parseLayerGenes(units, activation):
        return (
            "Dense" #unica suportavel por enquanto
            ,
            {   "units" : units,
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
            })
    def parseOptimizer(optimizer):
        return [
                "adadelta",
                "adagrad",
                "adam",
                "adamax"
            ][optimizer]
    
    hParams = {
        "train": parseTrainGenes(*dna[0:4]),
        "model": {
            "layersArgs" : [parseLayerGenes(dna[4+ i*2], dna[4+ i*2 + 1]) for i in range(4)],
            "optimizer" : parseOptimizer(dna[12])
        }
    }
    return hParams


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
    logger.info(f"Parsing DNA: {dna}")
    hParams = parseDna(dna)
    logger.info(f"hyperparameters: {hParams}")
    logger.info(f"Building neuralNetwork...")
    testFunction, trainFunction, model = paraneural.buildAll(hParams)
    
    logger.info("Evaluating individual")
    trainRes = evaluateTrain(trainFunction)
    testRes = evaluateTest(testFunction)
    
    logger.info(f"Results:\n\t{trainRes, testRes}")
    return locals()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main([  0x0A, 0x05, 0x01, 0x08,
                0x40, 0x01,
                0x80, 0x01, 
                0x40, 0x02, 
                0x40, 0x02, 
                0x01])