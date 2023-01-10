## How to do non-standard changes

Add a chapter:

- Add plain chapter name to Contents.md
  e.g.   ```25. Interesting Stuff```
- run makeBook

Add a section:

- add Name to chapter base file
  e.g.  ```## Interesting Section```
- run makeBook

Delete a section:

- Delete section file
- Delete ```##``` line from chapter base file
- run makeBook
- run indexBook (and check warnings of broken citations)

Delete a chapter:

- Delete ```N. Name directory```
- Delete ```N. Name``` block from Contents.md
- run makeBook
- run indexBook (and check warnings of broken citations)

Rename a section:

- rename section file
- change ``##`` text in section file
- change ``##`` link in chapter base file
- run makeBook
- run indexBook (and check warnings of broken citations)

Rename or renumber a chapter:

- rename chapter in Contents.md
  e.g. ```11. Chapter Test```
- rename chapter directory
- rename chapter base file
- change title in base file
  e.g. ```# 11. Chapter Test```
- run makeBook
- run indexBook (and check warnings of broken citations)