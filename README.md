# Social Network

 ### 1.  [Video Demonstration 45sec ](https://youtu.be/loSiFeFDmtA)

 ### 2. Launching

   The procedure described below presumes that you are using Bash. 
   Inside an empty folder, run: 
   
   ```
   git clone https://github.com/Evgeni6197/Portfolio4.git
   cd Portfolio4
   python3 -m venv ./venv
   source venv/bin/activate
   python -m pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

### 3. Content
  - User registration
  - Creating a new post
  - Viewing the overall post list 
  - User profile page 
  - Following and Unfollowing
  - Pagination
  - Editing posts
  - Liking and disliking
  - Adding comments

### 4. Tests

  - The project contains a set of 17 tests.
  - To run the tests, use the command: `python manage.py test`
  
 
  
