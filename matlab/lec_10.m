%% Kinematic simulation of a land-base mobile robot
clear all ; clc; close all;

%% Simulation parameters
dt =0.1; % Step size
ts =100; % Simulation time
t = 0:dt:ts; % Time span

%% Vehicle (mobile robot) parameters (physical)
a= 0.2; % radius of the wheel (fixed)
d= 0.5; % distance between wheel frame to vehicle frame (along y-axis)

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
    omega_1 =0.5 %left wheel angular velocity
    omega_2 =0 %right wheel angular velocity
    
    omega=[omega_1;omega_2];
    
    %% Wheel configuration mattrix
    
    W=[a/2,a/2;
        0,0;
        -a/(2*d),a/(2*d)];   
    %velocity input commands
    zeta(:,i) =W*omega;

    
%     e(:,i)=eta_d -eta(:,i);

    
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
l=0.4; % length of the mobile robot
w=2*d; % width of the mobile robot
%Mobile robot coordinates
mr_co = [-l/2,l/2,l/2,-l/2,-l/2;
         -w/2,-w/2,w/2,w/2,-w/2;];
figure
for i = 1:5:length(t) % animation start here
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
    pause(0.01);
    hold off
end %animation end here

