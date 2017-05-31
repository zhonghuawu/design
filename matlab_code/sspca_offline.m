function W = sspca_offline(X, alpha, k)
% WStar = sspca_offline(X, alpha, k)
% WStar = argmin_W ||XWW' - X||_F^2 + alpha*||W||_2,1
%         s.t.  W'W = I_k
% [n, d] = size (X), data matrix
% [d, k] = size (W), weight matrix
    [n, d] = size (X);
    if k>d
        fprintf('k can not be greater than d.\n');
        return;
    end
    M = X'*X;
    W = eye(d);
    W = W(:, 1:k);
    MaxIter = 1000;
    ObjValue = zeros(MaxIter, 1);
    RelativeError = 0.0001;
    for i=1:MaxIter
        ObjValue(i) = norm(X*W*W' - X, 'fro')^2 + alpha*(sum(sqrt(sum(W.*W,2))));
        fprintf('Step %d,  Check object value: %f\n',i, ObjValue(i));
        if i>=2 && abs(ObjValue(i-1) - ObjValue(i))/ObjValue(i-1) < RelativeError
            fprintf('Finished in %d steps\n', i);
            break;
        end
        D = diag(0.5./(sqrt(sum(W.*W, 2))+0.001));
        [U, ~] = eig(M - alpha*D);%取X'X-lambda*D的前k个主特征向量
        W = U(:,d-k+1:d);
    end
    
    if i>MaxIter
        sprintf('Finished after maximum iterations.\n');
    end
end
