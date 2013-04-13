close all
clear all
filename = 'RSP-Zp4-Step.traj';

m = dlmread(filename, ',');
T = 0.005;
sdes=ceil(2.5/T);;

trange = 1:ceil(sdes);;

t = m(:,1);
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

title('Angle of Right Shoulder Pitch')
xlabel('Time (s)')
ylabel('Angle (rad)')
