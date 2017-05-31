function [MainData_new, W_new] = refresh_selected(MainData, W, RetainCount)
% [MainData, W] = refresh_selected(MainData, W)
% Retain the RetainCount indexes with the hightest row values. 
    RowScore = sum(W.*W, 2);
    [~, k] = size(W);
    [n, ~] = size(MainData);
    [~, dex] = sort(RowScore, 'descend');
    Length_new = min(length(dex), RetainCount);
    W_new = zeros(Length_new, k);
    MainData_new = zeros(n, Length_new);
    for i=1:Length_new
        W_new(i, :) = W(dex(i),:);
        MainData_new(:,i) = MainData(:,dex(i));
    end
end