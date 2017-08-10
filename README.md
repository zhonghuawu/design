<!--
## 0. Result figure on 8 datasets
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/all_8_datasets.png)

        note: sfs_l21(streaming feature selection regularized by l21-norm) is our algorithm

### datasets
        1        TOX_171
        2         GLIOMA
        3         ALLAML
        4          colon
        5     Prostat_GE
        6    Lung_Cancer
        7          SRBCT
        8          DLBCL

### 0.1 epsilon
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/epsilon/fig/accuracy_on_Prostate_GE.png)
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/epsilon/fig/accuracy_on_ALLAML.png)
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/epsilon/fig/accuracy_on_colon.png)
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/epsilon/fig/accuracy_on_SRBCT.png)
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/epsilon/fig/accuracy_on_DLBCL.png)

### 0.2 lambda
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/threshold/fig/accuracy_on_Prostate_GE.png)
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/threshold/fig/accuracy_on_ALLAML.png)
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/threshold/fig/accuracy_on_colon.png)
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/threshold/fig/accuracy_on_SRBCT.png)
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/threshold/fig/accuracy_on_DLBCL.png)
-->



## 1. Result figure on 12 datasets
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/all_final.png)

### datasets
        1         TOX_171
        2        lymphoma
        3     SMK_CAN_187
        4          GLIOMA
        5          ALLAML
        6          GLI_85
        7            lung
        8           colon
        9      Prostat_GE
        10     Lung_Cancer
        11          SRBCT
        12          DLBCL

### Result record on 12 datasets
* [dataset attribute](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/all_attribute.csv) <br>
* [Prediction accuracy](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/all_cls.csv) <br>
* [The number of selected features](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/all_nfs.csv)

## 2. parameter epsilon effect to algorithm
#### 2.1 on [Prostate\_GE](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/epsilon/opt_epsilon_on_Prostate_GE.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/epsilon/opt_epsilon_on_Prostate_GE.png)

#### 2.2 on [ALLAML](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/epsilon/opt_epsilon_on_ALLAML.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/epsilon/opt_epsilon_on_ALLAML.png)

#### 2.3 on [colon](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/epsilon/opt_epsilon_on_colon.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/epsilon/opt_epsilon_on_colon.png)

#### 2.4 on [lung](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/epsilon/opt_epsilon_on_lung.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/epsilon/opt_epsilon_on_lung.png)

#### 2.5 on [SRBCT](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/epsilon/opt_epsilon_on_SRBCT.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/epsilon/opt_epsilon_on_SRBCT.png)

#### 2.5 on [DLBCL](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/epsilon/opt_epsilon_on_DLBCL.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/epsilon/opt_epsilon_on_DLBCL.png)

## 3. parameter lambda effect to algorithm
#### 3.1 on [Prostate\_GE](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/threshold/opt_threshold_on_Prostate_GE.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/threshold/opt_threshold_on_Prostate_GE.png)

#### 3.2 on [ALLAML](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/threshold/opt_threshold_on_ALLAML.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/threshold/opt_threshold_on_ALLAML.png)

#### 3.3 on [colon](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/threshold/opt_threshold_on_colon.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/threshold/opt_threshold_on_colon.png)

#### 3.4 on [lung](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/threshold/opt_threshold_on_lung.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/threshold/opt_threshold_on_lung.png)

#### 3.5 on [SRBCT](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/threshold/opt_threshold_on_SRBCT.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/threshold/opt_threshold_on_SRBCT.png)

#### 3.6 on [DLBCL](https://github.com/zhonghuawu/design/blob/master/datas/gene/all_result/threshold/opt_threshold_on_DLBCL.csv) dataset
![image](https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/threshold/opt_threshold_on_DLBCL.png)

## 4. ![streaming](https://github.com/zhonghuawu/design/tree/master/datas/gene/all_result/streaming")
<!--
<center >
<img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/TOX_171.png" width='30%'> <img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/lymphoma.png" width='30%'> <img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/SMK_CAN_187.png" width='30%'>
<img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/GLIOMA.png" width='30%'> <img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/ALLAML.png" width='30%'> <img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/GLI_85.png" width='30%'> 
<img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/lung.png" width='30%'> <img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/colon.png" width='30%'> <img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/Prostate_GE.png" width='30%'>
<img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/Lung_Cancer.png" width='30%'> <img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/SRBCT.png" width='30%'> <img src="https://github.com/zhonghuawu/design/raw/master/datas/gene/all_result/streaming/DLBCL.png" width='30%'>
</center>
-->

