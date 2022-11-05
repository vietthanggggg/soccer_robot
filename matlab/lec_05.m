%% Kinematic simulation of a land-base mobile robot
clear all ; clc; close all;

%% Simulation parameters
dt =0.1; % Step size
ts =10; % Simulation time
t = 0:dt:ts; % Time span

%% Intial Conditions
x0 =  0;
y0 = 0;
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
    u=0.1;% x-axis velocity with respect to B frame
    v=0.05;% y-axis velocity with respect to B frame
    r=0;% anglelar velocity with respect to B frame
    
    zeta(:,i) =[u;v;r];
    
    eta_dot(:,i) =J_psi* zeta(:,i);
    
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

figure
plot(t,eta(1,1:i),'r-');
hold on
plot(t,eta(2,1:i),'b--');
plot(t,eta(3,1:i),'m-.');
legend('x,[m]','y,[m]','\psi,[rad]');
set(gca,'fontsize',24)
xlabel('t,[s]');
ylabel('\eta,[units]');
