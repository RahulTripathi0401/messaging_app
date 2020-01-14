# Plan

## Splitting workload
Making sure each member is contributing an even amount of both code and documentation, this is about 8 functions each.
|Function Name|Person in-charge|
|-------------|----------------|
|auth/login|James|
|auth/logout|James|
|auth/register|James|
|auth/passwordreset/request|James|
|auth/passwordreset/reset|James|
|channel/invite|Rahul|
|channel/details|Alper|
|channel/messages|Laura|
|channel/leave|Laura|
|channel/join|Laura|
|channel/addowner|Alper|
|channel/removeowner|Alper|
|channels/list|James|
|channels/listall|James|
|channels/create|James|
|message/sendlater|Rahul|
|message/send|Laura|
|message/remove|Rahul|
|message/edit|Rahul|
|message/react|Rahul|
|message/unreact|Rahul|
|message/pin|Rahul|
|message/unpin|Rahul|
|user/profile|Alper|
|user/profile/setname|Alper|
|user/profile/setemail|Alper|
|user/profile/sethandle|Alper|
|user/profiles/uploadphoto|Alper|
|standup/start|Laura|
|standup/send|Laura|
|search|Laura|
|admin/userpermission/change|Laura|

### Pair programming
Split the workload in half and have two people work on a group of functions together to reduce errors and increase efficiency

## Preparing for deadline - managing time
Organising set group meeting to make sure each member is on task
### Taskboard
Using the issues section on gitlab we can plan and visualise what needs to be done
    Can be used to relate each user story to specific functions
### Running sprints
Team set deadlines, setting goals to meet before a given time
    e.g. Between weeks 3 and 5 aiming to finish a basic implementation of all the functions so on the last week of the iteration other team members can go over each others work - peer checking

## Order to approach the functions
Prioritising functions based on their dependencies
    e.g. auth_register should be the first implemented function so we have a way of creating a token to pass into other functions
Using the stakeholder video in deciding prioritisation of functions 

![flowchart](https://gitlab.cse.unsw.edu.au/COMP1531/19T3/T15A-PyCharmers/raw/master/flowchart.png)

example of how the dependencies of functions interact and how we should approach the iteration

very basic outline would be auth->channel->message->(user_profile|standup|admin|search)
