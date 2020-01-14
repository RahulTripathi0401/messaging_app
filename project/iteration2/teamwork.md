# Team Meetings

Throughout iteration 2, the group met up if necessary as it was deemed more productive to implement the functions individually, asking for help when faced with a challenge. As the problems faced were more technical, we could just easily message each other or google a solution rather than a long coding sprint. Another consideration that was taken into account for team meetings was everyone’s increased workload due to mid-term exams, making impractical to meet frequently. However, our lack of meetings was substituted with great and cohesive team meetings.

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

# Managing Workflow
1. To organise our workload we used the issues board on gitlab to separate the functions which we had not been completed to the completed functions. This enabled the team to have updated progress on what each member had completed.

    ![functionsboard](https://gitlab.cse.unsw.edu.au/COMP1531/19T3/T15A-PyCharmers/raw/master/functionsboard.png)
    ![functionsboardfinished](https://gitlab.cse.unsw.edu.au/COMP1531/19T3/T15A-PyCharmers/raw/master/functionsboardfinished.png)

2. Another method we used to help manage workflow was pair coding. Developing the message functions heavily revolved around this idea as it was a more efficient process. We were able to bounce ideas off each other, helping resolving problems in a shorter time.

    ![flowchart](https://gitlab.cse.unsw.edu.au/COMP1531/19T3/T15A-PyCharmers/raw/master/flowchart.png)

3. Another consideration when creating our functions was the order in which we did it. There was no point creating a message function before a channel or auth functions as there would be no way to test it. We generally followed the flow chart creating our message and channel functions first, then implementing functions with dependencies.

# Agile Practices

![agileflow](https://gitlab.cse.unsw.edu.au/COMP1531/19T3/T15A-PyCharmers/raw/master/agileflow.png)

1. **User Stories driving implementation.**  
Development is driven for the stakeholder, and the stakeholders need. Thus it was imperative to reflect back on the requirements of the stakeholders when implementing our functions. This helped our teamwork as it gave us a common goal to try and fulfil, therefore everyone was on the same page. 

2. **Pair Programming.**  
Allows to bounce ideas off each other, resolving problems in a fast and effective manner, thus helping our teamwork.

3. **Test-Driven Programming.**  
Any session starts with writing programming adaptive tests and they are preceded by unit tests. Then the code specific to the user stories are written. This helped our teamwork as we were given a specific test/goal to fulfil making implementation more clear between members when solving issues.

4. **Face-to-face conversation.**  
The most efficient and effective method of conveying information to and within a development team This helped our teamwork as ideas could be discussed more clearly and communication was a lot easier.

5. **Keep It Simple.**  
Cutting functionality that does not lend value. This helped when looking over each others code. As well, this helped the efficiency of our algorithms as clutter was removed.