# pyutap
Python wrapper library for [libutap](https://github.com/UPPAALModelChecker/utap). This project is still a work in progress.

To be able to use this library, libutap has to be built dynamically.

### Dependencies:

- [libutap](https://github.com/UPPAALModelChecker/utap) Uppaal timed automata parser

- [cppyy](https://github.com/wlav/cppyy) >= 1.7.1


### Building UTAP dynamically:
Copy the patch to cloned libutap directory and apply with:

	git apply dynamic_patch.patch && autoreconf -i

Then build with the instructions specified in libutap's repository.


### Install pyutap:
Simply run:

	pip install .


#### TODOs:
- Expose bindings in a faster and more useful way
- Error handling, prevent crashing of the Python kernel completely
- ~Run verifyta~ -> To be tested
- Better and additional installation instructions, like installing in virtualenv
- Proper explanations and usage examples in markdown

In case of any problem or suggestion, feel free to create an issue or send me an email.