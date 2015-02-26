# probabilistic-route-flow
This project defines a route as a policy over a graph, derived from
a specific path.

Usage
====
Currently, there is nothing to use.
    
Testing
====
To run the tests:

    python -m unittest discover

To run only the fast (eg. unit) tests:

    python -m unittest discover tests/fast

To run only the slow (eg. integration) tests:

    python -m unittest discover tests/slow

Development
====
* For this project, and any derived from it, please run the following command
  from the project root directory:

      ln -s ../../pre-commit.sh .git/hooks/pre-commit

* Write unit tests as you go. Document as you go.
* Run all unit tests before you push any code.

References
====
