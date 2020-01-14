## Refactored Changes Across All Functions
### Data Storage
We were previous storing data in lists which we changed to dictionaries in iteration3, this was because:
  - Dictionaries remove the need to iterate through lists hence reducing most functions complexity to constant time
  - Allows a cleaner correlation between relevant data i.e. channel_id will be a key to all messages in a channel
  - Removes any risk of the data becoming unorganised in a way that would require any iteration to find data.

### Error handling on routes
 - Instead of each route having its own try except clause to abort on exception and return a json response to give the error in the format required for the frontend, a more general function has been used that catches any exceptions when the server is running and returns a required error in json format.
    - This works better than a decorator over each function because there's even less repetition as the need to include the decorator over each function is removed. Issues with decorators interfering with the flask routes are also completely eliminated.

### Imports
 - try except clauses were previously being used to allow pytests to be run inside the function directory - this was removed for cleaner code and 100% code coverage, but means we have to run tests from the root directory as well as change some of the pytests e.g. `with pytest.raises(functions.errors.AccessError)` rather than just `with pytest.raises(AccessError)`
    - This is a problem with pytest where the imports aren't consistent about where they're being run from - some files act like the errors file is on the same level being run from while others require the import to be from root. However, importing the actual functions being used are always treated as fine when imported from the same directory.
    - While this doesn't impact the functions themselves at all, it does mean import structure can vary between different test files
 - Changing import structure from `from x import y` to `import x` to reduce issues with cyclic imports as well as making the structure of the files cleaner and easier to understand.
    - Any added confusion due to the calling of files being longer (functions.auth_functions.auth_register) could be avoided by using `from x import y as z`

### Moving all related functions to one file
 - Moved all associated functions to relevant file e.g. channel functions to channel.py. This was because:
    - Imports are streamlined and removes cyclic Imports
    - Pytests are now able to run properly when called from root directory
    - Makes organising files clean and manageable

### Error checking functions
 - Functions were created to check whether a given variable was an int or string so these could be used throughout the project to avoid long sections of repetition

# Use of Software Engineering Principles

### DRY
 - Use of helper functions e.g. u_id extraction, enables developer to simply call function rather than repeat lines of code
 - Eliminating the try-except abort statements on routes
 - Functions to check variable types and raise errors

### KISS
 - Using a clear code style amongst all programmers allows the code to become harmonious and clear
 - Moving related files to one relevant file makes organising code easier
 - Removing cyclic imports and unneeded variables like standup initiator
 - Moving all tests to a single folder makes navigating directory easier
 - Cleaning up root directory and moving files to relevant iteration folders

### Top-down thinking
 - Functionality was initially added from the highest levels of abstraction
 - This gave us a solid base to work off
 - By using the spec given to us we created user stories and from that we implemented the functions, utilising top-down thinking

### Single Responsibility Principle
 -  Each function only has one purpose which it fulfils
 -  This allows to keep the code simply whilst also reducing repeated lines of code

### Abstraction
 -  Hiding internal details of an implementation, where all that needs to be known are the methods being called and the parameters required to trigger operations.
 -  Dealing with tokens is mostly entirely taken care of within the class and helper functions meaning the details of the token don't need to be known to be used, not being impacted by external changes and not needing to worry about other parts. Other functions only need to call set functions to receive whatever information they need about a token.
