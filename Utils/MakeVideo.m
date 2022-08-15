clc
clear

video = VideoWriter('TonyRoadVideo.avi'); %create the video object
open(video); %open the file for writing

for i = 0:419
    disp(i)
    try
        image_name = strcat('TonyRoadImages_VP/vp_img', num2str(i), '.jpg');
        I = imread(image_name); 
    catch
        image_name = strcat('TonyRoadImages/img', num2str(i+1), '.jpg');
        I = imread(image_name); 
    end
    writeVideo(video,I); 

end


close(video); %close the file