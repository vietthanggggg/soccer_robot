%% Kinematic simulation of a land-base mobile robot
clear all ; clc; close all;

%% Simulation parameters
dt =0.1; % Step size
ts =10; % Simulation time
t = 0:dt:ts; % Time span

%% Intial Conditions
x0 =  0.5;
y0 = 0.5;
psi0 = pi/4;

eta0 = [x0;y0;psi0];

eta(:,1) = eta0;


%% Loop starts here
for i = 1:length(t)
    psi = eta(3,i); %current orientation in rad.
    %Jacobian mattrix
    J_psi = [cos(psi) ,-sin(psi),0;
             sin(psi) , cos(psi),0;
             0,0,1];
    %% Input
%     u=0.1;% x-axis velocity with respect to B frame
%     v=0.05;% y-axis velocity with respect to B frame
%     r=0.05;% anglelar velocity with respect to B frame
    
%% Desired states(Generlized coordinates)
    eta_d = [2-2*cos(0.1*t(i));2*sin(0.1*t(i));0.1*t(i)];
    eta_d_dot=[2*0.1*sin(0.1*t(i));2*0.1*cos(0.1*t(i)); 0.1;];
    %% Vector of velocity input commands
    zeta(:,i) =inv(J_psi)* eta_d_dot;
    
    e(:,i)=eta_d -eta(:,i);
    %velocity input commands
%     zeta(:,i) =[u;v;r];
    
    %time derivatives of generalized coordinates
    eta_dot(:,i) =J_psi* zeta(:,i);
    
    %% Position propagation using Euler method
    eta(:,i+1)= eta(:,i) +dt* eta_dot(:,i); %Euler mothod
    
end

%% Plotting function
% figure
% plot(t, eta(1,1:i),'r-');
% set(gca,'fontsize',12)
% xlabel('t,[s]');
% ylabel('x,[m]');
% 
% figure
% plot(t, eta(2,1:i),'b-');
% set(gca,'fontsize',12)
% xlabel('t,[s]');
% ylabel('y,[m]');
% 
% figure
% plot(t, eta(3,1:i),'g-');
% set(gca,'fontsize',12)
% xlabel('t,[s]');
% ylabel('\psi,[rad]');

% figure
% plot(t,eta(1,1:i),'r-');
% hold on
% plot(t,eta(2,1:i),'b--');
% plot(t,eta(3,1:i),'m-.');
% legend('x,[m]','y,[m]','\psi,[rad]');
% set(gca,'fontsize',24)
% xlabel('t,[s]');
% ylabel('\eta,[units]');

%% Animation (mobile robot motion animation)
l=0.6; % length of the mobile robot
w=0.4; % width of the mobile robot
%Mobile robot coordinates
mr_co = [-l/2,l/2,l/2,-l/2,-l/2;
         -w/2,-w/2,w/2,w/2,-w/2;];
figure
for i = 1:length(t) % animation start here
    psi= eta(3,i);
    R_psi = [cos(psi), -sin(psi);
             sin(psi), cos(psi);];%rotation mattrix
    v_pos = R_psi*mr_co;
    fill(v_pos(1,:)+eta(1,i),v_pos(2,:)+eta(2,i),'g');
    hold on, grid on;
    axis([-1 3 -1 3]),axis square
    plot(eta(1,1:i),eta(2,1:i),'-b');
    legend('MR','Path');
    set(gca,'fontsize',24)
    xlabel('x,[m]'); ylabel('y,[m]');
    pause(0.1);
    hold off
end %animation end here

 figure
 plot(t, e);
 legend('x_e,[m]','y_e,[m]','\psi,[rad]');
 set(gca,'fontsize',24)
 xlabel('t,[s]');
 ylabel('\eta,[unit]');