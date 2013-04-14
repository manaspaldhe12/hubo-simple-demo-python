close all
clear all
filename = 'RSP-Zp4-Step-Filter-Real.traj';
%filename = 'RSP-Zp4-Step-Step-Real.traj';

m = dlmread(filename, ',');
T = 0.005;
tend = 2.5;

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
plot(t,rref,'r')
plot(t,sref,'g')
plot(t,spos,'b')

legend('Reference','Commanded Reference','Actual Position')

title('Step Response: Angle of Right Shoulder Pitch','FontSize', 25)
xlabel('Time (s)','FontSize', 15)
ylabel('Angle (rad)','FontSize', 15)
