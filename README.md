# HwAwareProb
Repository for the paper "Towards Hardware-Aware Tractable Learning of Probabilistic Models", to be presented in NeurIPS 2019.

## Dependencies

* Python 2.7 (code soon to be updated for Python 3)

## Usage and options

The goal is to find the Pareto optimal set of configurations in the accuracy vs hardware-cost space by scaling tunable system properties. The properties to consider can be given as options as follows:

* -ms: Scale model complexity
* -csi: Scale sensor interfaces (prune features, sensors and simplify model)
* -ps: Scale precision
* -csi: Consider featuse and sensor cost

## Example

For the HAR benchmark, for which sensor and feature costs are available, following the full scaling pipeline (model complexity scaling - sensor interfaces scale - precision scale):

```
python hwopt.py HAR -models 10,22,38  -ms -ps -csi 
```

## Other

### Models
We have included the ACs used in our experiments, trained using the LearnPsdd algorithm introduced in <sup>[1](#myfootnote1)</sup>

### Datasets
For reproducibility, we have included the binarized and randomly split classification datasets used for the experiments: banknote<sup>[2](#myfootnote2)</sup>, HAR<sup>[3](#myfootnote3)</sup>, HAR_multiclass<sup>[3](#myfootnote3)</sup> ,houses<sup>[4](#myfootnote4)</sup> ,madelone <sup>[5](#myfootnote5)</sup> and wilt<sup>[6](#myfootnote6)</sup>. Density estimation datasets NLTCS and Jester were taken from https://github.com/UCLA-StarAI/Density-Estimation-Datasets, and introduced in<sup>[7](#myfootnote7)</sup>.

### References
<a name="myfootnote1">1</a>: Liang, Yitao, Jessa Bekker, and Guy Van den Broeck. "Learning the structure of probabilistic sentential decision diagrams." Proceedings of the 33rd Conference on Uncertainty in Artificial Intelligence (UAI). 2017.

<a name="myfootnote2">2</a>: Dua, D. and Graff, C. (2019). UCI Machine Learning Repository. Irvine, CA: University of California, School of Information and Computer Science. 

<a name="myfootnote3">3</a>: Davide Anguita, Alessandro Ghio, Luca Oneto, Xavier Parra and Jorge L. Reyes-Ortiz. A Public Domain Dataset for Human Activity Recognition Using Smartphones. 21th European Symposium on Artificial Neural Networks, Computational Intelligence and Machine Learning, ESANN 2013. Bruges, Belgium 24-26 April 2013. 

<a name="myfootnote4">4</a>: Pace, R. Kelley, and Ronald Barry. "Sparse spatial autoregressions." Statistics & Probability Letters 33.3 (1997): 291-297.

<a name="myfootnote5">5</a>: Isabelle Guyon, Steve R. Gunn, Asa Ben-Hur, Gideon Dror, 2004. Result analysis of the NIPS 2003 feature selection challenge. In: NIPS.

<a name="myfootnote6">6</a>: Johnson, B., Tateishi, R., Hoan, N., 2013. A hybrid pansharpening approach and multiscale object-based image analysis for mapping diseased pine and oak trees. International Journal of Remote Sensing, 34 (20), 6969-6982. 

<a name="myfootnote7">7</a>: Daniel Lowd, Jesse Davis: Learning Markov Network Structure with Decision Trees. ICDM 2010
