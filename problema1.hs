import Infrastructure
import Moo
import Data.Array.Accelerate
import qualified Data.ByteString as Bs



-- comecamos com a aplicacao 1
-- 1) 
-- temos 3 variaveis, que sao o numero de unidades de cada placa. No entanto, existe uma restricao ligando-as, que é o número de horas maximas de operacoes. 
-- Poderiamos escolher dentre 2 opcoes:
-- -- implementar o AG com essas 3 variaveis (numero de placa a, numero de placa b e numeros de placa c) e punir os individuos que ultrapassarem as restrições de forma agressiva, ou
-- -- implementar o AG com duas variáveis paramétricas, como as proporcoes entre as placas A e B e entre as placas A e C. Isso agilizaria a busca por soluções, mas poderia causar problemas matematicos, uma vez que estariamos, em essencia, utilizando o vetor (1, B/A, C/A) como parametro, e A, nesse caso nao poderia ser nulo, ou os outros parametros tenderiam a explosao.
-- Afim de evitar o surgimento de problemas numa etapa mais avancada do desenvolvimento, escolhe-se o uso das 3 variaveis mesmo, mas isso leva a necessidade de uma funcao objetivo adequa

data Fenotipo = Fen { pA :: Int
                    , pB :: Int
                    , pC :: Int 
                    } 
                    deriving (Eq, Show, Read)

Gene2Bs gene = Bs.packChars $ show gene
Bs2Gene bs = read bs

makeFenotipo :: [Gene] -> Fenotipo
makeFenotipo (pa:pb:pc:[]) = Fen pa pb pc

dna2Fen :: Dna -> Fenotipo
dna2Fen dna = makeFenotipo . map Bs2Gene $ dna



evaluateIndividual 

hourMatrix = Matrix []