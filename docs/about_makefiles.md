# About Makefiles

Makefiles are usually used to compile code, so why are we using one for Python? There's a lot more you can do
with them! Most of the make commands we have set up are convenient aliases to script tasks such as running the
application, creating the virtual environment, or linting the code.

To use makefiles, make needs to be installed.

For more info about makefiles and some of the things you can do with them, check out
[this overview](https://opensource.com/article/18/8/what-how-makefile).

## Example Usage
* Run the application
    ```bash
    make run
    ```
    This has a dependency of the virtual environment, so it will build that also if needed!
