module Infrastructure (
    Gene, Dna, Population, Mask, MaskGene, Score, 
    selectIndividuals, crossover, makeMask,  
) where

import qualified Data.Int as Int 
import qualified Data.Bits as Bits
import qualified Data.Map as Map
import qualified Data.IntMap as IMap
import qualified System.Random as Random
import qualified Data.ByteString as BS

type Gene = BS.ByteString
type Dna =   [Gene]
type Population = [Dna]
type Mask = [MaskGene]
type MaskGene = Bool
type Score = Int


selectIndividuals :: Random.StdGen -> IMap.IntMap (Dna, Score) -> (,) Population Random.StdGen
selectIndividuals gen perfMap = (individuals, last generators)
    where
        (individuals, generators) = unzip (scanl accFunc (selFunc gen) [1..])
        (dnas, scores) = getCols perfMap
        selFunc = \gen' -> (
            let (i, nextGen) = (selectWeighted gen' scores) 
            in  (dnas !! i, nextGen)
            )
        accFunc (aInd, aGen) = \_ -> selFunc aGen 


--TODO: defactor crossover and makeMask to a common controller
crossover :: Mask -> [Dna] -> [Dna] -> [Dna]
crossover (m:ms) (x:xs) (y:ys) = (g) : (crossover  ms xs ys)
    where g = case m of False -> x
                        True ->  y

makeMask :: Random.StdGen -> Float -> Int ->  (Mask, Random.StdGen)
makeMask gen _ 0 = ([], gen)
makeMask gen x n = (newMaskGene:retMask, newGen) 
    where
        (retMask, retGen) = makeMask gen x (n-1)
        (val, newGen) = Random.random retGen :: (Float, Random.StdGen)
        newMaskGene = val < x
        
-- funcoes ajudantes --
(<|) = ($)

getCols = \someMap -> (unzip . snd . unzip . IMap.toList $ someMap)

selectR  v (x:xs) = 
    let inRange v xl xh = (v >= xl) && (v < xh)
        isInRange = inRange v x (head xs)
    in if isInRange then 0
                    else (selectR v xs) + 1
selectR' v l = 
    let index =  (`subtract` 1) . length . fst . break (v >) $ l 
    in  index

compositeSum = \list -> scanl (\acc x -> acc + x) 0 list

selectWeighted :: Random.StdGen -> [Score] -> (Int, Random.StdGen)
selectWeighted gen scores = (selectedIndex, newGen)
    where   compositeScore = compositeSum scores
            (randVal, newGen) = Random.randomR (0, (last compositeScore) :: Int) gen
            selectedIndex = selectR' randVal compositeScore

