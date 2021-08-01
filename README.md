# ATM-CLI-Project
It is quite a simple project where I am trying to work with OOPs concepts in python and learning to use advanced python refactoring techniques.

It stores the data in Pickle files, so created accounts and the funds in each of them are saved even if the file is closed. The next time you run the code it will pick up from where it was last left. I've tried to refactor the code as much as I could and forced myself to over-engineer this, so as to practice the things I've learnt as a developer and apply them in a project.

By no means this is a useful project to anyone but it has helped me gain some knowledge on industry-ready code.

Things, where I think this still lacks, are:
1. Need a better way than if-elif statements to navigate the menu. The solution I thought was to use function reference in a dict() with their menu option as the key. This worked, as I could easily add a new feature without writing a special if-elif block but had problems passing arguments to the functions.
2. A large ATM class is not ideal, I need to beak it into other special classes.
3. Some functions are still not atomic and need to break up, but currently, I'm unable to break them further without handling many special edge cases,
