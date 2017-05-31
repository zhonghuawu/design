function [MainData_new, W_new, objVal] = sspca_online_feature(MainData, W, NewBatch, RetainCount, ModelPara)

 if gradient_validation(MainData, W, NewBatch, ModelPara) %ֱ����֤���0�Ƿ���local minimizer
     fprintf('Begin offline optimization:\n');
     MainData = [MainData, NewBatch];
     
     % ���⵱ǰ��ѡ���������Ž⣬�ɵȼ�ת��Ϊ���߰汾����
     W = sspca_offline(MainData, ModelPara.alpha, ModelPara.k);
     
     % �����������Ž�W��������������ֻ����ǰRetainCount��
     [MainData_new, W_new] = refresh_selected(MainData, W, RetainCount);
 else
     % ֱ������������
     MainData_new = MainData;
     W_new = W;
 end
 
end
