%close all
%clear all
%filename = 'RSP-Zp4-Step-Filter-Real.traj';
%filename = 'RSP-Zp4-Step-Filter-Enc-Real.traj';
filename = 'RSP-Zp4-Step-NoFilter-NewSim.traj';
%filename = 'RSP-Zp4-Step-Step-Real.traj';
%filename = 'RSP-Zp4-Step-Filter-Enc-Mass-Real.traj';

m = dlmread(filename, ',');
T = 0.005;
tend = 3;

sdes=ceil(2.5/T);

%trange = 1:ceil(sdes);

t = m(:,1);
finalV = 0;
for i = 1:length(t)
    if t(i) > tend
       finalV = i;
       break;
    end
end

trange = 1:finalV;

t = t - t(1);
t = t(trange);


rref = m(:,2);
rref = rref(trange);

sref = m(:,3);
sref = sref(trange);

spos = m(:,4);
spos = spos(trange);

hold on
%subplot(2,1,1);
plot(t,rref,'r')
hold on
plot(t,sref,'g')
plot(t,spos,'b')

legend('Reference','Commanded Reference','Actual Position')
ylabel('Angle (rad)','FontSize', 12)

%title({'Angle of Right Shoulder Pitch';'Step Response with Compliance Amplification'},'FontSize', 17)
%title({'Angle of Right Shoulder Pitch';'Step Response with Reference Filtering'},'FontSize', 17)
title({'Angle of Right Shoulder Pitch';'Step Response - Simulator'},'FontSize', 17)
axis([0 tend*1.02 -0.02 0.42])
grid on

%tn = t(2:length(t));
%subplot(2,1,2);plot(tn,diff(rref),'r')
%hold on
%plot(tn,diff(sref),'g')
%plot(tn,diff(spos),'b')




xlabel('Time (s)','FontSize', 12)

