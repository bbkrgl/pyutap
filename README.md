# pyutap
Wrapper library for [libutap](https://github.com/UPPAALModelChecker/utap).

To be able to use this library, libutap has to be built dynamically.

### Dependencies:

- [libutap](https://github.com/UPPAALModelChecker/utap) Uppaal timed automata parser

- [cppyy](https://github.com/wlav/cppyy) >= 1.7.1


### Building UTAP dynamically:
Copy the patch to cloned libutap directory and apply with:

	git apply dynamic_patch.patch

Then build with the instructions specified in libutap's repository.


#### TODOs:
- Add TODOs

In case of any problem or suggestion, feel free to create an issue or send me an email.
