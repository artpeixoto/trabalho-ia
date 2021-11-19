%Implementação do SIAD-AG (Aplicação 2)
%Código MatLab:

clear all
close all
clc

%% Definindo o range das variáveis

epochs = [1 16]; 
batchSize = [1 10]; 
use_multiprocessing = [0 1];
workers = [1 8]; 

LB = [pA(1) pB(1) pC(1)]; %Limite inferior
UB = [pA(2) pB(2) pC(2)]; %Limite Superior

%% Configuração do Solver GA 

Numero_Variaveis = 3;
Tamanho_Populacao = 10;
Numero_Geracoes = 10;
Probabilidade_Crossover = 1.0;  % padrão = 0.8
Individuos_Elite = round(0.05*Tamanho_Populacao);  %elitismo
    
options = gaoptimset('UseParallel', true);
options = gaoptimset(options,'PopulationSize',Tamanho_Populacao);
options = gaoptimset(options,'PopInitRange', [LB;UB]);
options = gaoptimset(options,'Generations',Numero_Geracoes);
options = gaoptimset(options,'PopulationType','doubleVector'); %'bitstring' | 'custom' | {'doubleVector'}
options = gaoptimset(options,'CrossoverFraction',Probabilidade_Crossover);
options = gaoptimset(options,'EliteCount', Individuos_Elite);%0.05*ParamsGA.population_size
options = gaoptimset(options,'StallGenLimit',100);
options = gaoptimset(options,'Display', 'iter');%'off','iter','diagnose','fina'
options = gaoptimset(options,'PlotFcn',{@gaplotbestf,@gaplotstopping});

rng default
FuncaoFitness =@GAFuncObj02;
Matriz_A = [5 2 10; 2 5 3; 4 2 7];
Vetor_b = [900 500 700];

%% solver

%[x,fval,exitflag,output,population,scores]=ga(fun,nvars,A,b,Aeq,beq,lb,ub,nonlcon,IntCon,options)
 [x,fval,exitflag,output,population,scores]=ga(FuncaoFitness,Numero_Variaveis,Matriz_A,Vetor_b,[],[],LB,UB,[],[1,2],options)