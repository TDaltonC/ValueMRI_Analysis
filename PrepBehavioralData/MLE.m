function [ y_output,y_max,p_output,bestValue,bestLL] = MLEmain()
%you need to feed data as two-column vector called 'x'.
%this script will call on a log-likelihood fcn called 'MLEequation.m' that
%will report parameters as variable called 'p_fit'

subjIDs = [3301, 3303, 3304, 3306, 3308, 3309, 3310, 3312, 3313, 3314];
% subjIDs = [3306];
% dataDir = '/vol';
dataDir = '~/Documents/Projects/BundledOptionsExp/Analysis/Data';
% dataDir = '~/Documents/MATLAB/fMRI_fall2015/Dalton';

for subjCounter = 1:length(subjIDs)
    clearvars -except subjIDs dataDir subjCounter
    % Get to the subjects directory
    currentSubj = subjIDs(subjCounter);
    disp(currentSubj)
    cd(strcat(dataDir, '/RawData/SID', num2str(currentSubj), '/DataFrames'));
    % Import all of the choices
    trialByTrial = readtable(strcat('trialByTrial.csv'));
    ExplicitChoices = trialByTrial(trialByTrial.Choice>0,{'Opt1Code','Opt2Code','Choice'});
    choices = table2array(ExplicitChoices);
    
    
    % Import all of the options
    optionsDF = readtable(strcat('rank', num2str(currentSubj), '.csv'));
    
    %% NEW STUFF
    % count how many options there are
    allOptCount = height(optionsDF);
    
    % Omit those options that were never presented from variable "choices"
    allOptions = [1:allOptCount]; % create a vector of all possible options
    allOptions(2,:) = zeros;
    for j = 1:2 % check both the columns (option 1's and option 2's)
        for i = 1:length(allOptions)
            if(length(find(choices(:,j)==allOptions(1,i)))>0) % if option number is found in "choices"
                allOptions(2,i) = allOptions(2,i) + 1; % add 1 under that option number in "allOptions"
            else % otherwise
                allOptions(2,i) = allOptions(2,i) + 0; % add 0 under that option number
            end
        end
    end
    
    position = 1;
    for i = 1:length(allOptions)
        if allOptions(2,i) > 0  % if an option has been presented at least once
            allPresentedOptions(position) = i; % add that option to list "allPresentedOptions"
            position = position + 1;
        else
            position = position + 0;
        end
    end
    
    % count how many presented options there are
    optCount = length(allPresentedOptions);
    
    cat(1,choices(:,1),choices(:,2)); % create one column vector of all options (vertically concatonate option 1 and option 2 list)
    sortedOptions = sort(ans); % sort in ascending order
    
    j = 1; % loop through the "sortedOptions" list and rename them from 1:optCount so that MLE won't freak out
    for i = 1:length(sortedOptions)
        if i == 1
            sortedOptionsRenamed(j,1) = sortedOptions(1);
            sortedOptionsRenamed(j,2) = 1;
        else
            if sortedOptions(i,1) == sortedOptions(i-1,1)
                j = j + 0;
            elseif sortedOptions(i,1) ~= sortedOptions(i-1,1)
                j = j + 1;
                sortedOptionsRenamed(j,1) = sortedOptions(i);
                sortedOptionsRenamed(j,2) = j;
            end
        end
    end
    
    % replace option numbers as listed in "choices" with their new names as
    % listed in "sortedOptionsRenamed"
    for i = 1:length(choices)
        choices(i,1) = sortedOptionsRenamed((find(sortedOptionsRenamed(:,1)==choices(i,1))),2);
        choices(i,2) = sortedOptionsRenamed((find(sortedOptionsRenamed(:,1)==choices(i,2))),2);
    end
    
    
    %%
    x = zeros(length(choices),3);
    
    for m = 1:length(choices)
        x(m,1:2) = choices(m,1:2);
    end
    
    for m = 1:length(x)
        if choices(m,3) == 1
            x(m,3) = 1;
        elseif choices(m,3) == 2
            x(m,3) = 0;
        end
    end
    
    options = optimset('Algorithm','sqp');
    options.MaxFunEvals = 50000;
    
    %% MLE Models
    
    % Lower bound, upper bound, sum restriction
    limit_lower = -ones(1,optCount)*1000;
    limit_upper = ones(1,optCount)*1000;
    sumValuesMatrix = ones(1,optCount);
    sumValues = 0;
    
    p_initial(1:optCount,1) = linspace(1,-1,optCount); % initial values for all options
    [p_fitS,y_valS] = fmincon(@(p) MLEequation(p, x), p_initial,[],[],sumValuesMatrix,sumValues,limit_lower,limit_upper,[],options);
    %     p_outputS = join(p_fitS,sortedOptionsRenamed(:,1),'key','Key1','Type','outer',...
    %    'MergeKeys',true);
    p_fitS = cat(2,p_fitS,sortedOptionsRenamed(:,1)); % put option numbers in column to right of their values
    for i = 1:length(p_fitS)
        p_outputS(p_fitS(i,2),1) = p_fitS(i,1);
    end
    p_outputS = cat(1,p_outputS,zeros((allOptCount-length(p_outputS)),1));
    for j = 1:allOptCount
        if p_outputS(j,1)==0
            p_outputS(j,1) = str2num('NaN');
        else
            p_outputS(j,1) = p_outputS(j,1);
        end
    end
    y_outputS = y_valS;
    clear p
    
    % LB, UB, no sum restriction
    limit_lower = -ones(1,optCount);
    limit_upper =  ones(1,optCount);
    
    p_initial(1:optCount,1) = 0.1; % initial values for all options
    [p_fitLBUB, y_valLBUB] = fmincon(@(p) MLEequation(p, x), p_initial,[],[],[],[],limit_lower,limit_upper,[],options);
    %     p_outputLBUB = join(p_fitLBUB,sortedOptionsRenamed(:,1),'key','Key1','Type','outer',...
    %    'MergeKeys',true);
    p_fitLBUB = cat(2,p_fitLBUB,sortedOptionsRenamed(:,1)); % put option numbers in column to right of their values
    for i = 1:length(p_fitLBUB)
        p_outputLBUB(p_fitLBUB(i,2),1) = p_fitLBUB(i,1);
    end
    p_outputLBUB = cat(1,p_outputLBUB,zeros((allOptCount-length(p_outputLBUB)),1));
    for i = 1:allOptCount
        if p_outputLBUB(i,1)==0
            p_outputLBUB(i,1) = str2num('NaN');
        else
            p_outputLBUB(i,1) = p_outputLBUB(i,1);
        end
    end
    y_outputLBUB = y_valLBUB;
    clear p
    
    % LB, no UB, no sum restriction
    limit_lower = zeros(optCount,1);
    
    p_initial(1:optCount,1) = 0.01; % initial values for all options
    [p_fitLB,y_valLB] = fmincon(@(p) MLEequation(p, x), p_initial,[],[],[],[],limit_lower,[],[],options);
    %     p_outputLB = join(p_fitLB,sortedOptionsRenamed(:,1),'key','Key1','Type','outer',...
    %    'MergeKeys',true);
    p_fitLB = cat(2,p_fitLB,sortedOptionsRenamed(:,1)); % put option numbers in column to right of their values
    for i = 1:length(p_fitLB)
        p_outputLB(p_fitLB(i,2),1) = p_fitLB(i,1);
    end
    p_outputLB = cat(1,p_outputLB,zeros((allOptCount-length(p_outputLB)),1));
    for i = 1:allOptCount
        if p_outputLB(i,1)==0
            p_outputLB(i,1) = str2num('NaN');
        else
            p_outputLB(i,1) = p_outputLB(i,1);
        end
    end
    y_outputLB = y_valLB;
    clear p
    
    % no LB, UB, no sum restriction
    limit_upper = ones(1,optCount);
    
    p_initial(1:optCount,1) = 0.1; % initial values for all options
    [p_fitUB, y_valUB] = fmincon(@(p) MLEequation(p, x), p_initial,[],[],[],[],[],limit_upper,[],options);
    %     p_outputUB = join(p_fitUB,sortedOptionsRenamed(:,1),'key','Key1','Type','outer',...
    %    'MergeKeys',true);
    p_fitUB = cat(2,p_fitUB,sortedOptionsRenamed(:,1)); % put option numbers in column to right of their values
    for i = 1:length(p_fitUB)
        p_outputUB(p_fitUB(i,2),1) = p_fitUB(i,1);
    end
    p_outputUB = cat(1,p_outputUB,zeros((allOptCount-length(p_outputUB)),1));
    for i = 1:allOptCount
        if p_outputUB(i,1)==0
            p_outputUB(i,1) = str2num('NaN');
        else
            p_outputUB(i,1) = p_outputUB(i,1);
        end
    end
    y_outputUB = y_valUB;
    clear p
    
    %     %% Saving
    %     y_max = min(y_output);
    %     b = find(y_output == min(y_output));
    %     c = min(b);
    %     bestValue = p_output(c,:);
    %     bestLL = y_max;
    %
    %     resultsMLE.sub3301.y_output = y_output;
    %     resultsMLE.sub3301.y_max = y_max;
    %     resultsMLE.sub3301.p_output = p_output;
    %     resultsMLE.sub3301.bestValue = bestValue;
    %     resultsMLE.sub3301.bestLL = bestLL;
    %
    %     save('resultsMLE.mat','resultsMLE');
    
    optionsDF.MLEValueS = p_outputS;
    optionsDF.MLEValueLBUB = p_outputLBUB;
    optionsDF.MLEValueLB = p_outputLB;
    optionsDF.MLEValueUB = p_outputUB;  
    
    writetable(optionsDF, 'optionValue.csv')
    
    
    % %% Check that values make sense
    %
    % optionlist.sub3301 = zeros(optCount,3);
    %
    % for i = 1:length(optionlist.sub3301)
    %     optionlist.sub3301(i,1) = i;
    % end
    %
    %  for i = 1:length(choices.sub3301)
    %      if choices.sub3301(i,3) == 1
    %          optionlist.sub3301(find(optionlist.sub3301(:,1) == choices.sub3301(i,1)),2) = optionlist.sub3301(find(optionlist.sub3301(:,1) == choices.sub3301(i,1)),2) + 1;
    %          optionlist.sub3301(find(optionlist.sub3301(:,1) == choices.sub3301(i,2)),3) = optionlist.sub3301(find(optionlist.sub3301(:,1) == choices.sub3301(i,2)),3) + 1;
    %      elseif choices.sub3301(i,3) == 2
    %          optionlist.sub3301(find(optionlist.sub3301(:,1) == choices.sub3301(i,1)),3) = optionlist.sub3301(find(optionlist.sub3301(:,1) == choices.sub3301(i,1)),3) + 1;
    %          optionlist.sub3301(find(optionlist.sub3301(:,1) == choices.sub3301(i,2)),2) = optionlist.sub3301(find(optionlist.sub3301(:,1) == choices.sub3301(i,2)),2) + 1;
    %     end
    %  end
    %
    % save('optionlist.mat','optionlist');
end
end

function y = MLEequation(p, x)

numberObs = length(x);
itemL = x(:,1); % item1, LEFT side of screen
itemR = x(:,2); % item2, RIGHT side of screen

probFcn = zeros(numberObs,1);

% We multiply the PDF of the logit model (here, "probFcn") by -1 because
% fmincon minimizes instead of maximizing. By minimizing the negative of
% the PDF we are essentially maximizing
for n = 1:numberObs
    probFcn(n) = (-1)*(...
        (x(n,3))*(log(1/(1 + exp(-p(itemL(n)) +p(itemR(n)))))) + ...
        (1-x(n,3))*(log(1 - (1/(1 + exp(-p(itemL(n)) +p(itemR(n)))))))...
        );
end

y = sum(probFcn(1:numberObs));

end


