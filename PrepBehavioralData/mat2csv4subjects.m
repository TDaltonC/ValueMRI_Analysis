subjIDs = [3301, 3303, 3304, 3306, 3308, 3309, 3310, 3312, 3313, 3314, 3316, 3318, 3319, 3320, 3321, 3325, 3326, 3328, 3329, 3330, 3331, 3332, 3333, 3334, 3335, 3336];
% subjIDs = [9998, 9999];

for subjCounter = 1:length(subjIDs)
    % Get to the subjects directory
    currentSubj = subjIDs(subjCounter);
    disp(currentSubj)
    cd(strcat('/Users/Dalton/Documents/Projects/BundledOptionsExp/Analysis/Data/RawData/SID', num2str(currentSubj), '/MatLABOutput'));
    
%     copy the blank CSV 'blankOutput.csv' and save it as the header file for the matlab output.
    copyfile('blankOutput.csv','dataFromMatLAB.csv')
    % get a list of all of the .mat files in this folder
    matfiles = dir(strcat(num2str(currentSubj),'*.mat'));
    disp(matfiles)
    for recordNum = 1:length(matfiles)
        clearvars -except currentSubj matfiles recordNum SubjCounter subjIDs
        record = matfiles(recordNum).name;
        if strcmp(record, '*global*')
            break
        end
        load(record)
        if strcmp(settings.task, 'OnScreenOffScreen') % for the scanner task
    %       When a run ends in a fixation trial, some of the records come up
    %       short. To acomidate this we will need to add a null to the end of
    %       the trial. The 'secs' vector will always be the right length. So
    %       we'll correct everything to that.
    %       if behaviral.key is short, add a space to the end
            if max(size(behavioral.secs)) == max(size(behavioral.key))
                keys = behavioral.key;
            else
                keys = strvcat(behavioral.key, ' ');
            end
    %       if bahvioral.choice is short, add a space to the end
            if max(size(behavioral.secs)) == max(size(behavioral.choice))
                choices = behavioral.choice;
            else
                choices = strvcat(behavioral.choice, ' ');
            end
    %       Get the items from settings.orderedOptions, use
    %       settings.indexes to figureout which ones you should get
            clear n
            n=1;
            for grandTrialNum = settings.indexes{settings.run}(1):settings.indexes{settings.run}(2)
                disp(grandTrialNum)
                opt1Itm1(n) = settings.orderedOptions{grandTrialNum}(1);
                opt1Itm2(n) = settings.orderedOptions{grandTrialNum}(2);
                n = n+1;
            end
            
    %       convert behavior.keys to a choices number code
            for key = 1:length(keys)
                if keys(key) == '1'
                    finalKeys(key) = 1;
                elseif keys(key) == '3'
                    finalKeys(key) = 2;
                else
                    finalKeys(key) = -1;
                end
            end

    %       convert behavior.choice to a choices number code
            for choice = 1:length(choices)
                if choices(choice) == 'n'
                    finalChoices(choice) = 0;
                elseif choices(choice) == 's'
                    finalChoices(choice) = 1;
                elseif choices(choice) == 'o'
                    finalChoices(choice) = 2;    
                else choices(choice) == ' '
                    finalChoices(choice) = -1;
                end
            end
    %       make an array the length of behaviral.secs out of currentSubj
            SubjID_col = zeros(max(size(behavioral.secs)),1) + currentSubj;
            opt1Code_col = zeros(max(size(behavioral.secs)),1); % This is filled in by python (finishingTouchesOnMatlabData.py)
            opt2Code_col = zeros(max(size(behavioral.secs)),1); % This is filled in by python (finishingTouchesOnMatlabData.py)
            opt1Item1_col = opt1Itm1';
            opt1Item2_col = opt1Itm2';
            opt2Item1_col = zeros(max(size(behavioral.secs)),1) + settings.fixedOpt;
            opt2Item2_col = zeros(max(size(behavioral.secs)),1);
            onsetTime_col = settings.FlipTimestamp';
            run_col = zeros(max(size(behavioral.secs)),1) + settings.run;
            reactionTime_col = behavioral.secs';
            button_col = finalKeys';
            choice_col = finalChoices';
            

        elseif strcmp(settings.task, 'LeftRight') % for the post-scanner task
            
            
%           Encode the choices
            choices = behavioral.key;
            switchLR = settings.switchLR;
            for choice = 1:length(choices)
                if choices(choice) == 'f'
                    if switchLR(choice) == 0
                        finalChoices(choice) = 1;
                    elseif switchLR(choice) == 1
                        finalChoices(choice) = 2;
                    end
                    
                elseif choices(choice) == 'j'
                    if switchLR(choice) == 0
                        finalChoices(choice) = 2;
                    elseif switchLR(choice) == 1
                        finalChoices(choice) = 1;
                    end   
                else
                    finalChoices(choice) = -1;
                end
            end
            
% %         Get the itmes
            for trialNum = 1:length(behavioral.secs)
                task = settings.taskAll(trialNum);
%           Option1
                opt1Item1(trialNum) = settings.taskAll{1, trialNum}{1, 1}{1}(1);
                try
                    opt1Item2(trialNum) = settings.taskAll{1, trialNum}{1, 1}{1}(2);
                catch
                    opt1Item2(trialNum) = 0;
                end
%           Option2
                opt2Item1(trialNum) = settings.taskAll{1, trialNum}{1, 1}{1, 2}{1,1}(1);
                try
                    opt2Item2(trialNum) = settings.taskAll{1, trialNum}{1, 1}{1, 2}{1,1}(2);
                catch
                    opt2Item2(trialNum) = 0;
                end
            end
                    
            
            SubjID_col =       zeros(max(size(behavioral.secs)),1) + currentSubj;
            opt1Code_col =     zeros(max(size(behavioral.secs)),1);
            opt2Code_col =     zeros(max(size(behavioral.secs)),1);
            opt1Item1_col =    opt1Item1';
            opt1Item2_col =    opt1Item2';
            opt2Item1_col =    opt2Item1';
            opt2Item2_col =    opt2Item2';
            onsetTime_col =    zeros(max(size(behavioral.secs)),1);
            run_col =          zeros(max(size(behavioral.secs)),1);
            reactionTime_col = behavioral.secs;
            button_col =       zeros(max(size(behavioral.secs)),1);
            choice_col =       finalChoices';
        end
%       convert behavior.choice to a choices number code

%       make an array the length of behaviral.secs out of currentSubj

%       Now that everyhting is a number, slam it all on to one matrix 
        Matrix = [SubjID_col, opt1Code_col, opt2Code_col, opt1Item1_col, opt1Item2_col, opt2Item1_col, opt2Item2_col, onsetTime_col, run_col, reactionTime_col, button_col, choice_col];


%       append the matrix to the end of the csv
        
        dlmwrite('dataFromMatLAB.csv', Matrix, '-append');
        disp(record)
    end
    
    
end

% For each subject, 
% navigate to thier matlab folder,
% get a list of all of the .mat files in this folder
% write the titles of the columns to a csv
% For each .mat file found
%     load the .mat files 
%     write each coumn to the csv, one at a time with dlmwrite
