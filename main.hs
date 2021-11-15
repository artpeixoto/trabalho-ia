import qualified Data.Int as Int 
import qualified Data.Bits as Bits
import qualified Data.Map as Map
import qualified System.Random as Random
import Data.ByteString (ByteString)



let
    newtype Dna =   Dna [Gene]
    type Population = [Dna]
    type Mask = [MaskGene]
    type MaskGene = Bool
    type Probability = Float
    type Score = Float
    type MixDnaFunction = (Dna -> Dna -> Dna)

    testIndividual :: Dna -> Solution

    evaluateSolution :: Solution -> Score 

    selectIndividuals :: [Score] -> [[Int]]

    produceChildren :: [MixDnaFunction] -> [Dna] -> [Dna]

    crossover :: Mask -> MixDnaFunction
                            True ->  y

    makeMask :: Random.StdGen -> Probability -> Int ->  (Mask, Random.StdGen)
    makeMask gen _ 0 = ([], gen)
    makeMask gen x n = (newMaskGene:retMask, newGen) 
        where
            (retMask, retGen) = makeMask gen x (n-1)
            (val, newGen) = Random.uniform retGen :: (Float, Random.StdGen)
            newMaskGene = val < x
    
    crossover (m:ms) (x:xs) (y:ys) = (g) : (crossover  ms xs ys)
        where g = case m of False -> x




where --funcoes ajudantes
    (<|) = ($)
