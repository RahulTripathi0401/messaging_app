_Provide assurances that your backend implementation is fit for purpose. Consider both verification and validation when doing this. This will, at a minimum, require acceptance criteria for your user stories.  
Briefly describe the strategies you followed and tools you used to achieve this in assurance.md.  
-Demonstration of an understanding of the need for software verification and validation  
-Development of appropriate acceptance criteria based on user stories and requirements.  
-Demonstration of appropriate tool usage for assurance (code coverage, linting, etc.)_




We used the user stories and the spec to start building our functions, with the pytests being used to make sure we were on the right track and that our functions were working correctly. We also created acceptance criteria based on the user stories on gitlab so that we were sure that the functions fit the requirements as we had interpreted them in the first iteration of the project.  

Software verification is required to make sure we have a working product that conforms to what was asked of us by the client, conforming to specifications that we had received and written tests for in iteration 1. Software validation is required to make sure the product does what would be required by a user, fitting what a user would need and want, done through acceptance criteria written from the user stories from iteration 1, as well as our own testing through the use of the frontend.

Acceptance critieria should be in the user stories on the task board

Verification  
-system has been built right  
-comparing product against required characteristics

Validation  
-the right system has been built  
-ensuring the system is able to accomplish its intended use, goals and objectives

Tool usage:  
pycoverage w/ pytest for coverage testing  
    -used to know whether our pytests are good and see where they can be improved  
    -code coverage, not test coverage  
    -testing how much of the code is being run rather than how much of the feature set is covered  
    -verification  

pytest to test our functions behave as intended  
    -whitebox unit testing  
    -verification

acceptance criteria and individuals using the frontend to test that it works  
    -black box testing, by users for validation

pylint for linting  
    -just makes code cleaner  
    -good for group project where we are sharing code