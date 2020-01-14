# Plan

## Splitting workload
Making sure each member is contributing an even amount of both code and documentation
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

## Implementation specific problems
should determine how to create tokens, whether we should be allowing the creation of multiple tokens under the same user, etc.
should message_id be specific to each channel or be unique across the entire slackr?

## Useful software tools
Gitlab: staying organised and regularly pulling and pushing, appropriate usage of branches
Messenging: staying in contact with team members through group chats so everyone is up to date on the progress in the project
Skype: pair programming; 
Slack: to communicate with team members as well testing a reference implementation