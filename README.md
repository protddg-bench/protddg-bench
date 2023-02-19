## Benchmarking resource for predictors of protein stability change.

INTRODUCTION

      Emidio Capriotti, Ludovica Montanucci and Piero Fariselli, 2023.
      Scripts are licensed under the Creative Commons by NC-SA license.

      ProtDDG-Bench is a benchmarking resource for predictors of protein stability change. 


DATASETS

      All the datasets for testing the performance of the predictors of DDG upon mutation are available at
      the protddg-bench repository. The protddg-bench repository includes the following datasets:

      1. VB1432:    1432 variants from 79 protein structures corresponding to 65 clusters.
                    9 mutations have double experimental data. 1 mutation is not mapping 
                    to the strcuture. The 1LRP structure was replace with 1LMB. For structure 1WQ5
                    was considered the chain B. Data from PMID:29597263.
      2. S2648:     2648 variants from 132 protein strcutures corresponding to 113 clusters.
                    Experimental DDGs of the same variants are avereged. Data from PMID:21569468.
      3. Ssym:      634 variants from 357 structures corresponding to 13 clusters.
                    Dataset composed by 342 mutations and their reverse. Data from PMID:29718106.
      5. Broom:     Dataset composed by 605 mutations from 58 structures corresponding to 50 clusters.
                    This dataset contains 53 mutations from non-native proteins and 59 mutations
                    referring to fragment of the protein. Experimental data are duplicated and 
                    triplicated in 17 and 1 cases. Data from PMID:28710274.

      4. Myoglobin: 134 variants from myoglobin from structure 1BZ6. Experimental data are 
                    duplicated and triplicated in 14 and 3 cases respectively. The variation of                    
                    unfolding free energy (DDG) was calculated changing the sign of the DDG
                    reported in literarture. Data from PMID:26054434
                    
      5. P53:       42 variants from P53 structure 2OCJ. Data from PMID:24281696.

      6. PTMUL:     914 multiple site variants from 91 protein structures and 77 clusters.
                    PMID:31266447.
      7. KORPM:     2,371 mutations from 129 protein famileis with sequence identity <25%.  
                    PMID:36629451.


     - The directory S2648 and VB1432 contains 10 files for 10-folds cross-validation tests.
       Furthermore, the cross-validation subset of S2648 and VB1432 are consistent. This means that 
       the following predictions can be performed:

         Training: not SET_i vb1432-10fold-split-j.tsv -> Test: SET_i s2648-10fold-split-j.tsv
         Training: not SET_i s2648-10fold-split-j.tsv  -> Test: SET_i vb1432-10fold-split-j.tsv


     - The directory BROOM contains a 5-fold split of the BROOM dataset. Given the number of mutations
       mutations form the same cluster the set has been diveded in 5 subsets. 
       The test on this dataset can be performed as follow:

         Training: not SET_i train-vb1432-test-broom.tsv -> Test: SET_i broom-5fold.tsv
         Training: not SET_i train-s2648-test-broom.tsv  -> Test: SET_i broom-5fold.tsv


     - The directory SSYM contains a 5-fold split of the Ssym dataset. Given the large number of
       mutations form the same cluster the set has been diveded in 5 subsets. 
       The test on this dataset can be performed as follow:

         Training: not SET_i train-vb1432-test-ssym.tsv -> Test: SET_i ssym-5fold.tsv
         Training: not SET_i train-s2648-test-ssym.tsv  -> Test: SET_i ssym-5fold.tsv


     - The directory MYOGLOBIN test contains the testing dataset myoglogin.tsv with the 
       best subsets of VB1432 and S2648 to be used as possible training.
       The following prediction can be performed:

         Training: train-vb1432-test-myoglobin.tsv (1399) -> Test: myoglobin.tsv
         Training: train-s2648-test-myoglobin.tsv  (2607) -> Test: myoglobin.tsv


     - The directory P53 test contains the testing dataset p53.tsv with the best subsets 
       of VB1432 and S2648 to be used as possible training. 
       The following prediction can be performed:

         Training: train-vb1432-test-p53.tsv       (1427) -> Test: p53.tsv
         Training: train-s2648-test-p53.tsv        (2643) -> Test: p53.tsv


     - The directory PTMUL contains files for testing predictions on multiple site mutations starting from  
       a training on a set single point mutations.
       The directory also includes a 5-fold split of the PTMUL dataset. Given the number of mutations
       mutations form the same cluster the set has been diveded in 5 subsets.
       The test on this dataset can be performed as follow:

         Training: not SET_i train-vb1432-test-ptmul.tsv -> Test: SET_i ptmul-5fold.tsv
         Training: not SET_i train-s2648-test-ptmul.tsv  -> Test: SET_i ptmul-5fold.tsv


     - The directory KORPM contains 10 files for 10-folds cross-validation tests. 
       Furtermore it contains 2 training and 2 testing files. The testing file are 
       Ssym and S461.
       The tests on this dataset can be performed as follow:

	 Training: not SET_i korpm-10fold-split-j.tsv -> Test: SET_i korpm-10fold-split-j.tsv
         Training: not Ssym  train-korpm-nossym.tsv  (1,807) -> Test: ssym-korpm.tsv
         Training: not S461  train-korpm-nos461.tsv  (2,224) -> Test: s461-korpm.tsv


CLUSTERING

     The file data/cluster-545-pdbchains.txt contains 132 clusters of 545 PDB chains. 
     The clustering is obtained using blastclust with the options -S 25 -L 0.5 -b F.
     
     On the korpm dataset proteins are clustered in 129 groups using MMseq with 25% 
     sequence identity cutoff of

TESTING

     To test your method you need to:
        1. replace the file scripts/predict-ddg-value.py with your own script that runs taking 
           in input only the testing and training files and returning in standard output 
           the experimental and the predicted ddgs respectively
           The program runs as follows:
                ./predict-ddg-value.py test_file.txt train_file.txt

        2. Generate an inputfile containing a two columns representing the PDB chain 
           identifier and the mutation followed by all the inputfeatures.
           The full list of mutations are reported in the file data/unique-mutations-input.txt
           and example of input file with two input features is data/ifeatures-KYTJ820101-BASU050101.txt.
     
     Finally run ./test.py input_feature_file.txt to score the performace of your method.
     For example runs:
           ./test.py data/ifeatures-KYTJ820101-BASU050101.txt


