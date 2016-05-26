Models--
Model_001 : This model is supoed to get a clear view of the value regressor. There are 5 regressors: Value, Diff, and one for each sub-task.

Model_001v : Like model_002 except is has no difference regressors, just 3 task regressors and 1 value regresors. 

Model_001d : Like model_002 except is has no value regressors, just 3 task regressors and 1 difference regresors. 

Model_002 : This model is designed to compair the value regressor for each subtask. There are 9 regressors : value for each sub-task, diff for each subtask, and a task regressor for each task. 

Model_002v : Like model_002 except is has no difference regressors, just 3 task regressors and 3 value regresors. 

Model_002d : Like model_002 except is has no value regressors, just 3 task regressors and 3 difference regresors. 

Model_003 : This is like model 2 except is assumes that the tracked value should be the min(item1_value, item1_value, combined_option_value) that is still greater than the value of the fixed option. If none of those are greater than the fixed option, than the tracked value is the max(item1_value, item1_value, combined_option_value). Notice, that subjects are faster to pick the on screen item when it is avaialable for bundled options. 

Model_004 : If the value of either item that makes up a bundle is greater than the value of the fixxed option, they will only consider that item before making a choice. 

Model_005 : This model groups options in to low/medium/high value groups and uses each in a seperate GLM. This is a group only model. No parametrics. 

Model_006 : This model groups options by type and in to low/medium/high value groups and uses each in a seperate GLM. This is the same as model 5, but there is also parametric value. 

Model_007 : This model uses a different regressor for each item.

Model_008 : 3 regressors (task, value, and diff) for each of 5 subtasks (control, scaling(single_item_sufficient), scaling(other), bundling(single_item_sufficient), bundling(other))

Model_009 : This is like model 1 in that it only has one value and diff regressor for all trials together. It's like model 4 in that it uses the same value model (ie track the max of the two values of the single items that make up a bundle)

Model_009_v : like modle 9 but with no diff regressor (ie the only parametric regressor is Value)

PPI_001 : Connectivity models. There are three task regressors one for each subtask.

PPI_002 : Connectivity models. There are 5 task regressors. (1) control; (2) scaling options that only require a partial valuation; (3) scaling options that require a complete valuation; (4) Bundling options that only require a partial valuation; (5) Bundling options that requre a full valuation. This is based off of the same definitions as model_004


Flags--
_Chosen : Value of the chosen Option

_LBUB : These models use a MLE value estmate model that assumes the *Lower Bound* of value is -1 and *Upper Bound* is +1

_LB : These models use a MLE value estmate model that assumes the *Lower Bound* of value is 0

_MLERank : Rank by MLE value 

_S : These use a value MLE value model that is only bound by sum 

_Rank : These models use the rank as a proxy for value.

_Offset : These models set the vale of the control option to 0 so that options more valuable than the control item have positive value and options that are less valuable than the control item have negative value. 

_Split : These models have seperate regressors for [options with positive value] and [options with negative value].

_RT : There is a parametric regressor for reaction time.