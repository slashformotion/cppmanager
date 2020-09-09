# cppmanager

A CLI tool build with python to create and modify basics C and C++ templates 


## Getting Started

### Dependancies

* click
* Python >= 3.6.x 

### Installing
For now, you need to download the cppmanager folder and import it manually

### Use it.

To create a basic project
```
cppmanager create main module1::namespace1::class1 module2::namespace2::class2
```

This will create this stucture
```
.-|
  |-main.cpp
  |-module1.hpp
  |-module1.cpp
  |-module2.hpp
  |-module2.cpp
```
Inside module1.hpp and module1.cpp you will find your namespace and class already there.

Of course, you are not supposed to create a class and a namespace every time. You can create the module with:
- a class and a namespace: `cppmanager create main module1::namespace1::class1`
- just a namespace: `cppmanager create main module1::namespace1`
- without a namespace and a class, just with some boilerplate code: `cppmanager create main module1`

>You can add as many modules as you want by adding arguments at the end of the command. They must respect this syntax: `{module_name}::{namespace_name}::{class_name}`

To add a module to an existing project
```
cppmanager add main module3::namespace3
```
This will create a module3.cpp and a module.hpp with the code magically in. Of course, main.cpp will be modified to include the header module3.hpp.


## Help
Create an issue [here](https://github.com/slashformotion/cppmanager/issues).