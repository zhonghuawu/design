function zero_isnot_minimizer = gradient_validation(MainData, W, NewBatch, ModelPara)
% zero_isnot_minimizer = gradient_validation(MainData, W, NewBatch)
% ||X*W*W'-X||_F^2 + alpha*||W||_2,1
% This the speed of this function depends on the sample size, but not the dimension
    [t, k] = size(W);
    [n, t] = size(MainData);
    eps = 0.1;
    alpha = ModelPara.alpha;
    N = 100;% 0¸½½üµÄN¸öËæ»úµã
    point_set = eps*rand(k, N) - 0.5*eps; % Á¢·½ÌåËæ»ú²ÉÑù·¨£¬epsÎªÁ¢·½Ìå±ß³¤
    M = [MainData, NewBatch]'*[MainData, NewBatch];
    D_vector = 0.5./sqrt(sum(W.*W, 2));
% ÀûÓÃ¾ØÕó·ÖÁÑÊÖ¶Î£¬·ÖÀë³ö¼ÆËãÌÝ¶ÈÊ±µÄÖØ¸´²¿·Ö£º
% subgradient = 2*(alpha*D - X'X)W
%             = 2*alpha(D_old*W_old + D_old*W_incre + D_incre*W_old +
%             D_incre* W_incre) - 2*M*W_old - 2*M*W_incre
%             =  (2*alpha*D_old*W_old - 2*M*W_old) +  (ÌáÇ°¼ÆËã)
%             (2*alpha*D_incre*W_incre - 2*M*W_incre) (Ã¿´ÎÔÚÐÂµÄ²âÊÔµã¼ÆËã)
    W_old = [W;zeros(1, k)];
    D_old = diag([D_vector;0]);
    gradient_old = 2*alpha*D_old*W_old - 2*M*W_old;
    zero_isnot_minimizer = 0;
    k_count = 0;    

    for i=1:N %ÒÀ´Î²âÊÔN¸öµãµÄÌÝ¶ÈÊÇ·ñÂú×ãÒ»½×TaylorÔöÁ¿Ìõ¼þ
        W_come = point_set(:, i)';
        % W_incre = zeros(t+1, k); W_incre(t+1,:) = W_come
        % ¿ÉÑéÖ¤£¬M*W_increµÈ¼ÛÓÚM(:,t+1)*W_come£¬½øÒ»²½°Ñ3´Î¼ÆËã¸´ÔÓ¶È½µÎª2´Î
        gradient_incre = [zeros(t, k);alpha*W_come/norm(W_come, 2)] - 2*M(:,t+1)*W_come;
        subgradient = gradient_old + gradient_incre;
        
        % fÔÚ·Ç0´¦¿Éµ¼  ===>  f(0) = f(W_come) + gradient_f(W_come)*(-W_come) + O(...)
        % f(0)¾Ö²¿×îÐ¡ <===>  gradient_f(W_come)*(-W_come) <= 0
        if subgradient*point_set(:, i) < 0
	    zero_isnot_minimizer=1;
	    break
	    % k_count = k_count+1;
        end
    end
    fprintf('k_count = %d\n, n = %d, k = %d\n', k_count, n, k);
    if k_count>=k*n/40
	      zero_isnot_minimizer = 1;
    end
    if i<=N
        fprintf('pass the gradient validation in the point %d\n',i);
    else
        fprintf('did not pass the gradient validation\n');
    end
end
