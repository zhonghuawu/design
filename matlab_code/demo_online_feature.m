% n, d, k denote the sample size, sample dimension and subspace rank respectively.
n = 100;
d = 300;
alpha = 1;
k = 20;
ModelPara.alpha = alpha;
ModelPara.k = k;
MinCount =30;%默认直接选定前MinCount个特征
RetainCount= 25; %每次新的batch完成一次优化后，刷新下标集合，只保留RetainCount个特征
% ！参数设置时要保证 k小于等于MinCount和RetainCount，否则PCA无解(在k>d时，秩为d的矩阵W不可能带来W'W=I_k)

X = rand(n, d);
IndexSet = 1:MinCount;
addpath(genpath('../offline'));
MainData = X(:,IndexSet);
if ~isempty(MainData)
    W = sspca_offline(MainData, alpha, k);%求得MinCount个特征的最优
end
ObjValue=zeros(n,1);
ObjValue(MinCount) = norm(MainData*W*W' - MainData, 'fro')^2 + alpha*(sum(sqrt(sum(W.*W,2))));

for i = MinCount + 1 : n % 每个新的batch给1个样本
    NewBatch = X(:, i);
    fprintf('\nBatch %d:   ',i);
    [MainData, W] = sspca_online_feature(MainData, W, NewBatch, RetainCount, ModelPara);
    ObjValue(i) = norm(MainData*W*W' - MainData, 'fro')^2 + alpha*(sum(sqrt(sum(W.*W,2))));
end
