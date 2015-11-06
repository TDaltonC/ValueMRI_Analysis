Models--
Model_001 : This model is supoed to get a clear view of the value regressor. There are 5 regressors: Value, Diff, and one for each sub-task.

Model_002 : This model is designed to compair the value regressor for each subtask. There are 9 regressors : value for each sub-task, diff for each subtask, and a task regressor for each task. 

Model_003 : This is like model 2 except is assumes that the tracked value should be the min(item1_value, item1_value, combined_option_value) that is still greater than the value of the fixed option. If none of those are greater than the fixed option, than the tracked value is the max(item1_value, item1_value, combined_option_value). Notice, that subjects are faster to pick the on screen item when it is avaialable for bundled options. 

Model_004 : If the value of either item that makes up a bundle is greater than the value of the fixxed option, they will only consider that item before making a choice. 

Flags--
_LBUB : These models use a MLE value estmate model that assumes the *Lower Bound* of value is -1 and *Upper Bound* is +1

_LB : These models use a MLE value estmate model that assumes the *Lower Bound* of value is 0

_Rank : These models use the rank as a proxy for value.

_Offset : These models set the vale of the control option to 0 so that options more valuable than the control item have positive value and options that are less valuable than the control item have negative value. 

_Split : These models have seperate regressors for [options with positive value] and [options with negative value].